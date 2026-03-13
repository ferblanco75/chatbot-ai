"""
Middleware de rate limiting usando slowapi.
Usa memoria en todos los entornos — Redis se reserva para OTPs.
"""

from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["100/minute"],
)
