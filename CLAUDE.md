# AsisteCR+ · Municipalidad de Comodoro Rivadavia

Plataforma de compras y contrataciones públicas municipales con IA conversacional.
Incluye chatbot público (index) + Portal del Proveedor con autenticación por CUIT.

---

## Arquitectura general

```
/                         ← Frontend estático (Vercel)
  index.html              ← Landing pública: hero, feature cards, preview chat, licitaciones
  login.html              ← Acceso proveedor: CUIT + código OTP (WhatsApp)
  portal.html             ← Portal autenticado: dashboard + 6 secciones (SPA con JS)
  admin.html              ← Panel admin: crear/editar licitaciones
  components.css          ← Sistema de diseño compartido (badges, cards, tablas, alerts)

/backend/                 ← FastAPI app (Railway o Render)
  main.py                 ← Entry point: uvicorn backend.main:app
  routers/
    licitaciones.py       ← GET /licitaciones, POST /licitaciones
    proveedores.py        ← GET /proveedores?rubro=X, GET /proveedores/{cuit}
    notificaciones.py     ← POST /notificar (dispara WhatsApp)
    chat.py               ← POST /chat (streaming SSE, contexto del proveedor)
    auth.py               ← POST /auth/request-code, POST /auth/verify → JWT
  services/
    scraper.py            ← Scraper comodoro.gov.ar/licitaciones
    whatsapp.py           ← Twilio WhatsApp wrapper
    auth_service.py       ← Generación/validación OTP y JWT
  data/
    proveedores.csv       ← 6.840 proveedores (CUIT, razón social, rubro, localidad)
    licitaciones.json     ← Cache del scraper + licitaciones manuales
```

---

## Stack

- **Frontend**: HTML + CSS + JS vanilla. Fuentes: Syne + DM Sans (Google Fonts). Deploy: Vercel.
- **Backend**: Python 3.11+ · FastAPI · uvicorn. Deploy: Railway (o Render).
- **IA**: Anthropic SDK. Modelo: `claude-sonnet-4-20250514`. Streaming SSE.
- **Auth**: JWT (PyJWT). OTP 6 chars, TTL 30 min, enviado por WhatsApp.
- **Scraping**: `httpx` + `beautifulsoup4`.
- **Notificaciones**: Twilio WhatsApp API.
- **CSV**: `pandas` para padrón de proveedores.
- **CI/CD**: GitHub Actions → Vercel + Railway.

---

## Flujo de autenticación del Portal

```
1. login.html → POST /auth/request-code {cuit}
   └── Busca proveedor en CSV → genera OTP → envía por WhatsApp → guarda en memoria TTL 30min

2. login.html → POST /auth/verify {cuit, code}
   └── Valida OTP → retorna JWT {cuit, nombre, rubros, exp: +8hs}
   └── Frontend guarda JWT en sessionStorage

3. portal.html carga → JS verifica JWT
   └── Inválido/expirado → redirect login.html
   └── Válido → GET /proveedores/{cuit} → carga perfil del proveedor

4. Logout → borra sessionStorage → redirect index.html
```

---

## Portal del Proveedor — Secciones (portal.html SPA)

| Screen | Hash | Endpoint principal | Descripción |
|--------|------|--------------------|-------------|
| Dashboard | `#dashboard` | GET /proveedores/{cuit} + GET /licitaciones | KPIs, licitaciones compatibles, estado inscripción, alertas |
| Mi Legajo | `#legajo` | GET /proveedores/{cuit} | Datos empresa, documentación, rubros |
| Licitaciones | `#licitaciones` | GET /licitaciones?rubro=X | Tabla filtrable, tag "Para vos" por rubro |
| Mis Ofertas | `#ofertas` | (simulado en v1) | Historial de presentaciones con estados |
| Normativa | `#normativa` | (estático) | Links a PDFs, CTA al asistente IA |
| Asistente IA | `#chat` | POST /chat (SSE) | Chat con contexto del proveedor inyectado |
| Notificaciones | `#notificaciones` | (log Twilio en v1) | Historial de alertas WhatsApp recibidas |

---

## Sistema de diseño

### Paleta
```
--navy:   #0B2347   sidebar, hero, headings
--blue:   #1055A8   botón primario, links
--sky:    #2278D4   acento activo, nav, bordes
--sky-l:  #EDF4FF   fondo chips y badges open
--gold:   #E8A000   alertas, brand accent
--green:  #0F7A45   activo, adjudicado, success
--red:    #C0302A   error, no adjudicada
--gray-1: #F4F7FC   fondo page
--gray-2: #E8EDF5   bordes, separadores
--gray-4: #6B7A90   texto secundario
```

### Tipografía
- **Syne 800/700/600**: títulos, brand, KPIs, nav
- **DM Sans 400/500**: cuerpo, tablas, UI

### Componentes (components.css)
- `.badge` + variantes: `badge-active`, `badge-pending`, `badge-inactive`, `badge-open`, `badge-closed`
- `.card` + `.card-header` + `.card-body`
- `.stat-card` con accent top (`.c-blue`, `.c-green`, `.c-gold`, `.c-sky`)
- `.alert-banner` + variantes: `alert-gold`, `alert-green`, `alert-blue`
- `.btn-primary`, `.btn-ghost`, `.btn-hero-primary`
- `.data-table` con hover y zebra stripes
- `.chip` para quick-actions del chat

---

## Comandos esenciales

```bash
# Backend local
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --port 8000

# Nueva dependencia de auth
pip install PyJWT python-jose

# Scraper manual
python -m backend.services.scraper

# Tests
pytest backend/tests/ -v

# Frontend
open index.html    # público, sin auth
open login.html    # para obtener JWT
# portal.html requiere JWT en sessionStorage
```

---

## Variables de entorno

```bash
# backend/.env — nunca commitear
ANTHROPIC_API_KEY=sk-ant-...
TWILIO_ACCOUNT_SID=AC...
TWILIO_AUTH_TOKEN=...
TWILIO_WHATSAPP_FROM=whatsapp:+14155238886
JWT_SECRET=cambiar-en-produccion-random-largo
JWT_EXPIRES_HOURS=8
ADMIN_PASSWORD=comodoro2025
CORS_ORIGINS=https://comodoro-asistente.vercel.app,http://localhost:3000
```

---

## Convenciones

- Python: PEP 8, type hints, docstrings en español, voseo rioplatense en mensajes al usuario.
- Endpoints: sustantivos plurales snake_case. Auth bajo `/auth/`.
- Errores: siempre `{"error": "mensaje en español"}`.
- No `print()` en prod — usar `logging`.
- Scraper: retry 3 intentos con backoff exponencial.
- Chat: **streaming SSE**. System prompt incluye contexto del proveedor cuando hay JWT.
- OTPs en memoria (dict Python). En producción → Redis.
- CSV: **solo lectura** — nunca modificar programáticamente.
- Portal: **SPA** — no recargar al navegar entre secciones.
- Rutas públicas (licitaciones, normativa, chat sin contexto) no requieren JWT.

---

## Reglas importantes

- NO commitear `.env`.
- NO hardcodear `localhost` — usar env vars.
- NO llamar Anthropic desde el frontend — siempre via backend.
- Endpoints de escritura validan `ADMIN_PASSWORD`.
- JWT validado en backend en cada endpoint protegido (`Authorization: Bearer <token>`).

---

## Contexto del dominio

- **Licitación Pública**: proceso abierto a proveedores habilitados.
- **Pliego de Bases**: documento con reglas de la licitación (PBCG general + PBCP particular).
- **Proveedor**: empresa/persona inscripta en el padrón municipal (CSV).
- **Normativa clave**: Ley II N°76 (contrataciones Chubut), Ley N°4829 (Compre Chubut), Decreto 777/06.
- **OTP**: código único 6 chars por WhatsApp, válido 30 min.
- **Contacto oficial**: licitacionesyconcursos@comodoro.gov.ar · Namuncurá 26, Comodoro Rivadavia.

---

## Docs de referencia

- Issues Sprint 1–3 (chatbot): `@docs/issues-plan.md`
- Issues Sprint 4–5 (portal): GitHub Project #2 — issues #016 al #029
- Prototipo UX navegable: `@docs/ux-proposal.html`
- API Anthropic streaming: https://docs.anthropic.com/en/api/messages-streaming
- Twilio WhatsApp: https://www.twilio.com/docs/whatsapp/quickstart/python
- PyJWT: https://pyjwt.readthedocs.io/
