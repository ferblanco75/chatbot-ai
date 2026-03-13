"""
Router de autenticación passwordless con OTP por email.

Endpoints:
- POST /auth/request-code: Envía código OTP por email
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
from services.email import send_otp_email
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
        "whatsapp": str(row.get('whatsapp', '')),
        "email": str(row.get('email', ''))
    }


# ══════════════════════════════════════════════════════════════
# ENDPOINTS
# ══════════════════════════════════════════════════════════════

@router.post("/request-code", status_code=status.HTTP_200_OK)
@limiter.limit("3/minute")  # Máximo 3 solicitudes por minuto
async def request_code(request: Request, body: RequestCodeRequest):
    """
    Solicita un código OTP enviado por email.

    Flujo:
    1. Busca el proveedor en el CSV por CUIT
    2. Genera código OTP de 6 caracteres
    3. Envía código por email vía Resend
    4. Almacena código en memoria con TTL de 30 min

    Returns:
        Confirmación del envío
    """
    # Cleanup de códigos expirados
    cleanup_expired_otps()

    # Buscar proveedor
    proveedor = find_proveedor(body.cuit)

    if not proveedor:
        logger.warning(f"Intento de autenticación con CUIT no registrado: {body.cuit}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="CUIT no encontrado en el padrón de proveedores"
        )

    email = proveedor.get('email', '').strip()
    if not email or email in ('nan', ''):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="El proveedor no tiene email registrado. Contactá a controldocumentalyproveedores@comodoro.gov.ar"
        )

    # Generar código OTP
    otp = generate_otp()

    # Enviar por email
    try:
        message_id = await send_otp_email(
            to=email,
            otp=otp,
            razon_social=proveedor['razon_social']
        )
        logger.info(f"OTP enviado a {proveedor['razon_social']} por email (ID: {message_id})")

    except Exception as e:
        logger.error(f"Error al enviar OTP por email: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al enviar código por email. Intente nuevamente."
        )

    # Almacenar código
    store_otp(cuit=normalize_cuit(body.cuit), otp=otp)

    # Enmascarar email: usuario@dominio.com → usu***@dominio.com
    partes = email.split('@')
    email_masked = partes[0][:3] + '***@' + partes[1] if len(partes) == 2 else '***'

    return {
        "message": "Código enviado por email",
        "email": email_masked,
        "expires_in_minutes": 30
    }


@router.post("/verify", status_code=status.HTTP_200_OK, response_model=AuthResponse)
@limiter.limit("5/minute")  # Máximo 5 intentos de verificación por minuto
async def verify_code(request: Request, body: VerifyCodeRequest):
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
    proveedor = find_proveedor(body.cuit)

    if not proveedor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="CUIT no encontrado"
        )

    # Verificar código OTP
    cuit_normalized = normalize_cuit(body.cuit)

    if not verify_otp(cuit=cuit_normalized, otp=body.code):
        logger.warning(f"Intento de login con código inválido para CUIT {body.cuit}")
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


@router.get("/test-twilio", status_code=status.HTTP_200_OK)
async def test_twilio_config():
    """
    Verifica la configuración de Twilio sin enviar mensajes.

    Solo para debugging. En producción debería estar protegido.
    """
    from services.whatsapp import verify_twilio_config

    config = await verify_twilio_config()

    return {
        "twilio": config,
        "env_vars": {
            "TWILIO_ACCOUNT_SID": os.getenv("TWILIO_ACCOUNT_SID")[:10] + "..." if os.getenv("TWILIO_ACCOUNT_SID") else None,
            "TWILIO_AUTH_TOKEN": "***" if os.getenv("TWILIO_AUTH_TOKEN") else None,
            "TWILIO_WHATSAPP_FROM": os.getenv("TWILIO_WHATSAPP_FROM")
        }
    }


class TestWhatsAppRequest(BaseModel):
    """Request body para enviar WhatsApp de prueba."""
    phone_number: str = Field(..., description="Número de teléfono en formato E.164 (ej: +5492974123456)")
    message: Optional[str] = Field(None, description="Mensaje personalizado (opcional)")

    class Config:
        json_schema_extra = {
            "example": {
                "phone_number": "+5492974123456",
                "message": "Mensaje de prueba desde AsisteCR+"
            }
        }


@router.post("/test-whatsapp", status_code=status.HTTP_200_OK)
async def test_whatsapp_send(request: TestWhatsAppRequest):
    """
    Envía un mensaje de WhatsApp de prueba.

    Solo para debugging. En producción debería estar protegido con contraseña admin.
    """
    mensaje = request.message or "Este es un mensaje de prueba desde AsisteCR+ - Sistema de Autenticación"

    try:
        message_sid = await send_whatsapp_message(
            to=request.phone_number,
            body=mensaje
        )

        return {
            "success": True,
            "message": "Mensaje enviado exitosamente",
            "message_sid": message_sid,
            "to": request.phone_number
        }

    except Exception as e:
        logger.error(f"Error en test de WhatsApp: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al enviar mensaje: {str(e)}"
        )


@router.post("/debug-request-code", status_code=status.HTTP_200_OK)
async def debug_request_code(request: RequestCodeRequest):
    """
    Versión debug de request-code sin rate limiting.

    Para identificar el error específico.
    """
    try:
        # Paso 1: Buscar proveedor
        logger.info(f"Buscando proveedor con CUIT: {request.cuit}")
        proveedor = find_proveedor(request.cuit)

        if not proveedor:
            return {"error": "Proveedor no encontrado", "cuit": request.cuit}

        logger.info(f"Proveedor encontrado: {proveedor}")

        # Paso 2: Generar OTP
        otp = generate_otp()
        logger.info(f"OTP generado: {otp}")

        # Paso 3: Preparar mensaje
        mensaje = f"""¡Hola {proveedor['razon_social']}!

Tu código de acceso a AsisteCR+ Portal del Proveedor es:

*{otp}*

Este código es válido por 30 minutos.

_Municipalidad de Comodoro Rivadavia_"""

        logger.info(f"Mensaje preparado, enviando a: {proveedor['whatsapp']}")

        # Paso 4: Enviar WhatsApp
        message_sid = await send_whatsapp_message(
            to=proveedor['whatsapp'],
            body=mensaje
        )

        logger.info(f"Mensaje enviado: {message_sid}")

        # Paso 5: Almacenar OTP
        store_otp(cuit=normalize_cuit(request.cuit), otp=otp)

        return {
            "success": True,
            "proveedor": proveedor['razon_social'],
            "whatsapp": proveedor['whatsapp'],
            "otp": otp,  # Solo para debug
            "message_sid": message_sid
        }

    except Exception as e:
        logger.error(f"Error en debug-request-code: {e}", exc_info=True)
        import traceback
        return {
            "error": str(e),
            "type": type(e).__name__,
            "traceback": traceback.format_exc()
        }
