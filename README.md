# Codi - Asistente de Compras Municipal

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115.6-009688.svg?logo=fastapi)](https://fastapi.tiangolo.com)
[![Claude AI](https://img.shields.io/badge/Claude-Sonnet%204.5-orange.svg)](https://www.anthropic.com)

> Chatbot inteligente estilo Boti (GCBA) para consultas sobre licitaciones y compras públicas de la Municipalidad de Comodoro Rivadavia.

![Demo del Asistente Codi](docs/assets/demo-screenshot.png)

## Descripción

**Codi** es un asistente virtual conversacional que facilita el acceso a información sobre licitaciones públicas municipales. Inspirado en [Boti](https://buenosaires.gob.ar/jefaturadegabinete/innovacion/boti) del Gobierno de la Ciudad de Buenos Aires, Codi permite a ciudadanos y proveedores:

- Consultar licitaciones activas y archivadas
- Buscar información sobre procesos de contratación
- Acceder al padrón de proveedores municipales (6.840 registros)
- Recibir notificaciones de nuevas licitaciones por WhatsApp
- Obtener información sobre normativa (Ley II N°76, Ley N°4829 Compre Chubut)

**Modelo de IA**: Claude Sonnet 4.5 (Anthropic) · **Interfaz**: Widget HTML/JS flotante · **Backend**: FastAPI (Python)

---

## Características Principales

- **Conversación Natural**: Procesamiento de lenguaje natural con Claude Sonnet 4.5
- **Widget Embebible**: Botón flotante (FAB) que se integra en cualquier sitio web
- **Scraping Automático**: Extracción de licitaciones desde el sitio oficial de Comodoro
- **Búsqueda de Proveedores**: Consulta del padrón municipal por CUIT, razón social o rubro
- **Notificaciones WhatsApp**: Alertas automáticas vía Twilio
- **Panel Admin**: Gestión manual de licitaciones desde interfaz web
- **Deploy Automático**: CI/CD con GitHub Actions → Vercel (frontend) + Railway/Render (backend)
- **Diseño Responsive**: Adaptado a mobile, tablet y desktop

---

## Stack Tecnológico

### Frontend
- **HTML5 + CSS3 + JavaScript Vanilla**: Sin frameworks, ligero y rápido
- **Fuente**: Nunito (Google Fonts)
- **Deploy**: [Vercel](https://vercel.com)

### Backend
- **Framework**: [FastAPI](https://fastapi.tiangolo.com) 0.115.6
- **Servidor**: [Uvicorn](https://www.uvicorn.org) con ASGI
- **Python**: 3.11+
- **Deploy**: [Railway](https://railway.app) o [Render](https://render.com)

### Inteligencia Artificial
- **API**: [Anthropic Claude](https://www.anthropic.com)
- **Modelo**: `claude-sonnet-4-20250514`
- **SDK**: `anthropic` (Python)

### Web Scraping
- **HTTP Client**: `httpx`
- **Parser**: `beautifulsoup4`
- **Target**: https://www.comodoro.gov.ar/secciones/licitaciones/

### Notificaciones
- **Servicio**: [Twilio WhatsApp API](https://www.twilio.com/whatsapp)
- **SDK**: `twilio` (Python)

### Datos
- **Padrón de Proveedores**: CSV con 6.840 registros (lectura con `pandas`)
- **Cache de Licitaciones**: JSON local

---

## Arquitectura

```
┌─────────────────────────────────────────────────────────────┐
│                         FRONTEND                             │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐  │
│  │  index.html  │    │  admin.html  │    │ assets/      │  │
│  │  (Widget)    │    │  (Panel)     │    │ (Avatar SVG) │  │
│  └──────────────┘    └──────────────┘    └──────────────┘  │
│                  Deploy: Vercel                              │
└─────────────────────────────────────────────────────────────┘
                             │
                         HTTPS │ API Calls
                             │
┌─────────────────────────────────────────────────────────────┐
│                        BACKEND (FastAPI)                     │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  main.py  (Entry Point)                              │  │
│  └──────────────────────────────────────────────────────┘  │
│                             │                                │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Routers (Endpoints REST)                            │  │
│  │  ├── /chat          → Conversación con Claude        │  │
│  │  ├── /licitaciones  → GET/POST licitaciones          │  │
│  │  ├── /proveedores   → Búsqueda en CSV                │  │
│  │  └── /notificaciones → Envío WhatsApp                │  │
│  └──────────────────────────────────────────────────────┘  │
│                             │                                │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Services                                            │  │
│  │  ├── scraper.py    → Web scraping comodoro.gov.ar    │  │
│  │  └── whatsapp.py   → Twilio wrapper                  │  │
│  └──────────────────────────────────────────────────────┘  │
│                             │                                │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Data                                                │  │
│  │  ├── proveedores.csv    (6.840 proveedores)          │  │
│  │  └── licitaciones.json  (Cache del scraper)          │  │
│  └──────────────────────────────────────────────────────┘  │
│                  Deploy: Railway / Render                    │
└─────────────────────────────────────────────────────────────┘
                             │
                   ┌─────────┴─────────┐
                   │                   │
           ┌───────▼──────┐    ┌──────▼──────┐
           │  Anthropic   │    │   Twilio    │
           │  Claude API  │    │  WhatsApp   │
           └──────────────┘    └─────────────┘
```

---

## Requisitos Previos

- **Python**: 3.11 o superior
- **pip**: Gestor de paquetes de Python
- **Cuentas necesarias**:
  - [Anthropic API Key](https://console.anthropic.com) (Claude AI)
  - [Twilio Account](https://www.twilio.com/try-twilio) (WhatsApp)
- **Opcional**: Git para control de versiones

---

## Instalación y Configuración

### 1. Clonar el Repositorio

```bash
git clone https://github.com/ferblanco75/chatbot-ai.git
cd chatbot-ai
```

### 2. Configurar el Backend

#### 2.1 Instalar Dependencias

```bash
cd backend
pip install -r requirements.txt
```

#### 2.2 Configurar Variables de Entorno

Copiar el archivo de ejemplo y editarlo con tus credenciales:

```bash
cp .env.example .env
```

Editar `backend/.env`:

```bash
# API Keys
ANTHROPIC_API_KEY=sk-ant-api03-TU_API_KEY_AQUI

# Twilio WhatsApp
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=tu_auth_token_aqui
TWILIO_WHATSAPP_FROM=whatsapp:+14155238886
TWILIO_TEST_NUMBER=+5492974XXXXXXX

# Admin
ADMIN_PASSWORD=comodoro2025

# CORS (separado por comas)
CORS_ORIGINS=https://tu-dominio.vercel.app,http://localhost:3000
```

#### 2.3 Iniciar el Servidor de Desarrollo

```bash
# Desde la carpeta backend/
uvicorn main:app --reload --port 8000
```

El backend estará disponible en:
- API: http://localhost:8000
- Documentación Swagger: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### 3. Configurar el Frontend

El frontend es estático (HTML/JS puro), no requiere instalación. Solo necesitas:

1. Abrir `index.html` en tu navegador (desarrollo local), o
2. Configurar la URL del backend en el código JavaScript

#### 3.1 Actualizar la URL del Backend

Editar `index.html` (buscar la variable `API_URL`):

```javascript
// En desarrollo local
const API_URL = 'http://localhost:8000';

// En producción
const API_URL = 'https://tu-backend.railway.app';
```

#### 3.2 Probar Localmente

```bash
# Opción 1: Abrir directamente
open index.html  # macOS
xdg-open index.html  # Linux

# Opción 2: Servidor HTTP simple
python -m http.server 3000
# Luego abrir http://localhost:3000
```

---

## Uso

### Widget del Chatbot (Frontend)

1. **Botón Flotante (FAB)**: Clic para abrir/cerrar el panel de chat
2. **Panel de Conversación**: Escribe tu consulta y presiona Enter
3. **Burbuja de Bienvenida**: Aparece automáticamente a los 3 segundos
4. **Chips de Respuesta Rápida**: Opciones predefinidas para consultas comunes

### Panel de Administración

Accede a `admin.html` para:
- Crear licitaciones manualmente
- Ver el caché de licitaciones scrapeadas
- Configurar notificaciones

### API REST (Backend)

#### Endpoints Principales

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `GET` | `/` | Health check |
| `POST` | `/chat/message` | Enviar mensaje al chatbot |
| `GET` | `/licitaciones` | Obtener todas las licitaciones |
| `POST` | `/licitaciones` | Crear licitación (requiere `ADMIN_PASSWORD`) |
| `GET` | `/proveedores?rubro=limpieza` | Buscar proveedores por rubro/localidad |
| `POST` | `/notificaciones/whatsapp` | Enviar notificación WhatsApp |

#### Ejemplo: Consulta al Chatbot

```bash
curl -X POST http://localhost:8000/chat/message \
  -H "Content-Type: application/json" \
  -d '{
    "message": "¿Cuáles son las licitaciones activas?",
    "conversation_history": []
  }'
```

Respuesta:

```json
{
  "response": "Actualmente hay 3 licitaciones activas:\n\n1. Licitación Pública N° 45/2025...",
  "conversation_history": [
    {"role": "user", "content": "¿Cuáles son las licitaciones activas?"},
    {"role": "assistant", "content": "Actualmente hay 3 licitaciones..."}
  ]
}
```

### Scraper Manual

Ejecutar el scraper para actualizar el caché de licitaciones:

```bash
cd backend
python -m services.scraper
```

---

## Estructura del Proyecto

```
chatbot-ai/
├── index.html              # Widget del chatbot (página principal)
├── admin.html              # Panel de administración
├── assets/
│   └── codi-avatar.svg     # Avatar del asistente (SVG optimizado)
├── backend/
│   ├── main.py             # Entry point FastAPI
│   ├── requirements.txt    # Dependencias Python (pinned)
│   ├── .env.example        # Template de variables de entorno
│   ├── routers/
│   │   ├── chat.py         # POST /chat/message (Claude API)
│   │   ├── licitaciones.py # GET/POST /licitaciones
│   │   ├── proveedores.py  # GET /proveedores (búsqueda CSV)
│   │   └── notificaciones.py # POST /notificaciones/whatsapp
│   ├── services/
│   │   ├── scraper.py      # Web scraper comodoro.gov.ar
│   │   └── whatsapp.py     # Twilio WhatsApp wrapper
│   └── data/
│       ├── proveedores.csv # 6.840 proveedores municipales
│       └── licitaciones.json # Caché del scraper
├── docs/
│   ├── architecture.md     # Arquitectura detallada
│   ├── development.md      # Guía de desarrollo
│   ├── issues-plan.md      # Roadmap y plan de issues
│   ├── codi-design-brief.md # Brief de diseño del personaje
│   └── guia-diseño-figma.md # Guía para diseñadores
├── CLAUDE.md               # Instrucciones para Claude Code
├── vercel.json             # Configuración de deploy en Vercel
├── render.yaml             # Configuración de deploy en Render
└── README.md               # Este archivo
```

---

## Deployment

### Frontend (Vercel)

El deploy a Vercel es automático desde GitHub:

1. Conectar el repositorio a Vercel
2. Configuración automática detecta `vercel.json`
3. Cada push a `master` despliega automáticamente

**Variables de entorno en Vercel**: No requiere (es estático)

**URL de ejemplo**: https://comodoro-asistente.vercel.app

### Backend (Railway)

#### Deploy con Railway

1. Instalar Railway CLI:
```bash
npm install -g @railway/cli
```

2. Login y deploy:
```bash
railway login
railway init
railway up
```

3. Configurar variables de entorno en el dashboard de Railway:
   - `ANTHROPIC_API_KEY`
   - `TWILIO_ACCOUNT_SID`
   - `TWILIO_AUTH_TOKEN`
   - `TWILIO_WHATSAPP_FROM`
   - `ADMIN_PASSWORD`
   - `CORS_ORIGINS` (incluir la URL de Vercel)

#### Deploy con Render

El archivo `render.yaml` ya está configurado:

1. Conectar repositorio en [Render Dashboard](https://dashboard.render.com)
2. Render detecta automáticamente `render.yaml`
3. Configurar variables de entorno en el dashboard
4. Deploy automático con cada push a `master`

---

## Tests

```bash
cd backend
pytest tests/ -v
```

**Nota**: Los tests no están implementados aún (issue #007 pendiente).

---

## Variables de Entorno

### Backend (`backend/.env`)

| Variable | Descripción | Ejemplo |
|----------|-------------|---------|
| `ANTHROPIC_API_KEY` | API Key de Claude (Anthropic) | `sk-ant-api03-...` |
| `TWILIO_ACCOUNT_SID` | Account SID de Twilio | `ACxxxxxxxx...` |
| `TWILIO_AUTH_TOKEN` | Auth Token de Twilio | `xxxxxxxx...` |
| `TWILIO_WHATSAPP_FROM` | Número WhatsApp de Twilio | `whatsapp:+14155238886` |
| `TWILIO_TEST_NUMBER` | Tu número de prueba | `+5492974XXXXXXX` |
| `ADMIN_PASSWORD` | Password para endpoints POST | `comodoro2025` |
| `CORS_ORIGINS` | Orígenes permitidos (separados por coma) | `https://example.com,http://localhost:3000` |

---

## Roadmap

- [x] **Issue #001**: Widget flotante HTML/CSS
- [x] **Issue #002**: Integración con Claude API
- [x] **Issue #003**: Scraper de licitaciones
- [x] **Issue #004**: Diseño en Figma (avatar + componentes)
- [ ] **Issue #005**: README completo + documentación (en curso)
- [ ] **Issue #006**: Deploy en Railway + Vercel
- [ ] **Issue #007**: Tests automatizados (pytest)
- [ ] **Issue #008**: Métricas y analytics
- [ ] **Issue #009**: Panel admin completo
- [ ] **Issue #010**: Notificaciones WhatsApp automáticas

Ver el roadmap completo en [docs/issues-plan.md](docs/issues-plan.md).

---

## Contribución

Las contribuciones son bienvenidas. Para cambios importantes:

1. Fork del repositorio
2. Crear una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit de tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abrir un Pull Request

**Convenciones de código**:
- Python: PEP 8, type hints obligatorios, docstrings en español
- Commits: Conventional Commits (feat, fix, docs, etc.)
- Mensajes y comentarios: español (voseo rioplatense)

---

## Licencia

Este proyecto está bajo la licencia MIT. Ver [LICENSE](LICENSE) para más detalles.

---

## Contacto y Soporte

**Municipalidad de Comodoro Rivadavia**
- Email: licitacionesyconcursos@comodoro.gov.ar
- Dirección: Namuncurá 26, Comodoro Rivadavia, Chubut
- Web oficial: https://www.comodoro.gov.ar

**Desarrollador**
- GitHub: [@ferblanco75](https://github.com/ferblanco75)
- Repositorio: https://github.com/ferblanco75/chatbot-ai
- Issues: https://github.com/ferblanco75/chatbot-ai/issues

---

## Normativa de Referencia

- **Ley Provincial II N°76**: Régimen de contrataciones del Estado Provincial
- **Ley N°4829**: "Compre Chubut" - Preferencia para proveedores locales
- **Pliego de Bases y Condiciones Generales (PBCG)**: Documento marco de licitaciones
- **Pliego de Bases y Condiciones Particulares (PBCP)**: Específico de cada licitación

---

## Agradecimientos

- [Boti (GCBA)](https://buenosaires.gob.ar/jefaturadegabinete/innovacion/boti) - Inspiración para el diseño del asistente
- [Anthropic](https://www.anthropic.com) - Claude AI
- [FastAPI](https://fastapi.tiangolo.com) - Framework web
- [Twilio](https://www.twilio.com) - WhatsApp API

---

**Desarrollado con Claude Code** 🤖

