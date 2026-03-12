"""
Middleware de rate limiting usando slowapi.
"""

import os
from slowapi import Limiter
from slowapi.util import get_remote_address

# Configurar storage para rate limiting
# En producción con Redis, usar: storage_uri=os.getenv("REDIS_URL")
# En desarrollo, usar memoria (default)
redis_url = os.getenv("REDIS_URL")

if redis_url:
    # Producción: Redis
    limiter = Limiter(
        key_func=get_remote_address,
        storage_uri=redis_url
    )
else:
    # Desarrollo: Memoria (requiere enabled=False si hay problemas)
    limiter = Limiter(
        key_func=get_remote_address,
        default_limits=["100/minute"],
        enabled=False  # Deshabilitar en desarrollo para evitar errores
    )
