"""
Middleware de autenticación JWT para FastAPI.

Provee dependencies para proteger endpoints que requieren autenticación.

Uso:
    from middleware.auth import get_current_user

    @router.get("/protected")
    async def protected_endpoint(user: dict = Depends(get_current_user)):
        return {"user": user["nombre"]}
"""

import logging
from typing import Dict, Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from services.auth_service import extract_bearer_token, verify_jwt_token

logger = logging.getLogger(__name__)

# Security scheme para OpenAPI/Swagger docs
security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> Dict:
    """
    Dependency de FastAPI que verifica el JWT y retorna el usuario autenticado.

    Args:
        credentials: Credenciales del header Authorization (automático)

    Returns:
        Payload del JWT con datos del proveedor

    Raises:
        HTTPException 401: Si el token es inválido o expirado
    """
    token = credentials.credentials

    if not token:
        logger.warning("Intento de acceso sin token")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token de autenticación requerido",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Verificar y decodificar JWT
    payload = verify_jwt_token(token)

    if not payload:
        logger.warning("Intento de acceso con token inválido")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o expirado",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return payload


async def get_optional_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(HTTPBearer(auto_error=False))
) -> Optional[Dict]:
    """
    Dependency opcional que retorna el usuario si hay token, o None si no lo hay.

    Útil para endpoints que funcionan con o sin autenticación pero cambian su
    comportamiento según el estado del usuario.

    Args:
        credentials: Credenciales opcionales

    Returns:
        Payload del JWT o None si no hay token o es inválido
    """
    if not credentials:
        return None

    token = credentials.credentials

    if not token:
        return None

    # Verificar token sin lanzar excepciones
    payload = verify_jwt_token(token)

    return payload


def require_cuit(allowed_cuits: list):
    """
    Factory que crea un dependency para verificar que el usuario tenga un CUIT específico.

    Útil para endpoints que solo deben ser accesibles por ciertos proveedores.

    Ejemplo:
        @router.get("/admin")
        async def admin_endpoint(user: dict = Depends(require_cuit(["30-12345678-9"]))):
            return {"message": "Admin access"}

    Args:
        allowed_cuits: Lista de CUITs permitidos

    Returns:
        Dependency function
    """
    async def verify_cuit(user: Dict = Depends(get_current_user)) -> Dict:
        if user.get("cuit") not in allowed_cuits:
            logger.warning(f"CUIT {user.get('cuit')} intentó acceder a endpoint restringido")
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes permisos para acceder a este recurso"
            )
        return user

    return verify_cuit


def require_rubro(allowed_rubros: list):
    """
    Factory que crea un dependency para verificar que el usuario tenga un rubro específico.

    Útil para endpoints que solo deben ser accesibles por ciertos rubros.

    Ejemplo:
        @router.get("/licitaciones-construccion")
        async def construccion_endpoint(user: dict = Depends(require_rubro(["construccion"]))):
            return {"message": "Solo proveedores de construcción"}

    Args:
        allowed_rubros: Lista de rubros permitidos

    Returns:
        Dependency function
    """
    async def verify_rubro(user: Dict = Depends(get_current_user)) -> Dict:
        if user.get("rubro") not in allowed_rubros:
            logger.warning(f"Rubro {user.get('rubro')} intentó acceder a endpoint restringido")
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Este recurso no está disponible para tu rubro"
            )
        return user

    return verify_rubro
