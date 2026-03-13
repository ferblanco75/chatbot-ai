"""Router de chat — proxy a Anthropic API con contexto dinámico y streaming SSE."""

import json
import os
from pathlib import Path
from typing import Optional, AsyncIterator

import anthropic
from fastapi import APIRouter, HTTPException, Depends, Request
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from middleware.auth import get_optional_user
from middleware.rate_limit import limiter

router = APIRouter()
DATA_DIR = Path(__file__).parent.parent / "data"
DATA_PATH = DATA_DIR / "licitaciones.json"
KNOWLEDGE_INSCRIPCION_PATH = DATA_DIR / "knowledge_inscripcion.md"
KNOWLEDGE_LICITACIONES_PATH = DATA_DIR / "knowledge_licitaciones.md"

SYSTEM_PROMPT_BASE = """Sos Codi, el asistente digital oficial de Compras y Contrataciones de la Municipalidad de Comodoro Rivadavia, Chubut, Argentina.

Tu nombre viene de "Comodoro" y tu misión es ayudar a proveedores, empresas y ciudadanos con información sobre licitaciones y contrataciones municipales.

Usás voseo rioplatense, tono amigable y profesional. Respuestas concisas (máx 300 palabras salvo que pidan detalle). Cuando corresponda, presentate como "Codi" al inicio de la conversación. Si el usuario pregunta por un proceso paso a paso, guialo en pasos numerados y claros.

{conocimiento_inscripcion}

{conocimiento_licitaciones}

{licitaciones_activas}

Si no sabés algo con certeza, referí al contacto oficial. No inventés información normativa."""


def _get_knowledge_context(path: Path) -> str:
    """Carga un archivo de knowledge base y lo retorna como string."""
    try:
        return path.read_text(encoding="utf-8")
    except Exception:
        return ""


def _get_licitaciones_context(rubro_proveedor: Optional[str] = None) -> str:
    """
    Genera contexto de licitaciones activas para inyectar en el system prompt.

    Args:
        rubro_proveedor: Rubro del proveedor autenticado (opcional).
                        Por ahora todas las licitaciones tienen rubro "general",
                        pero preparamos el código para cuando estén clasificadas.

    Returns:
        String formateado con licitaciones abiertas.
    """
    try:
        data = json.loads(DATA_PATH.read_text(encoding="utf-8"))
        # Normalizar estructura: puede venir como {"licitaciones": [...]} o [...]
        licitaciones = data.get("licitaciones", data) if isinstance(data, dict) else data

        # Buscar licitaciones abiertas (el scraper usa "abierta", no "activa")
        abiertas = [l for l in licitaciones if l.get("estado") == "abierta"]

        if not abiertas:
            return "LICITACIONES: No hay licitaciones abiertas registradas actualmente."

        # TODO: Cuando las licitaciones tengan rubros específicos, filtrar compatibles primero
        # Por ahora todas tienen rubro "general", así que mostramos todas

        items = "\n".join(
            f"- {l.get('numero_expediente', 'S/N')}: {l['titulo']} · Apertura: {l.get('fecha_apertura', 'a confirmar')}"
            for l in abiertas[:10]
        )

        header = "LICITACIONES ABIERTAS HOY"
        if rubro_proveedor:
            header += f" (tu rubro: {rubro_proveedor})"

        return f"{header}:\n{items}"
    except Exception as e:
        return f"LICITACIONES: Información no disponible en este momento."


class ChatMessage(BaseModel):
    role: str  # "user" | "assistant"
    content: str


class ChatRequest(BaseModel):
    messages: list[ChatMessage]


@router.post("/")
@limiter.limit("20/minute")  # Máximo 20 mensajes por minuto
async def chat(
    http_request: Request,
    request: ChatRequest,
    current_user: Optional[dict] = Depends(get_optional_user)
):
    """
    Proxy a Anthropic API con contexto dinámico y streaming SSE.

    - Si hay JWT, inyecta contexto del proveedor en el system prompt.
    - Retorna streaming SSE para respuestas en tiempo real.
    """
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="ANTHROPIC_API_KEY no configurada en el servidor")

    # Cargar knowledge bases
    conocimiento_inscripcion = _get_knowledge_context(KNOWLEDGE_INSCRIPCION_PATH)
    conocimiento_licitaciones = _get_knowledge_context(KNOWLEDGE_LICITACIONES_PATH)

    # Construir context de licitaciones (con rubro si hay usuario autenticado)
    rubro_proveedor = current_user.get('rubro') if current_user else None
    licitaciones_context = _get_licitaciones_context(rubro_proveedor=rubro_proveedor)

    # Construir contexto del proveedor si está autenticado
    contexto_proveedor = ""
    if current_user:
        contexto_proveedor = f"""

CONTEXTO DEL PROVEEDOR AUTENTICADO:
- CUIT: {current_user.get('cuit')}
- Razón social: {current_user.get('nombre')}
- Rubro: {current_user.get('rubro')}

Tené en cuenta el rubro del proveedor al recomendar licitaciones compatibles."""

    # System prompt completo
    system = SYSTEM_PROMPT_BASE.format(
        conocimiento_inscripcion=conocimiento_inscripcion,
        conocimiento_licitaciones=conocimiento_licitaciones,
        licitaciones_activas=licitaciones_context,
    ) + contexto_proveedor

    client = anthropic.Anthropic(api_key=api_key)

    try:
        # Generator para streaming SSE
        async def generate_stream() -> AsyncIterator[str]:
            with client.messages.stream(
                model="claude-sonnet-4-20250514",
                max_tokens=700,
                system=system,
                messages=[{"role": m.role, "content": m.content} for m in request.messages],
            ) as stream:
                for text in stream.text_stream:
                    yield f"data: {json.dumps({'content': text})}\n\n"

            yield "data: [DONE]\n\n"

        return StreamingResponse(generate_stream(), media_type="text/event-stream")

    except anthropic.APIError as e:
        raise HTTPException(status_code=502, detail=f"Error de Anthropic API: {str(e)}")
