"""
Router de autenticación passwordless con OTP por WhatsApp.

Endpoints:
- POST /auth/request-code: Envía código OTP por WhatsApp
- POST /auth/verify: Valida OTP y retorna JWT
"""

import logging
import os
from pathlib import Path
from typing import Optional

import pandas as pd
from fastapi import APIRouter, HTTPException, status, Request
from pydantic import BaseModel, Field

from services.auth_service import (
    cleanup_expired_otps,
    create_jwt_token,
    generate_otp,
    get_otp_storage_stats,
    store_otp,
    verify_otp
)
from services.whatsapp import send_whatsapp_message
from middleware.rate_limit import limiter

logger = logging.getLogger(__name__)

router = APIRouter()

# Path al CSV de proveedores
PROVEEDORES_CSV = Path(__file__).parent.parent / "data" / "proveedores.csv"


# ══════════════════════════════════════════════════════════════
# MODELOS PYDANTIC
# ══════════════════════════════════════════════════════════════

class RequestCodeRequest(BaseModel):
    """Request body para solicitar código OTP."""
    cuit: str = Field(..., description="CUIT del proveedor (formato XX-XXXXXXXX-X o sin guiones)")

    class Config:
        json_schema_extra = {
            "example": {
                "cuit": "30-12345678-9"
            }
        }


class VerifyCodeRequest(BaseModel):
    """Request body para verificar código OTP."""
    cuit: str = Field(..., description="CUIT del proveedor")
    code: str = Field(..., min_length=6, max_length=6, description="Código OTP de 6 caracteres")

    class Config:
        json_schema_extra = {
            "example": {
                "cuit": "30-12345678-9",
                "code": "K7M2N9"
            }
        }


class AuthResponse(BaseModel):
    """Response exitoso de autenticación."""
    token: str = Field(..., description="JWT firmado")
    proveedor: dict = Field(..., description="Datos del proveedor")


# ══════════════════════════════════════════════════════════════
# HELPERS
# ══════════════════════════════════════════════════════════════

def normalize_cuit(cuit: str) -> str:
    """Normaliza el formato del CUIT removiendo guiones."""
    return cuit.replace("-", "").strip()


def load_proveedores() -> pd.DataFrame:
    """Carga el CSV de proveedores."""
    try:
        # Forzar columnas críticas como string para evitar conversión numérica
        df = pd.read_csv(
            PROVEEDORES_CSV,
            dtype={
                'cuit': str,
                'whatsapp': str  # Importante: evitar que pandas lo convierta a int64
            }
        )
        # Normalizar CUITs en el DataFrame
        df['cuit_normalized'] = df['cuit'].astype(str).apply(normalize_cuit)
        return df
    except FileNotFoundError:
        logger.error(f"Archivo de proveedores no encontrado: {PROVEEDORES_CSV}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error de configuración del servidor"
        )
    except Exception as e:
        logger.error(f"Error al cargar proveedores: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al procesar datos de proveedores"
        )


def find_proveedor(cuit: str) -> Optional[dict]:
    """
    Busca un proveedor por CUIT en el CSV.

    Args:
        cuit: CUIT a buscar (se normaliza automáticamente)

    Returns:
        Dict con datos del proveedor o None si no existe
    """
    df = load_proveedores()
    cuit_normalized = normalize_cuit(cuit)

    result = df[df['cuit_normalized'] == cuit_normalized]

    if result.empty:
        return None

    row = result.iloc[0]

    return {
        "cuit": row['cuit'],
        "razon_social": row['razon_social'],
        "localidad": row['localidad'],
        "provincia": row['provincia'],
        "rubro": row['rubro'],
        "whatsapp": row['whatsapp']
    }


# ══════════════════════════════════════════════════════════════
# ENDPOINTS
# ══════════════════════════════════════════════════════════════

@router.post("/request-code", status_code=status.HTTP_200_OK)
@limiter.limit("3/minute")  # Máximo 3 solicitudes por minuto
async def request_code(http_request: Request, request: RequestCodeRequest):
    """
    Solicita un código OTP enviado por WhatsApp.

    Flujo:
    1. Busca el proveedor en el CSV por CUIT
    2. Genera código OTP de 6 caracteres
    3. Envía código por WhatsApp vía Twilio
    4. Almacena código en memoria con TTL de 30 min

    Returns:
        Confirmación del envío
    """
    # Cleanup de códigos expirados
    cleanup_expired_otps()

    # Buscar proveedor
    proveedor = find_proveedor(request.cuit)

    if not proveedor:
        logger.warning(f"Intento de autenticación con CUIT no registrado: {request.cuit}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="CUIT no encontrado en el padrón de proveedores"
        )

    # Generar código OTP
    otp = generate_otp()

    # Mensaje WhatsApp
    mensaje = f"""¡Hola {proveedor['razon_social']}!

Tu código de acceso a AsisteCR+ Portal del Proveedor es:

*{otp}*

Este código es válido por 30 minutos.

_Municipalidad de Comodoro Rivadavia_"""

    # Enviar por WhatsApp
    try:
        message_sid = await send_whatsapp_message(
            to=proveedor['whatsapp'],
            body=mensaje
        )

        logger.info(f"OTP enviado a {proveedor['razon_social']} (SID: {message_sid})")

    except Exception as e:
        logger.error(f"Error al enviar OTP por WhatsApp: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al enviar código por WhatsApp. Intente nuevamente."
        )

    # Almacenar código
    store_otp(cuit=normalize_cuit(request.cuit), otp=otp)

    return {
        "message": "Código enviado por WhatsApp",
        "whatsapp": proveedor['whatsapp'][-4:].rjust(len(proveedor['whatsapp']), '*'),  # Enmascarar número
        "expires_in_minutes": 30
    }


@router.post("/verify", status_code=status.HTTP_200_OK, response_model=AuthResponse)
@limiter.limit("5/minute")  # Máximo 5 intentos de verificación por minuto
async def verify_code(http_request: Request, request: VerifyCodeRequest):
    """
    Verifica el código OTP y retorna un JWT.

    Flujo:
    1. Valida el código OTP
    2. Si es correcto, genera JWT firmado con datos del proveedor
    3. JWT expira en 8 horas

    Returns:
        JWT y datos del proveedor
    """
    # Cleanup de códigos expirados
    cleanup_expired_otps()

    # Buscar proveedor
    proveedor = find_proveedor(request.cuit)

    if not proveedor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="CUIT no encontrado"
        )

    # Verificar código OTP
    cuit_normalized = normalize_cuit(request.cuit)

    if not verify_otp(cuit=cuit_normalized, otp=request.code):
        logger.warning(f"Intento de login con código inválido para CUIT {request.cuit}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Código inválido o expirado"
        )

    # Generar JWT
    try:
        token = create_jwt_token(
            cuit=proveedor['cuit'],
            razon_social=proveedor['razon_social'],
            rubro=proveedor['rubro'],
            whatsapp=proveedor['whatsapp']
        )

        logger.info(f"Login exitoso para {proveedor['razon_social']} (CUIT {proveedor['cuit']})")

        return {
            "token": token,
            "proveedor": {
                "cuit": proveedor['cuit'],
                "nombre": proveedor['razon_social'],
                "rubro": proveedor['rubro'],
                "localidad": proveedor['localidad'],
                "whatsapp": proveedor['whatsapp']
            }
        }

    except ValueError as e:
        logger.error(f"Error al generar JWT: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error de configuración del servidor"
        )


@router.get("/stats", status_code=status.HTTP_200_OK)
async def get_auth_stats():
    """
    Retorna estadísticas del sistema de autenticación.

    Solo para debugging/monitoreo. En producción debería estar protegido.
    """
    stats = get_otp_storage_stats()

    return {
        "otp_storage": stats,
        "environment": {
            "jwt_configured": bool(os.getenv("JWT_SECRET")),
            "twilio_configured": bool(os.getenv("TWILIO_ACCOUNT_SID"))
        }
    }
