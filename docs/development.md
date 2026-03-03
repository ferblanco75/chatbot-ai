# Guía de Desarrollo - Codi

Esta guía está dirigida a desarrolladores que quieran contribuir al proyecto o modificarlo para otros municipios.

---

## Tabla de Contenidos

- [Setup del Entorno de Desarrollo](#setup-del-entorno-de-desarrollo)
- [Estructura de Código](#estructura-de-código)
- [Convenciones de Código](#convenciones-de-código)
- [Flujo de Trabajo](#flujo-de-trabajo)
- [Testing](#testing)
- [Debugging](#debugging)
- [Deploy](#deploy)
- [Troubleshooting](#troubleshooting)
- [FAQ para Desarrolladores](#faq-para-desarrolladores)

---

## Setup del Entorno de Desarrollo

### Requisitos

- **Python 3.11+** (verificar con `python --version`)
- **pip** actualizado: `pip install --upgrade pip`
- **Git** para control de versiones
- **Editor recomendado**: VS Code con extensiones:
  - Python (Microsoft)
  - Pylance
  - Python Type Hint
  - FastAPI snippets

### 1. Clonar y Configurar

```bash
# Clonar repositorio
git clone https://github.com/ferblanco75/chatbot-ai.git
cd chatbot-ai

# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# Linux/Mac:
source venv/bin/activate
# Windows:
venv\Scripts\activate

# Instalar dependencias del backend
cd backend
pip install -r requirements.txt

# Volver a la raíz
cd ..
```

### 2. Configurar Variables de Entorno

```bash
# Copiar template
cp backend/.env.example backend/.env

# Editar con tu editor favorito
nano backend/.env  # o code backend/.env
```

**Variables obligatorias para desarrollo**:

```bash
# Anthropic API (obtener en https://console.anthropic.com)
ANTHROPIC_API_KEY=sk-ant-api03-XXXXXXXXXXXXXXXXXXXXXXX

# Twilio (obtener en https://www.twilio.com/console)
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_WHATSAPP_FROM=whatsapp:+14155238886
TWILIO_TEST_NUMBER=+5492974XXXXXXX  # Tu número de WhatsApp

# Admin
ADMIN_PASSWORD=comodoro2025

# CORS (localhost para desarrollo)
CORS_ORIGINS=http://localhost:3000,http://localhost:8000
```

### 3. Iniciar Servidores de Desarrollo

#### Terminal 1: Backend (FastAPI)

```bash
cd backend
uvicorn main:app --reload --port 8000
```

Salida esperada:
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [12345] using WatchFiles
INFO:     Started server process [12346]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

Abrir en navegador:
- API docs: http://localhost:8000/docs (Swagger UI)
- Alternative docs: http://localhost:8000/redoc

#### Terminal 2: Frontend (Servidor HTTP)

```bash
# Desde la raíz del proyecto
python -m http.server 3000
```

Abrir en navegador: http://localhost:3000

**Alternativa con Live Server** (VS Code):
1. Instalar extensión "Live Server"
2. Click derecho en `index.html` → "Open with Live Server"

### 4. Verificar que Todo Funciona

1. **Backend**: Ir a http://localhost:8000/docs y probar el endpoint `/health`
2. **Frontend**: Abrir http://localhost:3000, el widget debe aparecer
3. **Integración**: Escribir un mensaje en el chat y verificar respuesta

Si algo falla, ver [Troubleshooting](#troubleshooting).

---

## Estructura de Código

### Backend (FastAPI)

```
backend/
├── main.py                    # Entry point y configuración de la app
│   ├── FastAPI app instance
│   ├── CORS middleware
│   ├── Router registration
│   └── Health check endpoints
│
├── routers/                   # Endpoints REST (controllers)
│   ├── __init__.py
│   ├── chat.py               # POST /chat/message
│   │   └── Integración con Claude API
│   ├── licitaciones.py       # CRUD de licitaciones
│   │   ├── GET /licitaciones (listar)
│   │   ├── POST /licitaciones (crear)
│   │   └── GET /licitaciones/{id} (detalle)
│   ├── proveedores.py        # Búsqueda en CSV
│   │   └── GET /proveedores?rubro=X
│   └── notificaciones.py     # WhatsApp sender
│       └── POST /notificaciones/whatsapp
│
├── services/                  # Business logic (services)
│   ├── __init__.py
│   ├── scraper.py            # Web scraper
│   │   ├── scrape_licitaciones()
│   │   ├── parse_html()
│   │   └── save_to_json()
│   └── whatsapp.py           # Twilio wrapper
│       └── send_whatsapp_message()
│
├── data/                      # Archivos de datos
│   ├── proveedores.csv       # Padrón municipal (readonly)
│   └── licitaciones.json     # Caché del scraper (read/write)
│
├── requirements.txt           # Dependencias Python (pinned versions)
├── .env.example              # Template de variables de entorno
├── .env                      # Variables de entorno (gitignored)
└── .gitignore                # Archivos a ignorar en Git
```

### Frontend (HTML/CSS/JS)

```
/
├── index.html                 # Widget del chatbot
│   ├── <style> (CSS embebido)
│   │   ├── Variables CSS (:root)
│   │   ├── Estilos del FAB
│   │   ├── Estilos del panel de chat
│   │   └── Animaciones
│   └── <script> (JavaScript embebido)
│       ├── Estado global del widget
│       ├── Event listeners
│       ├── Funciones de UI (togglePanel, addMessage)
│       └── API calls (sendMessage)
│
├── admin.html                # Panel de administración
│   └── Formulario para crear licitaciones
│
└── assets/
    └── codi-avatar.svg       # Avatar del asistente
```

**Nota**: El HTML, CSS y JS están en el mismo archivo (`index.html`) para simplicidad de deploy. No hay build step ni bundler.

---

## Convenciones de Código

### Python (Backend)

#### 1. Estilo: PEP 8

```python
# ✅ BUENO: snake_case para funciones y variables
def get_licitaciones_activas():
    licitacion_id = "L-2025-001"

# ❌ MALO: camelCase
def getLicitacionesActivas():
    licitacionId = "L-2025-001"
```

#### 2. Type Hints Obligatorios

```python
# ✅ BUENO: Type hints en función
from typing import List, Optional

def buscar_proveedores(rubro: str, limit: int = 50) -> List[dict]:
    """Busca proveedores por rubro."""
    ...

# ❌ MALO: Sin type hints
def buscar_proveedores(rubro, limit=50):
    ...
```

#### 3. Docstrings en Español

```python
# ✅ BUENO: Docstring completo en español
def scrape_licitaciones() -> List[dict]:
    """
    Scrapea licitaciones desde comodoro.gov.ar.

    Returns:
        Lista de diccionarios con datos de licitaciones.

    Raises:
        HTTPError: Si el sitio no responde después de 3 reintentos.
    """
    ...

# ❌ MALO: Sin docstring o en inglés
def scrape_licitaciones():
    """Scrapes bids from website."""  # En inglés
    ...
```

#### 4. Modelos Pydantic para Validación

```python
# ✅ BUENO: Modelo con validación
from pydantic import BaseModel, Field

class Licitacion(BaseModel):
    numero: str = Field(..., min_length=1, max_length=50)
    titulo: str = Field(..., min_length=10)
    monto_estimado: Optional[float] = Field(None, ge=0)

# ❌ MALO: Dict sin validación
def create_licitacion(data: dict):
    ...
```

#### 5. Logging en lugar de Print

```python
# ✅ BUENO: Usar logging
import logging

logger = logging.getLogger(__name__)

def scraper():
    logger.info("Iniciando scraper de licitaciones")
    logger.error("Error al conectar con el sitio: %s", error)

# ❌ MALO: Usar print
def scraper():
    print("Iniciando scraper...")  # No usar en producción
```

### JavaScript (Frontend)

#### 1. Variables: const > let > nunca var

```javascript
// ✅ BUENO
const API_URL = 'http://localhost:8000';
let isTyping = false;

// ❌ MALO
var API_URL = 'http://localhost:8000';  // Nunca usar var
```

#### 2. Funciones Async/Await

```javascript
// ✅ BUENO: async/await
async function sendMessage(message) {
  try {
    const response = await fetch(`${API_URL}/chat/message`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message })
    });
    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Error al enviar mensaje:', error);
    throw error;
  }
}

// ❌ MALO: Callbacks anidados
function sendMessage(message, callback) {
  fetch(API_URL + '/chat/message', {
    method: 'POST',
    body: JSON.stringify({ message })
  })
  .then(response => response.json())
  .then(data => callback(null, data))
  .catch(err => callback(err));
}
```

#### 3. Template Literals para Strings

```javascript
// ✅ BUENO: Template literals
const message = `Licitación N° ${numero} - ${titulo}`;

// ❌ MALO: Concatenación
const message = 'Licitación N° ' + numero + ' - ' + titulo;
```

#### 4. Nombres en Español (voseo rioplatense)

```javascript
// ✅ BUENO: Mensajes en español con voseo
const BIENVENIDA = '¡Hola! Soy Codi. ¿En qué puedo ayudarte?';

function mostrarError() {
  alert('Disculpá, hubo un error. Intentá nuevamente.');
}

// ❌ MALO: Mensajes en inglés o español formal
const WELCOME = 'Hello! I am Codi';
function showError() {
  alert('Disculpe, hubo un error');  // "Disculpe" es formal
}
```

### Git Commits

Seguimos **Conventional Commits**:

```bash
# Formato: <tipo>(<scope>): <descripción>

# Tipos:
# - feat: Nueva funcionalidad
# - fix: Corrección de bug
# - docs: Documentación
# - style: Formato (sin cambios de lógica)
# - refactor: Refactorización
# - test: Tests
# - chore: Tareas de mantenimiento

# Ejemplos:
git commit -m "feat(chat): agregar soporte para imágenes en respuestas"
git commit -m "fix(scraper): corregir parsing de fechas con formato DD/MM/YYYY"
git commit -m "docs(readme): actualizar instrucciones de deploy"
git commit -m "refactor(proveedores): optimizar búsqueda con índices"
```

---

## Flujo de Trabajo

### Trabajar en un Nuevo Feature

```bash
# 1. Crear rama desde develop
git checkout develop
git pull origin develop
git checkout -b feature/nombre-del-feature

# 2. Hacer cambios
# ... editar archivos ...

# 3. Commit frecuentes
git add .
git commit -m "feat(scope): descripción del cambio"

# 4. Pushear a GitHub
git push origin feature/nombre-del-feature

# 5. Crear Pull Request en GitHub
# Ir a github.com/ferblanco75/chatbot-ai/pulls
# Click "New Pull Request"
# Base: develop ← Compare: feature/nombre-del-feature
```

### Estructura de Branches

```
master (producción)
  └── develop (desarrollo)
        ├── feature/nueva-funcionalidad-1
        ├── feature/nueva-funcionalidad-2
        └── fix/correccion-bug-x
```

**Reglas**:
- `master`: Solo código en producción (protegido)
- `develop`: Integración de features (rama principal de desarrollo)
- `feature/*`: Nuevas funcionalidades
- `fix/*`: Correcciones de bugs
- `docs/*`: Cambios solo de documentación

---

## Testing

### Backend: pytest

#### Instalación

```bash
cd backend
pip install pytest pytest-asyncio httpx
```

#### Crear Tests

```python
# backend/tests/test_licitaciones.py
import pytest
from httpx import AsyncClient
from main import app

@pytest.mark.asyncio
async def test_get_licitaciones():
    """Test GET /licitaciones retorna lista."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/licitaciones")

    assert response.status_code == 200
    data = response.json()
    assert "licitaciones" in data
    assert isinstance(data["licitaciones"], list)

@pytest.mark.asyncio
async def test_create_licitacion_sin_auth():
    """Test POST /licitaciones sin password falla."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post("/licitaciones", json={
            "numero": "L-2025-999",
            "titulo": "Test"
        })

    assert response.status_code == 401  # Unauthorized
```

#### Ejecutar Tests

```bash
cd backend
pytest tests/ -v
```

**Output esperado**:
```
tests/test_licitaciones.py::test_get_licitaciones PASSED
tests/test_licitaciones.py::test_create_licitacion_sin_auth PASSED

==================== 2 passed in 0.45s ====================
```

### Frontend: Tests Manuales

**Checklist de testing manual**:

- [ ] Widget aparece en la esquina inferior derecha
- [ ] FAB tiene animación de pulse
- [ ] Click en FAB abre/cierra el panel
- [ ] Burbuja de bienvenida aparece a los 3 segundos
- [ ] Enviar mensaje muestra typing indicator
- [ ] Respuesta del bot se renderiza correctamente
- [ ] Chips de respuesta rápida funcionan
- [ ] Scroll automático al último mensaje
- [ ] Panel se adapta a mobile (< 480px)
- [ ] LocalStorage persiste conversación al recargar

**Testing en múltiples navegadores**:
- Chrome/Edge (Chromium)
- Firefox
- Safari (si usas Mac)
- Mobile (usar DevTools → Toggle Device Toolbar)

---

## Debugging

### Backend (FastAPI)

#### Logs en Consola

```python
# En cualquier router o service
import logging

logger = logging.getLogger(__name__)

@router.post("/chat/message")
async def chat_message(request: ChatRequest):
    logger.info(f"Mensaje recibido: {request.message[:50]}...")  # Primeros 50 chars

    # ... lógica ...

    logger.info(f"Tokens usados: input={usage.input_tokens}, output={usage.output_tokens}")
    return response
```

Ver logs en la terminal donde corre `uvicorn`.

#### Debugger de VS Code

Crear `.vscode/launch.json`:

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "FastAPI",
      "type": "python",
      "request": "launch",
      "module": "uvicorn",
      "args": [
        "backend.main:app",
        "--reload",
        "--port",
        "8000"
      ],
      "jinja": true,
      "justMyCode": true
    }
  ]
}
```

Luego: F5 para iniciar debug, poner breakpoints con click en la línea.

### Frontend (JavaScript)

#### Console.log

```javascript
// En sendMessage()
async function sendMessage(message) {
  console.log('Enviando mensaje:', message);

  const response = await fetch(`${API_URL}/chat/message`, {
    method: 'POST',
    body: JSON.stringify({ message, conversation_history: state.conversation })
  });

  console.log('Respuesta recibida:', response.status);
  const data = await response.json();
  console.log('Data parseada:', data);

  return data;
}
```

Ver logs en: DevTools → Console (F12)

#### Breakpoints en DevTools

1. Abrir DevTools (F12)
2. Ir a la pestaña "Sources"
3. Buscar `index.html`
4. Click en el número de línea para agregar breakpoint
5. Interactuar con el widget para triggear el breakpoint

#### Network Tab

Para ver requests HTTP:
1. DevTools → Network
2. Filtrar por "Fetch/XHR"
3. Enviar mensaje en el chat
4. Ver request a `/chat/message` con:
   - Headers
   - Payload (body enviado)
   - Response (data recibida)

---

## Deploy

### Deploy del Frontend (Vercel)

#### Primera vez (desde GitHub)

1. Ir a [vercel.com](https://vercel.com) y crear cuenta
2. Click "New Project"
3. Importar repositorio `ferblanco75/chatbot-ai`
4. Configuración:
   - Framework Preset: **Other**
   - Root Directory: `.` (raíz)
   - Build Command: (vacío)
   - Output Directory: `.` (raíz)
5. Click "Deploy"

**URL generada**: https://chatbot-ai-XXXX.vercel.app

#### Configurar Dominio Personalizado (opcional)

1. En Vercel dashboard → Settings → Domains
2. Agregar `comodoro-asistente.vercel.app` (o tu dominio)
3. Verificar DNS

#### Deploy Automático

Cada push a `master` despliega automáticamente. Ver status en GitHub → Actions.

### Deploy del Backend (Railway)

#### Primera vez

```bash
# Instalar Railway CLI
npm install -g @railway/cli

# Login
railway login

# Inicializar proyecto (desde la carpeta raíz)
railway init

# Seleccionar "backend" como root directory
# Esto creará un railway.toml

# Deploy
railway up
```

**URL generada**: https://chatbot-backend-production-XXXX.up.railway.app

#### Configurar Variables de Entorno

```bash
# Opción 1: CLI
railway variables set ANTHROPIC_API_KEY=sk-ant-...
railway variables set TWILIO_ACCOUNT_SID=AC...
railway variables set TWILIO_AUTH_TOKEN=...
railway variables set ADMIN_PASSWORD=comodoro2025
railway variables set CORS_ORIGINS=https://tu-frontend.vercel.app

# Opción 2: Dashboard
# Ir a railway.app → tu proyecto → Variables
# Agregar cada variable manualmente
```

#### Deploy Automático

Railway hace deploy automático con cada push a `master` (si conectaste el repo GitHub).

### Deploy Alternativo (Render)

Si preferís Render en lugar de Railway:

1. Ir a [render.com](https://render.com) y crear cuenta
2. Click "New +" → "Web Service"
3. Conectar repositorio GitHub
4. Configuración:
   - Name: `chatbot-comodoro-backend`
   - Environment: **Python 3**
   - Root Directory: `backend`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
5. Agregar variables de entorno (Environment)
6. Click "Create Web Service"

**Nota**: Render detecta automáticamente `render.yaml` si está en la raíz.

---

## Troubleshooting

### Problema: "ModuleNotFoundError: No module named 'fastapi'"

**Causa**: Dependencias no instaladas o entorno virtual no activado.

**Solución**:
```bash
# Verificar que el entorno virtual esté activado
which python  # Debe mostrar .../venv/bin/python

# Si no está activado:
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Reinstalar dependencias
cd backend
pip install -r requirements.txt
```

### Problema: "403 Forbidden" al llamar a Claude API

**Causa**: API key inválida o sin créditos.

**Solución**:
1. Verificar API key en `.env`
2. Ir a https://console.anthropic.com → Settings → API Keys
3. Verificar que la key sea válida y tenga créditos

### Problema: CORS error en el frontend

**Error en consola**:
```
Access to fetch at 'http://localhost:8000/chat/message' from origin 'http://localhost:3000'
has been blocked by CORS policy
```

**Causa**: Backend no permite requests desde el origen del frontend.

**Solución**:
```bash
# Editar backend/.env
CORS_ORIGINS=http://localhost:3000,http://localhost:8000

# Reiniciar el servidor backend
```

### Problema: "Address already in use" al iniciar uvicorn

**Causa**: Puerto 8000 ya está siendo usado por otro proceso.

**Solución**:
```bash
# Opción 1: Matar el proceso en puerto 8000
# Linux/Mac:
lsof -ti:8000 | xargs kill -9

# Windows:
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Opción 2: Usar otro puerto
uvicorn main:app --reload --port 8001
```

### Problema: Widget no aparece en el frontend

**Checklist**:
1. ¿El servidor HTTP está corriendo? (puerto 3000)
2. ¿Hay errores en la consola del navegador? (F12)
3. ¿El archivo `assets/codi-avatar.svg` existe?
4. ¿El CSS está cargando? (ver DevTools → Elements)

**Debug**:
```javascript
// Agregar en index.html al final del <script>
console.log('Widget cargado correctamente');
```

Si ves el log, el problema es de CSS. Si no, hay un error de JS.

---

## FAQ para Desarrolladores

### ¿Cómo agrego un nuevo endpoint al backend?

1. Crear archivo en `backend/routers/mi_endpoint.py`:
```python
from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def mi_funcion():
    return {"mensaje": "Hola"}
```

2. Registrar en `backend/main.py`:
```python
from routers import mi_endpoint

app.include_router(mi_endpoint.router, prefix="/mi-endpoint", tags=["mi-tag"])
```

3. Probar en http://localhost:8000/docs

### ¿Cómo cambio el diseño del widget?

Todo el CSS está en `index.html` dentro de la etiqueta `<style>`. Buscar la sección que querés modificar:

```css
/* Ejemplo: Cambiar color del FAB */
#chat-fab {
  background: linear-gradient(135deg, #1055A8, #0B2347);
  /* Cambiar a otro color: */
  background: linear-gradient(135deg, #FF5722, #E91E63);
}
```

Refrescar el navegador (Ctrl+Shift+R) para ver cambios.

### ¿Cómo agrego un nuevo rubro de proveedores?

El archivo `backend/data/proveedores.csv` es de solo lectura (cargado en memoria). Para agregar rubros:

1. Editar el CSV directamente (Excel, LibreOffice)
2. Guardar con codificación UTF-8
3. Reiniciar el backend (uvicorn recarga el CSV)

**Formato del CSV**:
```csv
cuit,razon_social,rubro,localidad
20-12345678-9,Empresa SA,limpieza,Comodoro Rivadavia
```

### ¿Cómo cambio el tono de voz de Codi?

Editar el **system prompt** en `backend/routers/chat.py`:

```python
system_prompt = """
Sos Codi, asistente virtual de la Municipalidad de Comodoro Rivadavia.

Personalidad:
- Amigable y cercano (usá voseo: "podés", "consultá")
- Profesional pero no distante
- Paciente y didáctico

[... resto del prompt ...]
"""
```

### ¿Cómo pruebo las notificaciones WhatsApp sin enviar mensajes reales?

**Opción 1**: Usar el WhatsApp Sandbox de Twilio (solo envía a números opt-in)

**Opción 2**: Mockear el servicio en tests:
```python
# tests/test_notificaciones.py
from unittest.mock import patch

@patch('services.whatsapp.send_whatsapp_message')
def test_enviar_notificacion(mock_send):
    mock_send.return_value = True
    # ... test code ...
    assert mock_send.called
```

### ¿Cómo migro de Railway a Render (o viceversa)?

Ambos son PaaS compatibles con el mismo código. Pasos:

1. Crear nuevo servicio en la plataforma de destino
2. Conectar mismo repositorio GitHub
3. Copiar variables de entorno del dashboard original
4. Verificar que `render.yaml` o Railway config exista
5. Deploy

No hay cambios de código necesarios.

---

## Recursos Adicionales

- [FastAPI Tutorial](https://fastapi.tiangolo.com/tutorial/)
- [Anthropic Claude API Docs](https://docs.anthropic.com/en/api)
- [Twilio Python Quickstart](https://www.twilio.com/docs/libraries/python)
- [MDN Web Docs (JavaScript)](https://developer.mozilla.org/es/)
- [Python Type Hints Cheat Sheet](https://mypy.readthedocs.io/en/stable/cheat_sheet_py3.html)

---

**Si encontrás un bug o tenés una duda**, abrir un issue en GitHub: https://github.com/ferblanco75/chatbot-ai/issues

**Última actualización**: 2026-03-03
**Versión**: 1.0.0
