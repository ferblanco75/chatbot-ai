"""
Entry point de la aplicación FastAPI.
Asistente de Compras - Municipalidad de Comodoro Rivadavia
"""

import logging
import os
from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import licitaciones, proveedores, notificaciones

# Cargar variables de entorno
load_dotenv()

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


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

# Configurar CORS
cors_origins = os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Montar routers
app.include_router(licitaciones.router, prefix="/licitaciones", tags=["licitaciones"])
app.include_router(proveedores.router, prefix="/proveedores", tags=["proveedores"])
app.include_router(notificaciones.router, prefix="/notificaciones", tags=["notificaciones"])


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


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
