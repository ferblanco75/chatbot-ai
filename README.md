# AsisteCR+ — Plataforma Municipal de Compras Inteligente

> Asistente de inteligencia artificial para compras y contrataciones públicas de la Municipalidad de Comodoro Rivadavia.

---

## ¿Qué es AsisteCR+?

AsisteCR+ es una plataforma digital que conecta a los proveedores municipales con el sistema de licitaciones mediante inteligencia artificial. Permite:

- **Consultar licitaciones activas** filtradas por rubro, en lenguaje natural
- **Acceder al portal del proveedor**: legajo, estado de inscripción, historial de ofertas
- **Recibir alertas automáticas por WhatsApp** cuando se publica una licitación compatible
- **Consultar normativa y pliegos** con asistencia de IA disponible 24/7

---

## Estructura del proyecto

```
/
├── index.html          ← Landing pública (sin login requerido)
├── login.html          ← Acceso al portal: CUIT + código WhatsApp
├── portal.html         ← Portal del proveedor (requiere autenticación)
├── admin.html          ← Panel municipal (requiere contraseña admin)
├── components.css      ← Sistema de diseño compartido
│
└── backend/
    ├── main.py
    ├── routers/
    │   ├── auth.py           ← OTP + JWT
    │   ├── chat.py           ← IA conversacional (streaming)
    │   ├── licitaciones.py
    │   ├── proveedores.py
    │   └── notificaciones.py
    ├── services/
    │   ├── auth_service.py
    │   ├── scraper.py
    │   └── whatsapp.py
    └── data/
        ├── proveedores.csv   ← 6.840 proveedores registrados
        └── licitaciones.json ← Cache de licitaciones
```

---

## Tecnologías

| Capa | Tecnología |
|------|-----------|
| Frontend | HTML + CSS + JS vanilla · Syne + DM Sans |
| Backend | Python 3.11 · FastAPI · uvicorn |
| IA | Anthropic Claude API (streaming SSE) |
| Auth | JWT (PyJWT) · OTP por WhatsApp |
| Notificaciones | Twilio WhatsApp Business API |
| Deploy Frontend | Vercel |
| Deploy Backend | Railway / Render |
| CI/CD | GitHub Actions |

---

## Instalación local

### Backend

```bash
cd backend
cp .env.example .env      # completar con tus credenciales
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

La API queda disponible en `http://localhost:8000`.  
Documentación automática: `http://localhost:8000/docs`

### Frontend

```bash
# No necesita servidor — abrir directo en el browser
open index.html

# Para el portal, primero obtener JWT via login.html
open login.html
```

---

## Variables de entorno requeridas

Crear `backend/.env` basado en `backend/.env.example`:

```bash
ANTHROPIC_API_KEY=sk-ant-...          # Anthropic Console
TWILIO_ACCOUNT_SID=AC...              # Twilio Console
TWILIO_AUTH_TOKEN=...                 # Twilio Console
TWILIO_WHATSAPP_FROM=whatsapp:+14155238886
JWT_SECRET=string-random-largo        # Cualquier string seguro
JWT_EXPIRES_HOURS=8
ADMIN_PASSWORD=tu-contraseña-admin
CORS_ORIGINS=https://tu-app.vercel.app,http://localhost:3000
```

---

## Endpoints principales

| Método | Ruta | Auth | Descripción |
|--------|------|------|-------------|
| POST | `/auth/request-code` | No | Solicita OTP por WhatsApp |
| POST | `/auth/verify` | No | Valida OTP → retorna JWT |
| GET | `/licitaciones` | No | Lista licitaciones (filter: ?rubro=) |
| POST | `/licitaciones` | Admin | Crea licitación manual |
| GET | `/proveedores/{cuit}` | JWT | Perfil del proveedor autenticado |
| GET | `/proveedores` | No | Busca proveedores por rubro |
| POST | `/chat` | Opcional | Chat IA (SSE streaming) |
| POST | `/notificar` | Admin | Dispara alertas WhatsApp |

---

## Portal del Proveedor

El portal (`portal.html`) es una SPA en JS vanilla con 7 secciones:

1. **Dashboard** — KPIs, licitaciones compatibles con el rubro, estado de inscripción
2. **Mi Legajo** — Datos de la empresa, documentación, rubros declarados
3. **Licitaciones** — Tabla completa con filtros y tag "Para vos" por rubro
4. **Mis Ofertas** — Historial de presentaciones con estados y métricas
5. **Normativa** — Marco legal vigente (Ley II N°76, Ley 4829, Decreto 777/06)
6. **Asistente IA** — Chat con contexto del proveedor precargado
7. **Notificaciones** — Historial de alertas WhatsApp recibidas

### Acceso
El proveedor ingresa con su **CUIT** y un **código de 6 caracteres** enviado por WhatsApp. No necesita contraseña ni crear una cuenta.

---

## Deploy

### Frontend → Vercel
```bash
# Conectar repo en vercel.com → deploy automático en cada push a main
# El directorio raíz es /  (index.html, portal.html, etc. en la raíz)
```

### Backend → Railway
```bash
# Conectar repo en railway.app
# Configurar variables de entorno en el dashboard
# Railway detecta automáticamente el Procfile o el uvicorn command
```

---

## Planificación

- **Sprint 1–3** (chatbot base): Issues #001–#015 — completados
- **Sprint 4–5** (portal del proveedor): Issues #016–#029 — en curso
- Proyecto GitHub: https://github.com/users/ferblanco75/projects/2

---

## Licencia

Proyecto desarrollado para la Municipalidad de Comodoro Rivadavia.  
Consultas: ferblanco@gmail.com · +54 11 5701-6249
