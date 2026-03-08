"""
Servicio de autenticación con OTP y JWT.

Implementa:
- Generación de códigos OTP aleatorios de 6 caracteres
- Almacenamiento con Redis (producción) o memoria (desarrollo)
- Generación y firma de JWT con expiración de 8 horas
- Validación de códigos OTP y tokens JWT
"""

import logging
import os
import random
import string
from datetime import datetime, timedelta
from typing import Dict, Optional

import jwt
from jwt.exceptions import InvalidTokenError

logger = logging.getLogger(__name__)

# ══════════════════════════════════════════════════════════════
# STORAGE BACKEND SELECTION
# ══════════════════════════════════════════════════════════════

REDIS_URL = os.getenv("REDIS_URL")

if REDIS_URL:
    # Producción: usar Redis
    try:
        import redis
        _redis_client = redis.from_url(REDIS_URL, decode_responses=True)
        # Verificar conexión
        _redis_client.ping()
        logger.info("OTP storage: Redis configurado y conectado")
        USE_REDIS = True
    except Exception as e:
        logger.warning(f"Redis configurado pero no disponible ({e}), usando memoria")
        _otp_storage: Dict[str, Dict] = {}
        USE_REDIS = False
else:
    # Desarrollo: usar memoria
    _otp_storage: Dict[str, Dict] = {}
    logger.warning("OTP storage: usando memoria (solo para desarrollo)")
    USE_REDIS = False


# ══════════════════════════════════════════════════════════════
# OTP FUNCTIONS
# ══════════════════════════════════════════════════════════════

def generate_otp(length: int = 6) -> str:
    """
    Genera un código OTP aleatorio alfanumérico.

    Args:
        length: Longitud del código (por defecto 6)

    Returns:
        Código OTP en mayúsculas (ej: "K7M2N9")
    """
    characters = string.ascii_uppercase + string.digits
    otp = ''.join(random.choice(characters) for _ in range(length))

    logger.info(f"OTP generado: {otp[:2]}****")

    return otp


def store_otp(cuit: str, otp: str, ttl_minutes: int = 30) -> None:
    """
    Almacena un código OTP con TTL.

    En Redis: usa TTL automático con SETEX
    En memoria: guarda expires_at manualmente

    Args:
        cuit: CUIT del proveedor
        otp: Código OTP a almacenar
        ttl_minutes: Tiempo de vida en minutos (por defecto 30)
    """
    if USE_REDIS:
        # Redis: SETEX con TTL automático
        key = f"otp:{cuit}"
        _redis_client.setex(key, ttl_minutes * 60, otp)
        logger.info(f"OTP almacenado en Redis para CUIT {cuit}, TTL {ttl_minutes}min")
    else:
        # Memoria: guardar con expires_at
        expires_at = datetime.now() + timedelta(minutes=ttl_minutes)
        _otp_storage[cuit] = {
            "code": otp,
            "expires_at": expires_at
        }
        logger.info(f"OTP almacenado en memoria para CUIT {cuit}, expira {expires_at.strftime('%H:%M:%S')}")


def verify_otp(cuit: str, otp: str) -> bool:
    """
    Verifica si un código OTP es válido.

    En Redis: GET key, luego DEL para evitar reutilización
    En memoria: verificar expires_at, luego DEL

    Args:
        cuit: CUIT del proveedor
        otp: Código OTP a verificar

    Returns:
        True si el código es válido, False en caso contrario
    """
    if USE_REDIS:
        key = f"otp:{cuit}"
        stored_otp = _redis_client.get(key)

        if not stored_otp:
            logger.warning(f"No hay OTP en Redis para CUIT {cuit}")
            return False

        if stored_otp != otp.upper():
            logger.warning(f"Código OTP inválido para CUIT {cuit}")
            return False

        # Código válido → eliminar para evitar reutilización
        _redis_client.delete(key)
        logger.info(f"OTP verificado exitosamente para CUIT {cuit}")
        return True

    else:
        # Memoria: verificar manualmente
        if cuit not in _otp_storage:
            logger.warning(f"No hay OTP en memoria para CUIT {cuit}")
            return False

        stored_data = _otp_storage[cuit]

        # Verificar expiración
        if datetime.now() > stored_data["expires_at"]:
            logger.warning(f"OTP expirado para CUIT {cuit}")
            del _otp_storage[cuit]
            return False

        # Verificar código
        if stored_data["code"] != otp.upper():
            logger.warning(f"Código OTP inválido para CUIT {cuit}")
            return False

        # Código válido → eliminar
        del _otp_storage[cuit]
        logger.info(f"OTP verificado exitosamente para CUIT {cuit}")
        return True


def cleanup_expired_otps() -> int:
    """
    Limpia códigos OTP expirados.

    En Redis: no es necesario (TTL automático)
    En memoria: manual cleanup

    Returns:
        Cantidad de códigos eliminados
    """
    if USE_REDIS:
        # Redis maneja TTL automáticamente
        return 0

    else:
        # Memoria: cleanup manual
        now = datetime.now()
        expired_cuits = [
            cuit for cuit, data in _otp_storage.items()
            if now > data["expires_at"]
        ]

        for cuit in expired_cuits:
            del _otp_storage[cuit]

        if expired_cuits:
            logger.info(f"Limpiados {len(expired_cuits)} OTPs expirados")

        return len(expired_cuits)


def get_otp_storage_stats() -> Dict:
    """
    Retorna estadísticas del almacenamiento de OTPs.

    Returns:
        Dict con backend usado y cantidad de OTPs almacenados
    """
    if USE_REDIS:
        # Redis: contar keys con patrón otp:*
        keys = _redis_client.keys("otp:*")
        return {
            "backend": "redis",
            "total_stored": len(keys),
            "expired": 0,  # Redis maneja automáticamente
            "active": len(keys)
        }
    else:
        # Memoria: contar manualmente
        total = len(_otp_storage)
        now = datetime.now()
        expired = sum(1 for data in _otp_storage.values() if now > data["expires_at"])

        return {
            "backend": "memory",
            "total_stored": total,
            "expired": expired,
            "active": total - expired
        }


# ══════════════════════════════════════════════════════════════
# JWT FUNCTIONS
# ══════════════════════════════════════════════════════════════

def create_jwt_token(
    cuit: str,
    razon_social: str,
    rubro: str,
    whatsapp: str,
    expires_hours: Optional[int] = None
) -> str:
    """
    Genera un JWT firmado con información del proveedor.

    Args:
        cuit: CUIT del proveedor
        razon_social: Nombre de la empresa
        rubro: Rubro del proveedor
        whatsapp: Número de WhatsApp
        expires_hours: Horas de validez del token (por defecto lee de env)

    Returns:
        Token JWT firmado

    Raises:
        ValueError: Si no hay JWT_SECRET configurado
    """
    secret = os.getenv("JWT_SECRET")
    if not secret:
        raise ValueError("JWT_SECRET no configurado en variables de entorno")

    if expires_hours is None:
        expires_hours = int(os.getenv("JWT_EXPIRES_HOURS", "8"))

    # Payload del JWT
    now = datetime.utcnow()
    payload = {
        # Claims estándar
        "iat": now,  # Issued at
        "exp": now + timedelta(hours=expires_hours),  # Expiration
        "nbf": now,  # Not before

        # Claims custom
        "cuit": cuit,
        "nombre": razon_social,
        "rubro": rubro,
        "whatsapp": whatsapp
    }

    # Firmar token
    token = jwt.encode(payload, secret, algorithm="HS256")

    logger.info(f"JWT generado para {razon_social} (CUIT {cuit}), expira en {expires_hours}h")

    return token


def verify_jwt_token(token: str) -> Optional[Dict]:
    """
    Verifica y decodifica un JWT.

    Args:
        token: Token JWT a verificar

    Returns:
        Payload decodificado si el token es válido, None en caso contrario
    """
    secret = os.getenv("JWT_SECRET")
    if not secret:
        logger.error("JWT_SECRET no configurado")
        return None

    try:
        payload = jwt.decode(
            token,
            secret,
            algorithms=["HS256"],
            options={
                "verify_signature": True,
                "verify_exp": True,
                "verify_nbf": True
            }
        )

        logger.info(f"JWT válido para CUIT {payload.get('cuit')}")

        return payload

    except jwt.ExpiredSignatureError:
        logger.warning("JWT expirado")
        return None

    except jwt.InvalidTokenError as e:
        logger.warning(f"JWT inválido: {e}")
        return None

    except Exception as e:
        logger.error(f"Error al verificar JWT: {e}")
        return None


def extract_bearer_token(authorization_header: str) -> Optional[str]:
    """
    Extrae el token de un header Authorization: Bearer <token>.

    Args:
        authorization_header: Valor del header Authorization

    Returns:
        Token extraído o None si el formato es inválido
    """
    if not authorization_header:
        return None

    parts = authorization_header.split()

    if len(parts) != 2 or parts[0].lower() != "bearer":
        logger.warning(f"Formato de Authorization header inválido: {authorization_header[:20]}...")
        return None

    return parts[1]
