"""
Entry point de la aplicación FastAPI.
Asistente de Compras - Municipalidad de Comodoro Rivadavia
"""

import logging
import os
from contextlib import asynccontextmanager
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from starlette.middleware.base import BaseHTTPMiddleware

from routers import licitaciones, proveedores, notificaciones, chat, auth
from middleware.rate_limit import limiter

# Cargar variables de entorno desde backend/.env
env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


# ══════════════════════════════════════════════════════════════
# MIDDLEWARE PARA OPTIONS
# ══════════════════════════════════════════════════════════════

class OptionsMiddleware(BaseHTTPMiddleware):
    """Middleware que maneja peticiones OPTIONS (CORS preflight) antes del rate limiting."""

    async def dispatch(self, request: Request, call_next):
        if request.method == "OPTIONS":
            # Para peticiones OPTIONS, retornar respuesta vacía con headers CORS
            # El CORSMiddleware agregará los headers necesarios
            return Response(status_code=200)

        return await call_next(request)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manejo del ciclo de vida de la aplicación."""
    logger.info("Iniciando aplicación FastAPI")
    yield
    logger.info("Cerrando aplicación FastAPI")


# Crear aplicación FastAPI
app = FastAPI(
    title="Asistente de Compras - Municipalidad de Comodoro Rivadavia",
    description="API para licitaciones, proveedores y notificaciones WhatsApp",
    version="1.0.0",
    lifespan=lifespan
)

# Configurar rate limiting
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Configurar CORS
cors_origins_str = os.getenv("CORS_ORIGINS", "http://localhost:3000,https://chatbot-ai-eta.vercel.app")
cors_origins = [origin.strip() for origin in cors_origins_str.split(",")]
logger.info(f"CORS habilitado para: {cors_origins}")

# IMPORTANTE: OptionsMiddleware debe ir PRIMERO (se ejecuta en orden inverso)
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(OptionsMiddleware)

# Montar routers
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(licitaciones.router, prefix="/licitaciones", tags=["licitaciones"])
app.include_router(proveedores.router, prefix="/proveedores", tags=["proveedores"])
app.include_router(notificaciones.router, prefix="/notificaciones", tags=["notificaciones"])
app.include_router(chat.router, prefix="/chat", tags=["chat"])


@app.get("/")
async def root():
    """Health check endpoint."""
    return {
        "status": "ok",
        "service": "Asistente de Compras - Municipalidad de Comodoro Rivadavia",
        "version": "1.0.0"
    }


@app.get("/health")
async def health_check():
    """Endpoint de health check para monitoreo."""
    return {"status": "healthy"}


@app.get("/debug/env")
async def debug_env():
    """Debug endpoint para verificar variables de entorno."""
    return {
        "env_file_path": str(env_path),
        "env_file_exists": env_path.exists(),
        "twilio_configured": bool(os.getenv("TWILIO_ACCOUNT_SID")),
        "jwt_configured": bool(os.getenv("JWT_SECRET")),
        "anthropic_configured": bool(os.getenv("ANTHROPIC_API_KEY")),
        "twilio_sid_prefix": os.getenv("TWILIO_ACCOUNT_SID")[:10] if os.getenv("TWILIO_ACCOUNT_SID") else None
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
