"""
Middleware de rate limiting usando slowapi.
"""

from slowapi import Limiter
from slowapi.util import get_remote_address

# Limiter global
limiter = Limiter(key_func=get_remote_address)
