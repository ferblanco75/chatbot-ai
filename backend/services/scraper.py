"""
Scraper para el sitio de licitaciones de la Municipalidad de Comodoro Rivadavia.
Target: https://www.comodoro.gov.ar/secciones/licitaciones/

Implementa retry con backoff exponencial según las convenciones del CLAUDE.md
"""

import asyncio
import logging
from datetime import datetime
from typing import List, Dict, Optional

import httpx
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

SCRAPER_URL = "https://www.comodoro.gov.ar/secciones/licitaciones/"
MAX_RETRIES = 3
RETRY_BACKOFF = 2  # segundos


async def fetch_with_retry(url: str, retries: int = MAX_RETRIES) -> Optional[str]:
    """
    Realiza una petición HTTP con reintentos y backoff exponencial.

    Args:
        url: URL a consultar
        retries: Número máximo de reintentos

    Returns:
        Contenido HTML de la página o None si falla
    """
    async with httpx.AsyncClient(timeout=30.0) as client:
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

    Args:
        element: Elemento BeautifulSoup de la licitación

    Returns:
        Diccionario con datos de la licitación o None si no se puede parsear
    """
    try:
        # Este es un ejemplo genérico - debe adaptarse al HTML real del sitio
        # Estructura esperada (ajustar según el HTML real):
        # <div class="licitacion">
        #   <h3>Título de la licitación</h3>
        #   <p class="expediente">Expte: 123/2025</p>
        #   <p class="fecha">Fecha apertura: 15/03/2025</p>
        #   <a href="/pliegos/123.pdf">Ver pliego</a>
        # </div>

        titulo_elem = element.find("h3")
        if not titulo_elem:
            return None

        titulo = titulo_elem.get_text(strip=True)

        # Extraer número de expediente
        expediente_elem = element.find(class_="expediente")
        expediente = expediente_elem.get_text(strip=True) if expediente_elem else None

        # Extraer fecha de apertura
        fecha_elem = element.find(class_="fecha")
        fecha_apertura = None
        if fecha_elem:
            fecha_text = fecha_elem.get_text(strip=True)
            # Intentar parsear fecha (formato esperado: "Fecha apertura: DD/MM/YYYY")
            try:
                if ":" in fecha_text:
                    fecha_str = fecha_text.split(":")[-1].strip()
                    fecha_apertura = datetime.strptime(fecha_str, "%d/%m/%Y").strftime("%Y-%m-%d")
            except ValueError:
                logger.warning(f"No se pudo parsear fecha: {fecha_text}")

        # Extraer URL del pliego
        pliego_elem = element.find("a", href=True)
        url_pliego = None
        if pliego_elem and pliego_elem["href"]:
            href = pliego_elem["href"]
            # Si es URL relativa, completar con dominio
            if href.startswith("/"):
                url_pliego = f"https://www.comodoro.gov.ar{href}"
            else:
                url_pliego = href

        # Extraer descripción (si existe)
        descripcion_elem = element.find("p", class_="descripcion")
        descripcion = descripcion_elem.get_text(strip=True) if descripcion_elem else titulo

        # Generar ID único basado en título y fecha
        licitacion_id = f"SCRAPE-{abs(hash(titulo + str(fecha_apertura)))}"

        return {
            "id": licitacion_id,
            "titulo": titulo,
            "descripcion": descripcion,
            "numero_expediente": expediente,
            "fecha_publicacion": datetime.now().strftime("%Y-%m-%d"),
            "fecha_apertura": fecha_apertura or "No especificada",
            "presupuesto_oficial": None,
            "rubro": "general",
            "estado": "abierta",
            "url_pliego": url_pliego,
            "contacto": "licitacionesyconcursos@comodoro.gov.ar"
        }

    except Exception as e:
        logger.error(f"Error parseando licitación: {e}")
        return None


async def scrape_licitaciones() -> List[Dict]:
    """
    Scrape del sitio de licitaciones de la municipalidad.

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

        # Buscar elementos de licitaciones
        # NOTA: Ajustar el selector según la estructura real del sitio
        licitacion_elements = soup.find_all("div", class_="licitacion")

        if not licitacion_elements:
            # Intentar selectores alternativos
            licitacion_elements = soup.find_all("article", class_="licitacion")

        if not licitacion_elements:
            logger.warning("No se encontraron licitaciones en la página. Verificar selectores CSS.")
            return []

        licitaciones = []
        for element in licitacion_elements:
            licitacion = parse_licitacion(element)
            if licitacion:
                licitaciones.append(licitacion)

        logger.info(f"Se encontraron {len(licitaciones)} licitaciones")

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

    licitaciones = await scrape_licitaciones()

    print(f"\n{'='*60}")
    print(f"SCRAPING COMPLETADO: {len(licitaciones)} licitaciones encontradas")
    print(f"{'='*60}\n")

    for lic in licitaciones:
        print(f"ID: {lic['id']}")
        print(f"Título: {lic['titulo']}")
        print(f"Fecha apertura: {lic['fecha_apertura']}")
        print(f"URL pliego: {lic['url_pliego']}")
        print("-" * 60)


if __name__ == "__main__":
    asyncio.run(main())
