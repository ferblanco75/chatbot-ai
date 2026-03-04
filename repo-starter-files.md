## ARCHIVOS NUEVOS DEL PORTAL — Sprint 4–5
## Estos archivos se suman a los existentes del Sprint 1–3

════════════════════════════════════════════════════════
ARCHIVO: backend/routers/auth.py
════════════════════════════════════════════════════════

```python
"""
Router de autenticación — OTP por WhatsApp + JWT.
POST /auth/request-code  → genera y envía código OTP
POST /auth/verify        → valida OTP y retorna JWT
"""

import random
import string
import logging
from datetime import datetime, timedelta
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import jwt
import os
import pandas as pd

logger = logging.getLogger(__name__)
router = APIRouter()

# Store en memoria: {cuit: {code, expires_at}}
# En producción reemplazar con Redis
_otp_store: dict = {}

JWT_SECRET = os.getenv("JWT_SECRET", "dev-secret-cambiar-en-produccion")
JWT_EXPIRES_HOURS = int(os.getenv("JWT_EXPIRES_HOURS", "8"))


def _load_proveedor(cuit: str) -> dict | None:
    """Busca un proveedor en el CSV por CUIT."""
    try:
        df = pd.read_csv("backend/data/proveedores.csv", dtype=str)
        # Normalizar CUIT: quitar guiones y espacios
        cuit_clean = cuit.replace("-", "").replace(" ", "")
        df["cuit_clean"] = df["CUIT"].str.replace("-", "").str.replace(" ", "")
        row = df[df["cuit_clean"] == cuit_clean]
        if row.empty:
            return None
        r = row.iloc[0]
        return {
            "cuit": r.get("CUIT", cuit),
            "nombre": r.get("RAZON_SOCIAL", r.get("Razón Social", "Proveedor")),
            "rubro": r.get("RUBRO", r.get("Rubro", "")),
            "localidad": r.get("LOCALIDAD", r.get("Localidad", "")),
            "email": r.get("EMAIL", r.get("Email", "")),
            "whatsapp": r.get("WHATSAPP", r.get("WhatsApp", "")),
        }
    except Exception as e:
        logger.error(f"Error leyendo CSV: {e}")
        return None


def _generate_otp() -> str:
    """Genera código OTP de 6 caracteres alfanuméricos."""
    return "".join(random.choices(string.ascii_uppercase + string.digits, k=6))


class RequestCodeBody(BaseModel):
    cuit: str


class VerifyBody(BaseModel):
    cuit: str
    code: str


@router.post("/request-code")
async def request_code(body: RequestCodeBody):
    """
    Genera un OTP y lo envía por WhatsApp al proveedor.
    Requiere que el CUIT esté registrado en el padrón.
    """
    proveedor = _load_proveedor(body.cuit)
    if not proveedor:
        raise HTTPException(status_code=404, detail="CUIT no encontrado en el padrón municipal")

    whatsapp = proveedor.get("whatsapp", "")
    if not whatsapp:
        raise HTTPException(status_code=400, detail="El proveedor no tiene WhatsApp registrado")

    code = _generate_otp()
    expires_at = datetime.utcnow() + timedelta(minutes=30)
    _otp_store[body.cuit] = {"code": code, "expires_at": expires_at}

    # Enviar por WhatsApp
    try:
        from backend.services.whatsapp import send_whatsapp_message
        mensaje = (
            f"Hola {proveedor['nombre']}! 👋\n\n"
            f"Tu código de acceso al Portal AsisteCR+ es:\n\n"
            f"*{code}*\n\n"
            f"⏱ Válido por 30 minutos. No lo compartas con nadie."
        )
        await send_whatsapp_message(whatsapp, mensaje)
        logger.info(f"OTP enviado a {body.cuit}")
    except Exception as e:
        logger.error(f"Error enviando WhatsApp: {e}")
        # En dev, loguear el código para no bloquear el flujo
        logger.warning(f"[DEV] Código OTP para {body.cuit}: {code}")

    return {
        "status": "ok",
        "mensaje": f"Código enviado por WhatsApp al número registrado.",
        "nombre": proveedor["nombre"],
    }


@router.post("/verify")
async def verify(body: VerifyBody):
    """
    Valida el OTP y retorna un JWT firmado.
    """
    stored = _otp_store.get(body.cuit)

    if not stored:
        raise HTTPException(status_code=400, detail="No hay código activo para este CUIT. Solicitá uno nuevo.")

    if datetime.utcnow() > stored["expires_at"]:
        del _otp_store[body.cuit]
        raise HTTPException(status_code=400, detail="El código expiró. Solicitá uno nuevo.")

    if stored["code"].upper() != body.code.strip().upper():
        raise HTTPException(status_code=400, detail="Código incorrecto.")

    # Código válido — generar JWT
    del _otp_store[body.cuit]
    proveedor = _load_proveedor(body.cuit)

    payload = {
        "cuit": body.cuit,
        "nombre": proveedor["nombre"],
        "rubro": proveedor["rubro"],
        "exp": datetime.utcnow() + timedelta(hours=JWT_EXPIRES_HOURS),
    }

    token = jwt.encode(payload, JWT_SECRET, algorithm="HS256")
    logger.info(f"JWT generado para {body.cuit}")

    return {
        "token": token,
        "nombre": proveedor["nombre"],
        "cuit": body.cuit,
        "rubro": proveedor["rubro"],
    }
```

════════════════════════════════════════════════════════
ARCHIVO: backend/services/auth_service.py
════════════════════════════════════════════════════════

```python
"""
Servicio de autenticación — validación de JWT para rutas protegidas.
Usar como dependencia en endpoints que requieren proveedor autenticado.
"""

import os
import jwt
from fastapi import HTTPException, Header
from typing import Optional

JWT_SECRET = os.getenv("JWT_SECRET", "dev-secret-cambiar-en-produccion")


def get_current_proveedor(authorization: Optional[str] = Header(None)) -> dict:
    """
    Dependencia FastAPI que valida el JWT del header Authorization.
    Uso: proveedor = Depends(get_current_proveedor)
    """
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Token de autenticación requerido")

    token = authorization.split(" ")[1]

    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Sesión expirada. Ingresá nuevamente.")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Token inválido.")


def get_optional_proveedor(authorization: Optional[str] = Header(None)) -> dict | None:
    """
    Igual a get_current_proveedor pero no lanza error si no hay token.
    Para endpoints que funcionan con y sin auth (ej: /chat).
    """
    if not authorization:
        return None
    try:
        return get_current_proveedor(authorization)
    except HTTPException:
        return None
```

════════════════════════════════════════════════════════
ARCHIVO: backend/routers/proveedores.py  (ACTUALIZADO)
════════════════════════════════════════════════════════

```python
"""
Router de proveedores.
GET /proveedores          → busca por rubro (público)
GET /proveedores/{cuit}   → perfil del proveedor (requiere JWT)
"""

import pandas as pd
import logging
from fastapi import APIRouter, HTTPException, Depends
from backend.services.auth_service import get_current_proveedor

logger = logging.getLogger(__name__)
router = APIRouter()

CSV_PATH = "backend/data/proveedores.csv"


def _load_df():
    return pd.read_csv(CSV_PATH, dtype=str).fillna("")


@router.get("")
async def buscar_proveedores(rubro: str = "", localidad: str = "", q: str = ""):
    """Búsqueda pública de proveedores por rubro, localidad o texto libre."""
    df = _load_df()
    if rubro:
        df = df[df.apply(lambda r: rubro.lower() in str(r).lower(), axis=1)]
    if localidad:
        df = df[df.apply(lambda r: localidad.lower() in str(r).lower(), axis=1)]
    if q:
        df = df[df.apply(lambda r: q.lower() in str(r).lower(), axis=1)]
    return {"total": len(df), "proveedores": df.head(50).to_dict(orient="records")}


@router.get("/{cuit}")
async def get_perfil(cuit: str, proveedor_auth: dict = Depends(get_current_proveedor)):
    """
    Retorna el perfil completo del proveedor autenticado.
    Solo puede consultar su propio CUIT.
    """
    cuit_clean = cuit.replace("-", "").replace(" ", "")
    auth_cuit_clean = proveedor_auth["cuit"].replace("-", "").replace(" ", "")

    if cuit_clean != auth_cuit_clean:
        raise HTTPException(status_code=403, detail="No podés consultar datos de otro proveedor.")

    df = _load_df()
    df["cuit_clean"] = df["CUIT"].str.replace("-", "").str.replace(" ", "")
    row = df[df["cuit_clean"] == cuit_clean]

    if row.empty:
        raise HTTPException(status_code=404, detail="Proveedor no encontrado.")

    r = row.iloc[0]
    return {
        "cuit": r.get("CUIT", cuit),
        "nombre": r.get("RAZON_SOCIAL", r.get("Razón Social", "")),
        "rubro": r.get("RUBRO", r.get("Rubro", "")),
        "localidad": r.get("LOCALIDAD", r.get("Localidad", "")),
        "email": r.get("EMAIL", r.get("Email", "")),
        "whatsapp": r.get("WHATSAPP", r.get("WhatsApp", "")),
        "estado_inscripcion": "activo",  # TODO: calcular desde campo fecha_vencimiento
        "completitud_legajo": 78,         # TODO: calcular desde campos presentes
    }
```

════════════════════════════════════════════════════════
ARCHIVO: backend/routers/chat.py  (ACTUALIZADO — con contexto del proveedor)
════════════════════════════════════════════════════════

```python
"""
Router del chat IA — POST /chat con streaming SSE.
Si hay JWT válido, inyecta el contexto del proveedor en el system prompt.
"""

import os
import json
import logging
from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import Optional
import anthropic
from backend.services.auth_service import get_optional_proveedor

logger = logging.getLogger(__name__)
router = APIRouter()
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

SYSTEM_BASE = """Sos AsisteCR+, el asistente de inteligencia artificial del sistema de compras y contrataciones públicas municipales.

Tu función es ayudar a los proveedores a:
- Entender las licitaciones activas y sus pliegos
- Preparar la documentación necesaria para presentar ofertas
- Consultar normativa vigente (Ley II N°76, Ley N°4829 Compre Chubut, Decreto 777/06)
- Calcular garantías y plazos
- Resolver dudas sobre el proceso licitatorio

Respondé siempre en español rioplatense, con tono amigable y claro. Usá viñetas y formato simple.
Cuando no sepas algo con certeza, recomendá consultar con la Dirección de Licitaciones: licitacionesyconcursos@comodoro.gov.ar"""


def _build_system_prompt(proveedor: dict | None) -> str:
    if not proveedor:
        return SYSTEM_BASE
    return (
        SYSTEM_BASE
        + f"\n\n---\nPROVEEDOR AUTENTICADO:\n"
        + f"- Nombre: {proveedor.get('nombre', 'Proveedor')}\n"
        + f"- CUIT: {proveedor.get('cuit', '')}\n"
        + f"- Rubro: {proveedor.get('rubro', '')}\n"
        + "\nPersonalizá las respuestas según su rubro. "
        + "Si pregunta sobre sus licitaciones, referite a las que coinciden con su rubro."
    )


class ChatMessage(BaseModel):
    role: str  # "user" o "assistant"
    content: str


class ChatRequest(BaseModel):
    messages: list[ChatMessage]
    context: Optional[str] = None  # Contexto adicional (ej: licitación específica)


@router.post("")
async def chat(
    body: ChatRequest,
    proveedor: dict | None = Depends(get_optional_proveedor)
):
    """Chat con streaming SSE. Acepta historial de mensajes."""

    system_prompt = _build_system_prompt(proveedor)
    if body.context:
        system_prompt += f"\n\nCONTEXTO ADICIONAL:\n{body.context}"

    messages = [{"role": m.role, "content": m.content} for m in body.messages]

    def stream_response():
        with client.messages.stream(
            model="claude-sonnet-4-20250514",
            max_tokens=1024,
            system=system_prompt,
            messages=messages,
        ) as stream:
            for text in stream.text_stream:
                yield f"data: {json.dumps({'text': text})}\n\n"
        yield "data: [DONE]\n\n"

    return StreamingResponse(
        stream_response(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )
```

════════════════════════════════════════════════════════
ARCHIVO: backend/main.py  (ACTUALIZADO — agrega router auth)
════════════════════════════════════════════════════════

```python
"""
AsisteCR+ — Backend FastAPI
Entry point: uvicorn backend.main:app
"""

import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import os

from backend.routers import licitaciones, proveedores, notificaciones, chat, auth
from backend.services.scraper import run_scraper

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Iniciando backend — corriendo scraper inicial...")
    try:
        await run_scraper()
        logger.info("Scraper completado.")
    except Exception as e:
        logger.warning(f"Scraper falló al iniciar (usando cache): {e}")
    yield


app = FastAPI(
    title="AsisteCR+ — Plataforma Municipal de Compras",
    description="API para el portal de proveedores y chatbot de licitaciones",
    version="0.2.0",
    lifespan=lifespan,
)

CORS_ORIGINS = os.getenv("CORS_ORIGINS", "http://localhost:3000,http://127.0.0.1:5500").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router,          prefix="/auth",       tags=["Auth"])
app.include_router(licitaciones.router,  prefix="/licitaciones", tags=["Licitaciones"])
app.include_router(proveedores.router,   prefix="/proveedores",  tags=["Proveedores"])
app.include_router(notificaciones.router,prefix="/notificar",    tags=["Notificaciones"])
app.include_router(chat.router,          prefix="/chat",          tags=["Chat IA"])


@app.get("/")
async def root():
    return {"status": "ok", "servicio": "AsisteCR+ · Municipalidad de Comodoro Rivadavia", "version": "0.2.0"}


@app.get("/health")
async def health():
    return {"status": "healthy"}
```

════════════════════════════════════════════════════════
ARCHIVO: backend/requirements.txt  (ACTUALIZADO)
════════════════════════════════════════════════════════

```
fastapi==0.111.0
uvicorn[standard]==0.30.1
anthropic==0.28.0
twilio==9.2.0
httpx==0.27.0
beautifulsoup4==4.12.3
pandas==2.2.2
python-dotenv==1.0.1
PyJWT==2.8.0
python-jose[cryptography]==3.3.0
pytest==8.2.0
pytest-asyncio==0.23.7
httpx==0.27.0
```

════════════════════════════════════════════════════════
ARCHIVO: backend/.env.example  (ACTUALIZADO)
════════════════════════════════════════════════════════

```bash
# Anthropic
ANTHROPIC_API_KEY=sk-ant-api03-...

# Twilio WhatsApp
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_WHATSAPP_FROM=whatsapp:+14155238886

# Auth JWT
JWT_SECRET=reemplazar-con-string-aleatorio-largo-y-seguro
JWT_EXPIRES_HOURS=8

# Admin
ADMIN_PASSWORD=reemplazar-en-produccion

# CORS
CORS_ORIGINS=https://tu-app.vercel.app,http://localhost:3000
```

════════════════════════════════════════════════════════
ARCHIVO: login.html  (NUEVO — autenticación por CUIT + OTP)
════════════════════════════════════════════════════════

```html
<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>AsisteCR+ · Acceso Proveedor</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=DM+Sans:wght@300;400;500&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="components.css">
  <style>
    body {
      min-height: 100vh;
      background: linear-gradient(135deg, #0B2347 0%, #1B3B6A 100%);
      display: flex; align-items: center; justify-content: center;
      padding: 24px;
      font-family: 'DM Sans', sans-serif;
    }
    .login-box {
      background: #fff;
      border-radius: 20px;
      padding: 36px;
      width: 100%; max-width: 420px;
      box-shadow: 0 20px 60px rgba(0,0,0,.3);
    }
    .brand { text-align: center; margin-bottom: 32px; }
    .brand-name { font-family: 'Syne', sans-serif; font-size: 28px; font-weight: 800; color: #0B2347; }
    .brand-name span { color: #E8A000; }
    .brand-sub { font-size: 13px; color: #6B7A90; margin-top: 4px; }
    .step { display: none; }
    .step.active { display: block; }
    .field-label { font-size: 12px; font-weight: 600; color: #6B7A90; text-transform: uppercase; letter-spacing: .06em; margin-bottom: 6px; }
    .field-input {
      width: 100%; padding: 12px 14px;
      border: 1.5px solid #E8EDF5; border-radius: 10px;
      font-size: 15px; font-family: 'DM Sans', sans-serif;
      outline: none; transition: border-color .2s;
      background: #F4F7FC;
    }
    .field-input:focus { border-color: #2278D4; background: #fff; }
    .btn-submit {
      width: 100%; padding: 13px;
      background: #1055A8; color: #fff;
      border: none; border-radius: 10px;
      font-family: 'Syne', sans-serif; font-size: 15px; font-weight: 700;
      cursor: pointer; transition: all .2s; margin-top: 20px;
    }
    .btn-submit:hover { background: #2278D4; transform: translateY(-1px); }
    .btn-submit:disabled { background: #B0BCCF; cursor: not-allowed; transform: none; }
    .msg { font-size: 13px; margin-top: 12px; min-height: 20px; }
    .msg.error { color: #C0302A; }
    .msg.success { color: #0F7A45; }
    .otp-note { background: #F4F7FC; border-radius: 10px; padding: 14px; font-size: 12px; color: #6B7A90; margin-top: 20px; }
    .back-link { text-align: center; margin-top: 16px; }
    .back-link a { font-size: 12px; color: #6B7A90; text-decoration: none; }
    .back-link a:hover { color: #1055A8; }
  </style>
</head>
<body>
<div class="login-box">
  <div class="brand">
    <div class="brand-name">Asiste<span>CR+</span></div>
    <div class="brand-sub">Portal del Proveedor Municipal</div>
  </div>

  <!-- Paso 1: CUIT -->
  <div class="step active" id="step1">
    <h2 style="font-family:'Syne',sans-serif; font-size:18px; font-weight:800; color:#0B2347; margin-bottom:6px;">Ingresá tu CUIT</h2>
    <p style="font-size:13px; color:#6B7A90; margin-bottom:24px;">Te enviaremos un código de acceso por WhatsApp.</p>
    <div style="margin-bottom:16px;">
      <div class="field-label">CUIT de tu empresa</div>
      <input class="field-input" type="text" id="cuit-input" placeholder="20-28734190-4" maxlength="13">
    </div>
    <button class="btn-submit" id="btn-step1" onclick="requestCode()">Enviar código por WhatsApp →</button>
    <div class="msg" id="msg-step1"></div>
    <div class="otp-note">🔒 No necesitás contraseña. El acceso es mediante un código de un solo uso válido 30 minutos.</div>
  </div>

  <!-- Paso 2: OTP -->
  <div class="step" id="step2">
    <h2 style="font-family:'Syne',sans-serif; font-size:18px; font-weight:800; color:#0B2347; margin-bottom:6px;">Ingresá tu código</h2>
    <p style="font-size:13px; color:#6B7A90; margin-bottom:24px;" id="step2-sub">Te enviamos un código de 6 caracteres por WhatsApp.</p>
    <div style="margin-bottom:16px;">
      <div class="field-label">Código de acceso</div>
      <input class="field-input" type="text" id="otp-input" placeholder="Ej: A3F7K2" maxlength="6" style="text-transform:uppercase; letter-spacing:.2em; font-size:22px; text-align:center;">
    </div>
    <button class="btn-submit" id="btn-step2" onclick="verifyCode()">Ingresar al portal →</button>
    <div class="msg" id="msg-step2"></div>
    <div class="back-link"><a href="#" onclick="goBack()">← Cambiar CUIT</a></div>
  </div>
</div>

<script>
const API = 'http://localhost:8000'; // Cambiar en prod

let cuitActual = '';

async function requestCode() {
  const cuit = document.getElementById('cuit-input').value.trim();
  if (!cuit) { showMsg('step1', 'Ingresá tu CUIT.', 'error'); return; }

  const btn = document.getElementById('btn-step1');
  btn.disabled = true; btn.textContent = 'Enviando...';

  try {
    const res = await fetch(`${API}/auth/request-code`, {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({cuit})
    });
    const data = await res.json();
    if (!res.ok) throw new Error(data.detail || 'Error al enviar código');
    cuitActual = cuit;
    document.getElementById('step2-sub').textContent = `Código enviado a ${data.nombre} por WhatsApp.`;
    showStep('step2');
  } catch (e) {
    showMsg('step1', e.message, 'error');
  } finally {
    btn.disabled = false; btn.textContent = 'Enviar código por WhatsApp →';
  }
}

async function verifyCode() {
  const code = document.getElementById('otp-input').value.trim().toUpperCase();
  if (code.length < 6) { showMsg('step2', 'Ingresá los 6 caracteres del código.', 'error'); return; }

  const btn = document.getElementById('btn-step2');
  btn.disabled = true; btn.textContent = 'Verificando...';

  try {
    const res = await fetch(`${API}/auth/verify`, {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({cuit: cuitActual, code})
    });
    const data = await res.json();
    if (!res.ok) throw new Error(data.detail || 'Código incorrecto');
    sessionStorage.setItem('asistecr_token', data.token);
    sessionStorage.setItem('asistecr_nombre', data.nombre);
    sessionStorage.setItem('asistecr_cuit', data.cuit);
    sessionStorage.setItem('asistecr_rubro', data.rubro);
    showMsg('step2', `¡Bienvenido, ${data.nombre}! Redirigiendo...`, 'success');
    setTimeout(() => { window.location.href = 'portal.html'; }, 1000);
  } catch (e) {
    showMsg('step2', e.message, 'error');
    btn.disabled = false; btn.textContent = 'Ingresar al portal →';
  }
}

function showStep(id) {
  document.querySelectorAll('.step').forEach(s => s.classList.remove('active'));
  document.getElementById(id).classList.add('active');
}
function goBack() { showStep('step1'); }
function showMsg(step, text, type) {
  const el = document.getElementById(`msg-${step}`);
  el.textContent = text; el.className = `msg ${type}`;
}
</script>
</body>
</html>
```

════════════════════════════════════════════════════════
NOTAS DE INTEGRACIÓN
════════════════════════════════════════════════════════

1. **Agregar al backend/main.py**: importar y registrar `auth.router` con prefix="/auth"
   (ver archivo main.py actualizado arriba)

2. **Cambiar en portal.html**: al cargar, verificar JWT en sessionStorage
   ```javascript
   const token = sessionStorage.getItem('asistecr_token');
   if (!token) window.location.href = 'login.html';
   ```

3. **En los fetch del portal**, agregar el header:
   ```javascript
   headers: { 'Authorization': `Bearer ${sessionStorage.getItem('asistecr_token')}` }
   ```

4. **En el endpoint /chat**, el contexto del proveedor se inyecta automáticamente
   si el header Authorization está presente — no hay que cambiar nada en el frontend.

5. **Variables de entorno nuevas**: agregar JWT_SECRET y JWT_EXPIRES_HOURS al .env de Railway/Render.
