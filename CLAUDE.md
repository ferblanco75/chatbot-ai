# Asistente de Compras · Municipalidad de Comodoro Rivadavia

Chatbot estilo Boti (GCBA) para licitaciones y compras públicas municipales.
Widget flotante HTML/JS en el frontend + backend FastAPI (Python) para scraping, proveedores y notificaciones WhatsApp.

## Arquitectura

```
/                         ← Frontend estático (Vercel)
  index.html              ← Widget Boti + sitio municipal simulado
  admin.html              ← Panel admin para crear licitaciones
/backend/                 ← FastAPI app (Railway o Render)
  main.py                 ← Entry point: uvicorn backend.main:app
  routers/
    licitaciones.py       ← GET /licitaciones, POST /licitaciones
    proveedores.py        ← GET /proveedores?rubro=limpieza
    notificaciones.py     ← POST /notificar (dispara WhatsApp)
  services/
    scraper.py            ← Scraper comodoro.gov.ar/licitaciones
    whatsapp.py           ← Twilio WhatsApp wrapper
  data/
    proveedores.csv       ← 6.840 proveedores (CUIT, razón social, localidad)
    licitaciones.json     ← Cache del scraper + licitaciones manuales
/docs/                    ← Documentación adicional (no va al CLAUDE.md)
  architecture.md
  issues-plan.md
```

## Stack

- **Frontend**: HTML + CSS + JS vanilla (sin framework). Fuente: Nunito (Google Fonts). Deploy: Vercel.
- **Backend**: Python 3.11+ · FastAPI · uvicorn. Deploy: Railway (o Render como alternativa).
- **IA**: Anthropic Python SDK (`anthropic`). Modelo: `claude-sonnet-4-20250514`.
- **Scraping**: `httpx` + `beautifulsoup4`. Target: `https://www.comodoro.gov.ar/secciones/licitaciones/`
- **Notificaciones**: Twilio Python SDK. Canal: WhatsApp Sandbox (dev) → WhatsApp Business (prod).
- **CSV**: `pandas` para carga y búsqueda del padrón de proveedores.
- **CI/CD**: GitHub Actions → deploy automático a Vercel (frontend) y Railway (backend).

## Comandos esenciales

```bash
# Backend — desarrollo local
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --port 8000

# Correr scraper manualmente
python -m backend.services.scraper

# Tests
pytest backend/tests/ -v

# Frontend — abrir directo en browser (no necesita servidor)
open index.html
```

## Variables de entorno

```
# backend/.env (nunca commitear — ver .env.example)
ANTHROPIC_API_KEY=sk-ant-...
TWILIO_ACCOUNT_SID=AC...
TWILIO_AUTH_TOKEN=...
TWILIO_WHATSAPP_FROM=whatsapp:+14155238886
ADMIN_PASSWORD=comodoro2025
CORS_ORIGINS=https://comodoro-asistente.vercel.app,http://localhost:3000
```

## Convenciones de código

- Python: PEP 8, type hints en todas las funciones, docstrings en español.
- Nombres de variables y funciones: inglés. Comentarios y mensajes de usuario: español (voseo rioplatense).
- Endpoints REST: sustantivos en plural, snake_case. Ej: `/licitaciones`, `/proveedores`.
- Errores HTTP: siempre retornar `{"error": "mensaje descriptivo en español"}`.
- No usar `print()` en producción — usar `logging` con nivel apropiado.
- El scraper debe manejar errores de red con retry (3 intentos, backoff exponencial).

## Reglas importantes

- NO commitear `.env` ni ningún archivo con credenciales.
- NO usar `localhost` hardcodeado — usar variables de entorno para URLs.
- NO llamar a la Anthropic API desde el frontend en producción — siempre via el backend.
- Los endpoints del backend deben validar el `ADMIN_PASSWORD` en las rutas de escritura (`POST /licitaciones`).
- El CSV de proveedores es de solo lectura — nunca modificarlo programáticamente.
- Mantener `requirements.txt` actualizado con versiones pinneadas (`==`).

## Contexto del dominio

- **Licitación Pública**: proceso abierto, cualquier proveedor puede participar.
- **Pliego de Bases**: documento que define las reglas de cada licitación (PBCG general + PBCP particular).
- **Proveedor**: empresa o persona física inscripta en el padrón municipal (CSV disponible).
- **Normativa**: Ley II N°76 (contrataciones provinciales), Ley N°4829 (Compre Chubut).
- **Contacto oficial**: licitacionesyconcursos@comodoro.gov.ar · Namuncurá 26, Comodoro Rivadavia.

## Docs de referencia

- Arquitectura detallada: @docs/architecture.md
- Plan de issues: @docs/issues-plan.md
- API Anthropic: https://docs.anthropic.com/en/api/messages
- Twilio WhatsApp: https://www.twilio.com/docs/whatsapp/quickstart/python
