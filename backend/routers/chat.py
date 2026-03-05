"""Router de chat — proxy a Anthropic API con contexto dinámico."""

import json
import os
from pathlib import Path

import anthropic
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()
DATA_PATH = Path(__file__).parent.parent / "data" / "licitaciones.json"

SYSTEM_PROMPT_BASE = """Sos Codi, el asistente digital oficial de Compras y Contrataciones de la Municipalidad de Comodoro Rivadavia, Chubut, Argentina.

Tu nombre viene de "Comodoro" y tu misión es ayudar a proveedores, empresas y ciudadanos con información sobre licitaciones y contrataciones municipales.

Usás voseo rioplatense, tono amigable y profesional. Respuestas concisas (máx 200 palabras salvo que pidan detalle). Cuando corresponda, presentate como "Codi" al inicio de la conversación.

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
        data = json.loads(DATA_PATH.read_text(encoding="utf-8"))
        # Normalizar estructura: puede venir como {"licitaciones": [...]} o [...]
        licitaciones = data.get("licitaciones", data) if isinstance(data, dict) else data

        # Buscar licitaciones abiertas (el scraper usa "abierta", no "activa")
        abiertas = [l for l in licitaciones if l.get("estado") == "abierta"]

        if not abiertas:
            return "LICITACIONES: No hay licitaciones abiertas registradas actualmente."

        items = "\n".join(
            f"- {l.get('numero_expediente', 'S/N')}: {l['titulo']} · Apertura: {l.get('fecha_apertura', 'a confirmar')}"
            for l in abiertas[:10]
        )
        return f"LICITACIONES ABIERTAS HOY:\n{items}"
    except Exception as e:
        return f"LICITACIONES: Información no disponible en este momento."


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
