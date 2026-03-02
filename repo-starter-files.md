## ESTRUCTURA COMPLETA DEL REPO — ARCHIVOS INICIALES
## Copiar cada sección a su ruta correspondiente

════════════════════════════════════════════════════════
ARCHIVO: backend/main.py
════════════════════════════════════════════════════════

```python
"""
Asistente de Compras · Municipalidad de Comodoro Rivadavia
Backend FastAPI — Entry point
"""

import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import os

from backend.routers import licitaciones, proveedores, notificaciones, chat
from backend.services.scraper import run_scraper

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Ejecuta el scraper al arrancar el servidor."""
    logger.info("Iniciando backend — corriendo scraper inicial...")
    try:
        await run_scraper()
        logger.info("Scraper completado al iniciar.")
    except Exception as e:
        logger.warning(f"Scraper falló al iniciar (usando cache): {e}")
    yield


app = FastAPI(
    title="Asistente de Compras — Comodoro Rivadavia",
    description="API para el chatbot municipal de compras y contrataciones",
    version="0.1.0",
    lifespan=lifespan,
)

# CORS — el frontend en Vercel necesita acceder
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "http://localhost:3000,http://127.0.0.1:5500").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(licitaciones.router, prefix="/licitaciones", tags=["Licitaciones"])
app.include_router(proveedores.router, prefix="/proveedores", tags=["Proveedores"])
app.include_router(notificaciones.router, prefix="/notificar", tags=["Notificaciones"])
app.include_router(chat.router, prefix="/chat", tags=["Chat IA"])


@app.get("/")
async def root():
    return {"status": "ok", "servicio": "Asistente de Compras · Comodoro Rivadavia"}


@app.get("/health")
async def health():
    return {"status": "healthy"}
```

════════════════════════════════════════════════════════
ARCHIVO: backend/routers/licitaciones.py
════════════════════════════════════════════════════════

```python
"""Router de licitaciones — GET para consultar, POST para crear (admin)."""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Optional

from fastapi import APIRouter, HTTPException, Header
from pydantic import BaseModel

router = APIRouter()
DATA_PATH = Path(__file__).parent.parent / "data" / "licitaciones.json"
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "comodoro2025")


class LicitacionCreate(BaseModel):
    titulo: str
    numero: str
    rubro: str
    descripcion: str
    fecha_apertura: str  # ISO format: "2026-02-15"
    rubros_notificar: list[str] = []


def _load() -> list[dict]:
    if not DATA_PATH.exists():
        return []
    return json.loads(DATA_PATH.read_text(encoding="utf-8"))


def _save(data: list[dict]):
    DATA_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


@router.get("/")
async def get_licitaciones(estado: Optional[str] = None):
    """Retorna todas las licitaciones. Filtrar por estado: activa | cerrada."""
    licitaciones = _load()
    if estado:
        licitaciones = [l for l in licitaciones if l.get("estado") == estado]
    return {"licitaciones": licitaciones, "total": len(licitaciones)}


@router.get("/{numero}")
async def get_licitacion(numero: str):
    licitaciones = _load()
    match = next((l for l in licitaciones if l["numero"] == numero), None)
    if not match:
        raise HTTPException(status_code=404, detail=f"Licitación {numero} no encontrada")
    return match


@router.post("/", status_code=201)
async def crear_licitacion(
    licitacion: LicitacionCreate,
    x_admin_password: str = Header(..., alias="X-Admin-Password"),
):
    """Crear nueva licitación (requiere header X-Admin-Password)."""
    if x_admin_password != ADMIN_PASSWORD:
        raise HTTPException(status_code=403, detail="Contraseña de administrador incorrecta")

    licitaciones = _load()
    nueva = {
        **licitacion.model_dump(),
        "estado": "activa",
        "fecha_publicacion": datetime.now().isoformat()[:10],
        "url": f"https://www.comodoro.gov.ar/licitaciones/{licitacion.numero.lower().replace('/', '-')}",
    }
    licitaciones.append(nueva)
    _save(licitaciones)
    return {"mensaje": "Licitación creada exitosamente", "licitacion": nueva}
```

════════════════════════════════════════════════════════
ARCHIVO: backend/routers/proveedores.py
════════════════════════════════════════════════════════

```python
"""Router de proveedores — búsqueda en el CSV municipal."""

from fastapi import APIRouter, Query
from backend.services.proveedores_service import buscar_proveedores, get_stats

router = APIRouter()


@router.get("/")
async def search_proveedores(
    rubro: str = Query(..., description="Keyword de búsqueda. Ej: limpieza, construccion, IT"),
    localidad: str = Query(default="", description="Filtrar por localidad. Ej: Comodoro Rivadavia"),
    limit: int = Query(default=20, le=100),
):
    """Busca proveedores del padrón municipal por rubro y/o localidad."""
    resultados = buscar_proveedores(rubro=rubro, localidad=localidad, limit=limit)
    return {
        "query": {"rubro": rubro, "localidad": localidad},
        "total": len(resultados),
        "proveedores": resultados,
    }


@router.get("/stats")
async def get_proveedores_stats():
    """Estadísticas del padrón: total, localidades, etc."""
    return get_stats()
```

════════════════════════════════════════════════════════
ARCHIVO: backend/routers/chat.py
════════════════════════════════════════════════════════

```python
"""Router de chat — proxy a Anthropic API con contexto dinámico."""

import json
import os
from pathlib import Path

import anthropic
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()
DATA_PATH = Path(__file__).parent.parent / "data" / "licitaciones.json"

SYSTEM_PROMPT_BASE = """Sos el asistente digital oficial de Compras y Contrataciones de la Municipalidad de Comodoro Rivadavia, Chubut, Argentina.

Usás voseo rioplatense, tono amigable y profesional. Respuestas concisas (máx 200 palabras salvo que pidan detalle).

CONOCIMIENTO BASE:
- Inscripción de proveedores: ARCA/Monotributo, IIBB, CBU, habilitación. Email: controldocumentalyproveedores@comodoro.gov.ar | WhatsApp: 2975819952
- Tipos: Licitación Pública (abierta), Privada (invitados), Directa (montos menores), Subasta Pública
- Proceso: 1) Obtener pliego en Namuncurá 26 o licitacionesyconcursos@comodoro.gov.ar 2) Leer PBCG + PBCP 3) Sobre cerrado antes de la hora de apertura
- Normativa: Ley II N°76 (contrataciones), Ley N°4829 (Compre Chubut — preferencia proveedores locales)
- Contacto: licitacionesyconcursos@comodoro.gov.ar · Namuncurá 26 · días hábiles hasta 12:00 hs del día anterior a apertura

{licitaciones_activas}

Si no sabés algo con certeza, referí al contacto oficial. No inventés información normativa."""


def _get_licitaciones_context() -> str:
    try:
        licitaciones = json.loads(DATA_PATH.read_text(encoding="utf-8"))
        activas = [l for l in licitaciones if l.get("estado") == "activa"]
        if not activas:
            return "LICITACIONES: No hay licitaciones activas registradas actualmente."
        items = "\n".join(
            f"- LP {l['numero']}: {l['titulo']} · Apertura: {l.get('fecha_apertura', 'a confirmar')}"
            for l in activas[:10]
        )
        return f"LICITACIONES ACTIVAS HOY:\n{items}"
    except Exception:
        return "LICITACIONES: Información no disponible en este momento."


class ChatMessage(BaseModel):
    role: str  # "user" | "assistant"
    content: str


class ChatRequest(BaseModel):
    messages: list[ChatMessage]


@router.post("/")
async def chat(request: ChatRequest):
    """Proxy a Anthropic API con contexto dinámico de licitaciones."""
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="ANTHROPIC_API_KEY no configurada en el servidor")

    system = SYSTEM_PROMPT_BASE.format(licitaciones_activas=_get_licitaciones_context())
    client = anthropic.Anthropic(api_key=api_key)

    try:
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=700,
            system=system,
            messages=[{"role": m.role, "content": m.content} for m in request.messages],
        )
        return {"content": response.content[0].text, "usage": response.usage.model_dump()}
    except anthropic.APIError as e:
        raise HTTPException(status_code=502, detail=f"Error de Anthropic API: {str(e)}")
```

════════════════════════════════════════════════════════
ARCHIVO: backend/routers/notificaciones.py
════════════════════════════════════════════════════════

```python
"""Router de notificaciones — dispara WhatsApp a proveedores por rubro."""

import json
import logging
import os
from datetime import datetime
from pathlib import Path

from fastapi import APIRouter, Header, HTTPException
from pydantic import BaseModel

from backend.services.proveedores_service import buscar_proveedores
from backend.services.whatsapp import enviar_whatsapp

router = APIRouter()
logger = logging.getLogger(__name__)
LOG_PATH = Path(__file__).parent.parent / "data" / "notif-log.json"
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "comodoro2025")


class NotificacionRequest(BaseModel):
    numero_licitacion: str
    titulo: str
    rubro: str
    fecha_apertura: str
    url: str = ""


@router.post("/")
async def notificar_proveedores(
    req: NotificacionRequest,
    x_admin_password: str = Header(..., alias="X-Admin-Password"),
):
    """Envía WhatsApp a todos los proveedores del rubro especificado."""
    if x_admin_password != ADMIN_PASSWORD:
        raise HTTPException(status_code=403, detail="Contraseña incorrecta")

    proveedores = buscar_proveedores(rubro=req.rubro, localidad="", limit=500)
    con_whatsapp = [p for p in proveedores if p.get("whatsapp")]

    if not con_whatsapp:
        return {
            "enviados": 0,
            "mensaje": f"No hay proveedores con WhatsApp registrado para el rubro '{req.rubro}'",
        }

    mensaje = (
        f"📢 *Nueva licitación municipal*\n\n"
        f"*{req.titulo}* (Nº {req.numero_licitacion})\n"
        f"📅 Apertura: {req.fecha_apertura}\n"
        f"🔗 Ver pliego: {req.url or 'https://www.comodoro.gov.ar/secciones/licitaciones/'}\n\n"
        f"Consultas: licitacionesyconcursos@comodoro.gov.ar\n"
        f"Respondé este mensaje para más información."
    )

    enviados, fallidos = 0, 0
    for proveedor in con_whatsapp:
        ok = await enviar_whatsapp(numero=proveedor["whatsapp"], mensaje=mensaje)
        if ok:
            enviados += 1
        else:
            fallidos += 1

    # Log
    _log_notificacion(req, enviados, fallidos)

    return {
        "licitacion": req.numero_licitacion,
        "rubro": req.rubro,
        "proveedores_encontrados": len(con_whatsapp),
        "enviados": enviados,
        "fallidos": fallidos,
    }


def _log_notificacion(req: NotificacionRequest, enviados: int, fallidos: int):
    log = []
    if LOG_PATH.exists():
        log = json.loads(LOG_PATH.read_text(encoding="utf-8"))
    log.append({
        "timestamp": datetime.now().isoformat(),
        "licitacion": req.numero_licitacion,
        "rubro": req.rubro,
        "enviados": enviados,
        "fallidos": fallidos,
    })
    LOG_PATH.write_text(json.dumps(log, ensure_ascii=False, indent=2), encoding="utf-8")
```

════════════════════════════════════════════════════════
ARCHIVO: backend/services/scraper.py
════════════════════════════════════════════════════════

```python
"""Scraper de licitaciones de comodoro.gov.ar."""

import json
import logging
from datetime import datetime
from pathlib import Path

import httpx
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)
BASE_URL = "https://www.comodoro.gov.ar/secciones/licitaciones/"
DATA_PATH = Path(__file__).parent.parent / "data" / "licitaciones.json"


async def run_scraper() -> list[dict]:
    """Scrapea el sitio y actualiza licitaciones.json. Retorna la lista resultante."""
    logger.info(f"Scrapeando: {BASE_URL}")
    try:
        async with httpx.AsyncClient(timeout=15, follow_redirects=True) as client:
            resp = await client.get(BASE_URL)
            resp.raise_for_status()
    except httpx.HTTPError as e:
        logger.error(f"Error HTTP al scrapear: {e}")
        return _load_cached()

    soup = BeautifulSoup(resp.text, "html.parser")
    licitaciones = _parse(soup)

    # Merge con licitaciones manuales (creadas desde el admin)
    cached = _load_cached()
    manuales = [l for l in cached if l.get("origen") == "manual"]
    merged = {l["numero"]: l for l in licitaciones}
    for m in manuales:
        if m["numero"] not in merged:
            merged[m["numero"]] = m

    result = list(merged.values())
    DATA_PATH.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    logger.info(f"Scraper OK: {len(licitaciones)} del sitio + {len(manuales)} manuales")
    return result


def _parse(soup: BeautifulSoup) -> list[dict]:
    """Extrae licitaciones del HTML del sitio municipal."""
    licitaciones = []
    # El sitio usa posts de WordPress — buscar por artículos o lista
    articles = soup.find_all("article") or soup.find_all("li", class_=lambda c: c and "licitacion" in c.lower())

    for article in articles:
        titulo_tag = article.find(["h1", "h2", "h3", "a"])
        if not titulo_tag:
            continue
        titulo = titulo_tag.get_text(strip=True)
        if not titulo:
            continue

        # Inferir estado desde el título (el sitio pone "(finalizada)" o "(Finalizado)")
        titulo_lower = titulo.lower()
        estado = "cerrada" if any(w in titulo_lower for w in ["finalizada", "finalizado", "cerrada"]) else "activa"

        # Limpiar título
        titulo_limpio = titulo.replace("(finalizada)", "").replace("(Finalizado)", "").replace("(finalizado)", "").strip()

        # Extraer número de licitación del título
        import re
        num_match = re.search(r"N[°ºo]?\s*(\d+/\d+)", titulo, re.IGNORECASE)
        numero = num_match.group(1) if num_match else f"SN-{len(licitaciones)+1}"

        # Fecha de publicación
        fecha_tag = article.find("time") or article.find(class_=lambda c: c and "date" in str(c).lower())
        fecha = fecha_tag.get("datetime", fecha_tag.get_text(strip=True))[:10] if fecha_tag else datetime.now().isoformat()[:10]

        # URL del artículo
        link_tag = article.find("a", href=True)
        url = link_tag["href"] if link_tag else BASE_URL

        licitaciones.append({
            "numero": numero,
            "titulo": titulo_limpio,
            "estado": estado,
            "fecha_publicacion": fecha,
            "fecha_apertura": "",
            "descripcion": "",
            "url": url,
            "origen": "scraper",
        })

    return licitaciones


def _load_cached() -> list[dict]:
    if DATA_PATH.exists():
        return json.loads(DATA_PATH.read_text(encoding="utf-8"))
    return []
```

════════════════════════════════════════════════════════
ARCHIVO: backend/services/proveedores_service.py
════════════════════════════════════════════════════════

```python
"""Servicio de búsqueda en el CSV de proveedores municipales."""

import logging
from functools import lru_cache
from pathlib import Path

import pandas as pd

logger = logging.getLogger(__name__)
CSV_PATH = Path(__file__).parent.parent / "data" / "proveedores.csv"


@lru_cache(maxsize=1)
def _load_df() -> pd.DataFrame:
    """Carga el CSV una sola vez y lo cachea en memoria."""
    df = pd.read_csv(CSV_PATH, dtype=str).fillna("")
    # Normalizar nombres de columnas
    df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]
    logger.info(f"CSV cargado: {len(df)} proveedores")
    return df


def buscar_proveedores(rubro: str, localidad: str = "", limit: int = 20) -> list[dict]:
    """
    Busca proveedores por rubro (keyword en razón social o nombre fantasía)
    y opcionalmente filtra por localidad.
    """
    df = _load_df().copy()
    rubro_lower = rubro.lower()

    # Búsqueda en razón social y nombre fantasía
    mask = (
        df.get("razon_social", pd.Series(dtype=str)).str.lower().str.contains(rubro_lower, na=False)
        | df.get("nombre_fantasia", pd.Series(dtype=str)).str.lower().str.contains(rubro_lower, na=False)
    )
    resultado = df[mask]

    if localidad:
        localidad_lower = localidad.lower()
        resultado = resultado[
            resultado.get("localidad", pd.Series(dtype=str)).str.lower().str.contains(localidad_lower, na=False)
        ]

    return resultado.head(limit).to_dict(orient="records")


def get_stats() -> dict:
    df = _load_df()
    localidades = df.get("localidad", pd.Series(dtype=str)).value_counts().head(10).to_dict()
    return {
        "total_proveedores": len(df),
        "top_localidades": localidades,
    }
```

════════════════════════════════════════════════════════
ARCHIVO: backend/services/whatsapp.py
════════════════════════════════════════════════════════

```python
"""Wrapper de Twilio para envío de mensajes WhatsApp."""

import logging
import os

from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException

logger = logging.getLogger(__name__)


async def enviar_whatsapp(numero: str, mensaje: str) -> bool:
    """
    Envía un mensaje WhatsApp al número dado via Twilio.
    número debe incluir código de país, ej: '+5492975123456'
    Retorna True si fue exitoso, False si falló.
    """
    account_sid = os.getenv("TWILIO_ACCOUNT_SID")
    auth_token = os.getenv("TWILIO_AUTH_TOKEN")
    from_number = os.getenv("TWILIO_WHATSAPP_FROM", "whatsapp:+14155238886")

    if not account_sid or not auth_token:
        logger.warning("Twilio no configurado — saltando envío de WhatsApp")
        return False

    to_number = f"whatsapp:{numero}" if not numero.startswith("whatsapp:") else numero

    try:
        client = Client(account_sid, auth_token)
        message = client.messages.create(
            body=mensaje,
            from_=from_number,
            to=to_number,
        )
        logger.info(f"WhatsApp enviado a {numero}: SID {message.sid}")
        return True
    except TwilioRestException as e:
        logger.error(f"Error Twilio al enviar a {numero}: {e}")
        return False
```

════════════════════════════════════════════════════════
ARCHIVO: backend/requirements.txt
════════════════════════════════════════════════════════

```
fastapi==0.115.6
uvicorn[standard]==0.32.1
anthropic==0.40.0
httpx==0.28.1
beautifulsoup4==4.12.3
pandas==2.2.3
twilio==9.3.7
python-dotenv==1.0.1
pydantic==2.10.3
```

════════════════════════════════════════════════════════
ARCHIVO: backend/.env.example
════════════════════════════════════════════════════════

```
# Copiar a .env y completar con valores reales
# NUNCA commitear el .env real

ANTHROPIC_API_KEY=sk-ant-api03-XXXXXXXX
TWILIO_ACCOUNT_SID=ACXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
TWILIO_AUTH_TOKEN=your_auth_token_here
TWILIO_WHATSAPP_FROM=whatsapp:+14155238886
ADMIN_PASSWORD=comodoro2025
CORS_ORIGINS=https://comodoro-asistente.vercel.app,http://localhost:3000
```

════════════════════════════════════════════════════════
ARCHIVO: backend/tests/test_proveedores.py
════════════════════════════════════════════════════════

```python
"""Tests básicos del servicio de proveedores."""

import pytest
from backend.services.proveedores_service import buscar_proveedores, get_stats


def test_csv_carga():
    stats = get_stats()
    assert stats["total_proveedores"] > 0, "El CSV debe tener al menos 1 proveedor"


def test_busqueda_retorna_resultados():
    resultados = buscar_proveedores(rubro="srl")
    assert len(resultados) > 0, "Buscar 'srl' debe retornar resultados"


def test_busqueda_con_localidad():
    resultados = buscar_proveedores(rubro="", localidad="Comodoro")
    assert len(resultados) > 0


def test_limite_resultados():
    resultados = buscar_proveedores(rubro="a", limit=5)
    assert len(resultados) <= 5


def test_sin_resultados_keyword_inexistente():
    resultados = buscar_proveedores(rubro="zzzzzzzzz_inexistente_xyz")
    assert len(resultados) == 0
```

════════════════════════════════════════════════════════
ARCHIVO: .github/workflows/deploy.yml
════════════════════════════════════════════════════════

```yaml
name: CI/CD — Tests + Deploy

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test-backend:
    name: Tests Backend (Python)
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Python 3.11
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"
          cache: "pip"

      - name: Install dependencies
        run: |
          cd backend
          pip install -r requirements.txt
          pip install pytest pytest-asyncio

      - name: Run tests
        run: |
          cd backend
          pytest tests/ -v
        env:
          # Tests no necesitan credenciales reales
          ANTHROPIC_API_KEY: "sk-ant-test"
          TWILIO_ACCOUNT_SID: "test"
          TWILIO_AUTH_TOKEN: "test"

  deploy-frontend:
    name: Deploy Frontend (Vercel)
    needs: test-backend
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    steps:
      - uses: actions/checkout@v4
      - name: Deploy a Vercel
        uses: amondnet/vercel-action@v25
        with:
          vercel-token: ${{ secrets.VERCEL_TOKEN }}
          vercel-org-id: ${{ secrets.VERCEL_ORG_ID }}
          vercel-project-id: ${{ secrets.VERCEL_PROJECT_ID }}
          vercel-args: "--prod"
```

════════════════════════════════════════════════════════
ARCHIVO: vercel.json
════════════════════════════════════════════════════════

```json
{
  "version": 2,
  "builds": [
    { "src": "index.html", "use": "@vercel/static" },
    { "src": "admin.html", "use": "@vercel/static" }
  ],
  "routes": [
    { "src": "/admin", "dest": "/admin.html" },
    { "src": "/(.*)", "dest": "/$1" }
  ]
}
```

════════════════════════════════════════════════════════
ARCHIVO: .gitignore
════════════════════════════════════════════════════════

```
# Python
__pycache__/
*.py[cod]
*.pyo
.venv/
venv/
env/
*.egg-info/
dist/
.pytest_cache/

# Env
.env
.env.local
*.env

# Data (el CSV va al repo, los logs no)
backend/data/notif-log.json
backend/data/licitaciones.json

# Node (si se agrega algún script JS)
node_modules/
.npm/

# IDE
.vscode/
.idea/
*.swp
*.DS_Store

# Vercel
.vercel/
```
