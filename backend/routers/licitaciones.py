"""
Router para endpoints de licitaciones.
GET /licitaciones - Lista todas las licitaciones
POST /licitaciones - Crea una nueva licitación (requiere auth)
"""

import json
import logging
import os
from datetime import datetime
from pathlib import Path
from typing import List, Optional

from fastapi import APIRouter, HTTPException, Header
from pydantic import BaseModel, Field

from services.scraper import scrape_licitaciones

logger = logging.getLogger(__name__)

router = APIRouter()

# Path al archivo de licitaciones
DATA_DIR = Path(__file__).parent.parent / "data"
LICITACIONES_FILE = DATA_DIR / "licitaciones.json"


class Licitacion(BaseModel):
    """Modelo de una licitación."""
    id: str
    titulo: str
    descripcion: str
    numero_expediente: Optional[str] = None
    fecha_publicacion: str
    fecha_apertura: str
    presupuesto_oficial: Optional[float] = None
    rubro: str
    estado: str = "abierta"
    url_pliego: Optional[str] = None
    contacto: str = "licitacionesyconcursos@comodoro.gov.ar"


class LicitacionCreate(BaseModel):
    """Modelo para crear una licitación."""
    titulo: str = Field(..., min_length=10)
    descripcion: str = Field(..., min_length=20)
    numero_expediente: Optional[str] = None
    fecha_apertura: str
    presupuesto_oficial: Optional[float] = None
    rubro: str
    url_pliego: Optional[str] = None


def load_licitaciones() -> List[dict]:
    """Carga las licitaciones desde el archivo JSON."""
    if not LICITACIONES_FILE.exists():
        return []

    try:
        with open(LICITACIONES_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data.get("licitaciones", [])
    except Exception as e:
        logger.error(f"Error cargando licitaciones: {e}")
        return []


def save_licitaciones(licitaciones: List[dict]) -> None:
    """Guarda las licitaciones en el archivo JSON."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    try:
        with open(LICITACIONES_FILE, "w", encoding="utf-8") as f:
            json.dump({"licitaciones": licitaciones}, f, ensure_ascii=False, indent=2)
    except Exception as e:
        logger.error(f"Error guardando licitaciones: {e}")
        raise


@router.get("", response_model=List[Licitacion])
async def get_licitaciones(
    rubro: Optional[str] = None,
    estado: Optional[str] = None,
    refresh: bool = False
):
    """
    Obtiene la lista de licitaciones.

    - **rubro**: Filtrar por rubro (opcional)
    - **estado**: Filtrar por estado (opcional)
    - **refresh**: Si es True, actualiza el scraper antes de retornar (opcional)
    """
    try:
        # Si se solicita refresh, ejecutar el scraper
        if refresh:
            logger.info("Refrescando licitaciones desde el sitio web")
            scraped = await scrape_licitaciones()

            # Cargar licitaciones existentes
            existing = load_licitaciones()

            # Combinar (evitar duplicados por ID)
            existing_ids = {lic["id"] for lic in existing}
            for lic in scraped:
                if lic["id"] not in existing_ids:
                    existing.append(lic)

            # Guardar
            save_licitaciones(existing)

        # Cargar licitaciones
        licitaciones = load_licitaciones()

        # Aplicar filtros
        if rubro:
            licitaciones = [lic for lic in licitaciones if lic.get("rubro", "").lower() == rubro.lower()]

        if estado:
            licitaciones = [lic for lic in licitaciones if lic.get("estado", "").lower() == estado.lower()]

        return licitaciones

    except Exception as e:
        logger.error(f"Error obteniendo licitaciones: {e}")
        raise HTTPException(status_code=500, detail={"error": "Error al obtener las licitaciones"})


@router.post("", response_model=Licitacion, status_code=201)
async def create_licitacion(
    licitacion: LicitacionCreate,
    x_admin_password: Optional[str] = Header(None)
):
    """
    Crea una nueva licitación (requiere autenticación admin).

    Debe incluir el header: X-Admin-Password
    """
    # Validar password de admin
    admin_password = os.getenv("ADMIN_PASSWORD")
    if not admin_password or x_admin_password != admin_password:
        raise HTTPException(status_code=401, detail={"error": "No autorizado"})

    try:
        # Cargar licitaciones existentes
        licitaciones = load_licitaciones()

        # Generar ID único
        new_id = f"LIC-{datetime.now().strftime('%Y%m%d%H%M%S')}"

        # Crear nueva licitación
        nueva_licitacion = {
            "id": new_id,
            "titulo": licitacion.titulo,
            "descripcion": licitacion.descripcion,
            "numero_expediente": licitacion.numero_expediente,
            "fecha_publicacion": datetime.now().strftime("%Y-%m-%d"),
            "fecha_apertura": licitacion.fecha_apertura,
            "presupuesto_oficial": licitacion.presupuesto_oficial,
            "rubro": licitacion.rubro,
            "estado": "abierta",
            "url_pliego": licitacion.url_pliego,
            "contacto": "licitacionesyconcursos@comodoro.gov.ar"
        }

        # Agregar y guardar
        licitaciones.append(nueva_licitacion)
        save_licitaciones(licitaciones)

        logger.info(f"Licitación creada: {new_id}")

        return nueva_licitacion

    except Exception as e:
        logger.error(f"Error creando licitación: {e}")
        raise HTTPException(status_code=500, detail={"error": "Error al crear la licitación"})
