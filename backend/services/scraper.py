"""
Scraper para el sitio de licitaciones de la Municipalidad de Comodoro Rivadavia.
Target: https://www.comodoro.gov.ar/secciones/licitaciones/

Implementa retry con backoff exponencial según las convenciones del CLAUDE.md
"""

import asyncio
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional

import httpx
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

SCRAPER_URL = "https://www.comodoro.gov.ar/secciones/licitaciones/"
MAX_RETRIES = 3
RETRY_BACKOFF = 2  # segundos

# Path al archivo de salida
DATA_DIR = Path(__file__).parent.parent / "data"
OUTPUT_FILE = DATA_DIR / "licitaciones.json"


async def fetch_with_retry(url: str, retries: int = MAX_RETRIES) -> Optional[str]:
    """
    Realiza una petición HTTP con reintentos y backoff exponencial.

    Args:
        url: URL a consultar
        retries: Número máximo de reintentos

    Returns:
        Contenido HTML de la página o None si falla
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "es-AR,es;q=0.9,en;q=0.8",
    }

    async with httpx.AsyncClient(timeout=30.0, headers=headers) as client:
        for attempt in range(retries):
            try:
                logger.info(f"Intentando scraping: {url} (intento {attempt + 1}/{retries})")

                response = await client.get(url, follow_redirects=True)
                response.raise_for_status()

                logger.info(f"Scraping exitoso: {url}")
                return response.text

            except httpx.HTTPError as e:
                logger.warning(f"Error en intento {attempt + 1}: {e}")

                if attempt < retries - 1:
                    wait_time = RETRY_BACKOFF ** attempt
                    logger.info(f"Esperando {wait_time}s antes de reintentar...")
                    await asyncio.sleep(wait_time)
                else:
                    logger.error(f"Falló scraping después de {retries} intentos: {url}")
                    return None

    return None


def parse_licitacion(element) -> Optional[Dict]:
    """
    Parsea un elemento HTML de licitación y extrae la información.
    Adaptado para el sitio WordPress de comodoro.gov.ar

    Args:
        element: Elemento BeautifulSoup de la licitación (article)

    Returns:
        Diccionario con datos de la licitación o None si no se puede parsear
    """
    try:
        # Estructura WordPress:
        # <article>
        #   <div class="post_title">
        #     <h2><a href="...">Título</a></h2>
        #   </div>
        #   <ul class="post_meta">
        #     <li>fecha publicación</li>
        #   </ul>
        # </article>

        # Extraer título y URL
        titulo_elem = element.select_one(".post_title h2 a")
        if not titulo_elem:
            # Intentar selector alternativo
            titulo_elem = element.find("h2")
            if not titulo_elem:
                return None

        titulo = titulo_elem.get_text(strip=True)

        # Extraer URL de la licitación (enlace al post completo)
        url_detalle = None
        if titulo_elem.name == "a" and titulo_elem.get("href"):
            url_detalle = titulo_elem["href"]
        elif titulo_elem.find("a"):
            url_detalle = titulo_elem.find("a")["href"]

        # Si es URL relativa, completar con dominio
        if url_detalle and url_detalle.startswith("/"):
            url_detalle = f"https://www.comodoro.gov.ar{url_detalle}"

        # Extraer fecha de publicación
        fecha_publicacion = datetime.now().strftime("%Y-%m-%d")
        fecha_elem = element.select_one(".post_meta li")
        if fecha_elem:
            fecha_text = fecha_elem.get_text(strip=True)
            # Formato esperado: "día mes, año" (ej: "3 marzo, 2026")
            try:
                # Mapeo de meses en español
                meses = {
                    "enero": "01", "febrero": "02", "marzo": "03", "abril": "04",
                    "mayo": "05", "junio": "06", "julio": "07", "agosto": "08",
                    "septiembre": "09", "octubre": "10", "noviembre": "11", "diciembre": "12"
                }
                partes = fecha_text.replace(",", "").split()
                if len(partes) >= 3:
                    dia = partes[0].zfill(2)
                    mes = meses.get(partes[1].lower(), "01")
                    año = partes[2]
                    fecha_publicacion = f"{año}-{mes}-{dia}"
            except Exception as e:
                logger.warning(f"No se pudo parsear fecha: {fecha_text} - {e}")

        # Extraer número de licitación del título
        numero_expediente = None
        if "Nº" in titulo or "N°" in titulo:
            # Intentar extraer el número (ej: "Licitación Pública Nº 01/2026")
            import re
            match = re.search(r'N[ºo°]\s*(\d+/\d+)', titulo, re.IGNORECASE)
            if match:
                numero_expediente = match.group(1)

        # Determinar estado basado en el título o fecha
        estado = "abierta"
        titulo_lower = titulo.lower()
        if "finalizada" in titulo_lower or "cerrada" in titulo_lower:
            estado = "cerrada"

        # Generar ID único
        licitacion_id = f"SCRAPE-{abs(hash(titulo + fecha_publicacion))}"

        return {
            "id": licitacion_id,
            "titulo": titulo,
            "descripcion": titulo,  # En la vista de tarjetas no hay descripción detallada
            "numero_expediente": numero_expediente,
            "fecha_publicacion": fecha_publicacion,
            "fecha_apertura": "Ver detalle",  # Requiere entrar al post individual
            "presupuesto_oficial": None,
            "rubro": "general",
            "estado": estado,
            "url_pliego": url_detalle,  # URL al post completo
            "contacto": "licitacionesyconcursos@comodoro.gov.ar"
        }

    except Exception as e:
        logger.error(f"Error parseando licitación: {e}")
        return None


def save_licitaciones_to_file(licitaciones: List[Dict]) -> bool:
    """
    Guarda las licitaciones en el archivo JSON.

    Args:
        licitaciones: Lista de licitaciones a guardar

    Returns:
        True si se guardó exitosamente, False en caso contrario
    """
    try:
        # Crear directorio si no existe
        DATA_DIR.mkdir(parents=True, exist_ok=True)

        # Guardar con formato legible
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            json.dump(
                {"licitaciones": licitaciones},
                f,
                ensure_ascii=False,
                indent=2
            )

        logger.info(f"✓ Licitaciones guardadas en {OUTPUT_FILE}")
        return True

    except Exception as e:
        logger.error(f"Error guardando licitaciones en {OUTPUT_FILE}: {e}")
        return False


async def scrape_licitaciones(save_to_file: bool = True) -> List[Dict]:
    """
    Scrape del sitio de licitaciones de la municipalidad.

    Args:
        save_to_file: Si es True, guarda los resultados en licitaciones.json

    Returns:
        Lista de licitaciones encontradas
    """
    logger.info(f"Iniciando scraping de {SCRAPER_URL}")

    html = await fetch_with_retry(SCRAPER_URL)

    if not html:
        logger.error("No se pudo obtener contenido del sitio")
        return []

    try:
        soup = BeautifulSoup(html, "html.parser")

        # Buscar elementos de licitaciones (estructura WordPress)
        # El sitio usa <article> para cada post/licitación
        licitacion_elements = soup.find_all("article")

        if not licitacion_elements:
            logger.warning("No se encontraron licitaciones (artículos) en la página.")
            # Intentar selector más específico
            licitacion_elements = soup.select(".post-display-grid article")

        if not licitacion_elements:
            logger.warning("No se encontraron licitaciones con ningún selector. Verificar estructura del sitio.")
            return []

        logger.info(f"Se encontraron {len(licitacion_elements)} elementos article en la página")

        licitaciones = []
        for element in licitacion_elements:
            licitacion = parse_licitacion(element)
            if licitacion:
                licitaciones.append(licitacion)

        logger.info(f"Se parsearon exitosamente {len(licitaciones)} licitaciones")

        # Guardar en archivo si se solicita
        if save_to_file and licitaciones:
            save_licitaciones_to_file(licitaciones)

        return licitaciones

    except Exception as e:
        logger.error(f"Error durante el scraping: {e}")
        return []


async def main():
    """Función principal para ejecutar el scraper manualmente."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    licitaciones = await scrape_licitaciones(save_to_file=True)

    print(f"\n{'='*60}")
    print(f"SCRAPING COMPLETADO: {len(licitaciones)} licitaciones encontradas")
    print(f"Archivo guardado en: {OUTPUT_FILE}")
    print(f"{'='*60}\n")

    for lic in licitaciones:
        print(f"ID: {lic['id']}")
        print(f"Título: {lic['titulo']}")
        print(f"Estado: {lic['estado']}")
        print(f"Fecha publicación: {lic['fecha_publicacion']}")
        print(f"URL: {lic['url_pliego']}")
        print("-" * 60)


if __name__ == "__main__":
    asyncio.run(main())
