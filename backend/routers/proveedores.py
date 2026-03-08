"""
Router para endpoints de proveedores.
GET /proveedores - Busca proveedores en el padrón municipal
GET /proveedores/me - Obtiene datos del proveedor autenticado (requiere JWT)
GET /proveedores/{cuit} - Obtiene datos de un proveedor por CUIT (requiere JWT)
"""

import logging
from pathlib import Path
from typing import Dict, List, Optional

import pandas as pd
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from middleware.auth import get_current_user

logger = logging.getLogger(__name__)

router = APIRouter()

# Path al CSV de proveedores
DATA_DIR = Path(__file__).parent.parent / "data"
PROVEEDORES_FILE = DATA_DIR / "proveedores.csv"


class Proveedor(BaseModel):
    """Modelo de un proveedor."""
    cuit: str
    razon_social: str
    localidad: str
    provincia: str
    rubro: Optional[str] = None
    whatsapp: Optional[str] = None


def load_proveedores_df() -> pd.DataFrame:
    """
    Carga el DataFrame de proveedores desde el CSV.
    Retorna un DataFrame vacío si el archivo no existe.
    """
    if not PROVEEDORES_FILE.exists():
        logger.warning(f"Archivo de proveedores no encontrado: {PROVEEDORES_FILE}")
        return pd.DataFrame(columns=["cuit", "razon_social", "localidad", "provincia", "rubro", "whatsapp"])

    try:
        # Forzar ciertos campos como string para evitar conversión automática
        dtype = {
            "cuit": str,
            "whatsapp": str
        }
        df = pd.read_csv(PROVEEDORES_FILE, encoding="utf-8", dtype=dtype)
        logger.info(f"Cargados {len(df)} proveedores desde CSV")
        return df
    except Exception as e:
        logger.error(f"Error cargando proveedores: {e}")
        return pd.DataFrame(columns=["cuit", "razon_social", "localidad", "provincia", "rubro", "whatsapp"])


@router.get("", response_model=List[Proveedor])
async def get_proveedores(
    rubro: Optional[str] = None,
    localidad: Optional[str] = None,
    provincia: Optional[str] = None,
    limit: int = 100
):
    """
    Busca proveedores en el padrón municipal.

    - **rubro**: Filtrar por rubro (ej: "limpieza", "construccion")
    - **localidad**: Filtrar por localidad
    - **provincia**: Filtrar por provincia
    - **limit**: Número máximo de resultados (default: 100, max: 500)
    """
    try:
        # Cargar proveedores
        df = load_proveedores_df()

        if df.empty:
            return []

        # Aplicar filtros
        if rubro:
            df = df[df["rubro"].str.contains(rubro, case=False, na=False)]

        if localidad:
            df = df[df["localidad"].str.contains(localidad, case=False, na=False)]

        if provincia:
            df = df[df["provincia"].str.contains(provincia, case=False, na=False)]

        # Limitar resultados (máximo 500)
        limit = min(limit, 500)
        df = df.head(limit)

        # Convertir a lista de diccionarios (fillna para manejar valores nulos)
        proveedores = df.fillna("").to_dict("records")

        logger.info(f"Retornando {len(proveedores)} proveedores")

        return proveedores

    except Exception as e:
        logger.error(f"Error buscando proveedores: {e}")
        raise HTTPException(status_code=500, detail={"error": "Error al buscar proveedores"})


@router.get("/search")
async def search_proveedores(q: str, limit: int = 50):
    """
    Búsqueda libre de proveedores por razón social o CUIT.

    - **q**: Término de búsqueda
    - **limit**: Número máximo de resultados (default: 50, max: 200)
    """
    if not q or len(q) < 3:
        raise HTTPException(status_code=400, detail={"error": "El término de búsqueda debe tener al menos 3 caracteres"})

    try:
        # Cargar proveedores
        df = load_proveedores_df()

        if df.empty:
            return []

        # Buscar en razón social o CUIT
        mask = (
            df["razon_social"].str.contains(q, case=False, na=False) |
            df["cuit"].str.contains(q, case=False, na=False)
        )
        df = df[mask]

        # Limitar resultados
        limit = min(limit, 200)
        df = df.head(limit)

        proveedores = df.fillna("").to_dict("records")

        logger.info(f"Búsqueda '{q}': {len(proveedores)} resultados")

        return proveedores

    except Exception as e:
        logger.error(f"Error en búsqueda de proveedores: {e}")
        raise HTTPException(status_code=500, detail={"error": "Error al buscar proveedores"})


@router.get("/me", response_model=Proveedor)
async def get_my_profile(current_user: Dict = Depends(get_current_user)):
    """
    Obtiene el perfil del proveedor autenticado.

    **Requiere autenticación JWT** (Header: Authorization: Bearer <token>)

    Retorna:
    - Datos completos del proveedor desde el CSV
    - Si el proveedor no está en el CSV, retorna datos básicos del JWT
    """
    cuit = current_user.get("cuit")

    try:
        # Buscar proveedor en CSV
        df = load_proveedores_df()

        if not df.empty:
            # Normalizar CUIT para búsqueda (remover guiones)
            cuit_normalized = cuit.replace("-", "").strip()
            df["cuit_normalized"] = df["cuit"].astype(str).str.replace("-", "").str.strip()

            result = df[df["cuit_normalized"] == cuit_normalized]

            if not result.empty:
                # Proveedor encontrado en CSV
                proveedor = result.iloc[0].fillna("").to_dict()
                logger.info(f"Perfil cargado desde CSV para CUIT {cuit}")
                return proveedor

        # Si no está en CSV, retornar datos del JWT
        logger.warning(f"Proveedor {cuit} no encontrado en CSV, retornando datos del JWT")
        return {
            "cuit": current_user.get("cuit"),
            "razon_social": current_user.get("nombre"),
            "localidad": "",
            "provincia": "",
            "rubro": current_user.get("rubro", ""),
            "whatsapp": current_user.get("whatsapp", "")
        }

    except Exception as e:
        logger.error(f"Error obteniendo perfil: {e}")
        raise HTTPException(status_code=500, detail={"error": "Error al obtener perfil"})


@router.get("/{cuit}", response_model=Proveedor)
async def get_proveedor_by_cuit(
    cuit: str,
    current_user: Dict = Depends(get_current_user)
):
    """
    Obtiene los datos de un proveedor específico por CUIT.

    **Requiere autenticación JWT** (Header: Authorization: Bearer <token>)

    Nota: Por ahora cualquier proveedor autenticado puede ver otros proveedores.
    En el futuro se puede restringir para que solo vean su propio perfil.

    Args:
        cuit: CUIT del proveedor a buscar (con o sin guiones)

    Returns:
        Datos del proveedor
    """
    try:
        df = load_proveedores_df()

        if df.empty:
            raise HTTPException(status_code=404, detail={"error": "No se encontró el proveedor"})

        # Normalizar CUITs
        cuit_normalized = cuit.replace("-", "").strip()
        df["cuit_normalized"] = df["cuit"].astype(str).str.replace("-", "").str.strip()

        result = df[df["cuit_normalized"] == cuit_normalized]

        if result.empty:
            raise HTTPException(status_code=404, detail={"error": f"Proveedor con CUIT {cuit} no encontrado"})

        proveedor = result.iloc[0].fillna("").to_dict()

        logger.info(f"Proveedor {cuit} consultado por {current_user.get('cuit')}")

        return proveedor

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error obteniendo proveedor {cuit}: {e}")
        raise HTTPException(status_code=500, detail={"error": "Error al obtener proveedor"})
