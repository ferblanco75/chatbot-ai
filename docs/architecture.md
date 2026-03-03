# Arquitectura Técnica - Codi

Este documento describe la arquitectura completa del sistema de asistente virtual para licitaciones municipales.

---

## Tabla de Contenidos

- [Visión General](#visión-general)
- [Arquitectura de Alto Nivel](#arquitectura-de-alto-nivel)
- [Frontend (Cliente)](#frontend-cliente)
- [Backend (Servidor)](#backend-servidor)
- [Flujos de Datos](#flujos-de-datos)
- [Integraciones Externas](#integraciones-externas)
- [Seguridad](#seguridad)
- [Escalabilidad](#escalabilidad)
- [Decisiones Arquitectónicas](#decisiones-arquitectónicas)

---

## Visión General

**Codi** es una aplicación web de dos capas (frontend estático + backend API) que utiliza inteligencia artificial (Claude AI) para responder consultas sobre licitaciones municipales.

### Principios de Diseño

1. **Simplicidad**: Sin frameworks frontend, sin bases de datos complejas
2. **Escalabilidad**: Backend stateless, fácil de escalar horizontalmente
3. **Costo-eficiencia**: Infraestructura serverless/PaaS, sin servidores dedicados
4. **Mantenibilidad**: Código simple, type-safe, bien documentado

### Stack Resumido

| Capa | Tecnología | Deploy |
|------|------------|--------|
| Frontend | HTML/CSS/JS vanilla | Vercel (CDN) |
| Backend | FastAPI (Python 3.11) | Railway/Render |
| IA | Claude Sonnet 4.5 | Anthropic API |
| Notificaciones | WhatsApp | Twilio API |
| Scraping | httpx + BeautifulSoup4 | Cron job en backend |

---

## Arquitectura de Alto Nivel

```
┌─────────────────────────────────────────────────────────────────┐
│                         INTERNET                                 │
└─────────────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
┌───────▼──────┐    ┌─────────▼──────┐    ┌────────▼──────┐
│   Browser    │    │  Mobile Web    │    │   WhatsApp    │
│  (Desktop)   │    │   (Mobile)     │    │   (Users)     │
└───────┬──────┘    └─────────┬──────┘    └────────┬──────┘
        │                     │                     │
        └─────────────────────┼─────────────────────┘
                              │
        ┌─────────────────────▼─────────────────────┐
        │         CDN (Vercel Edge Network)          │
        │    ┌────────────────────────────────┐     │
        │    │  index.html + assets (static)  │     │
        │    └────────────────────────────────┘     │
        └─────────────────────┬─────────────────────┘
                              │
                        HTTPS │ REST API
                              │
        ┌─────────────────────▼─────────────────────┐
        │      Backend (Railway/Render)             │
        │  ┌─────────────────────────────────────┐  │
        │  │       FastAPI Application           │  │
        │  │  ┌─────────────────────────────┐    │  │
        │  │  │  Uvicorn ASGI Server        │    │  │
        │  │  │  (Port: 8000)               │    │  │
        │  │  └─────────────────────────────┘    │  │
        │  │                                     │  │
        │  │  ┌─────────────────────────────┐    │  │
        │  │  │  Routers                    │    │  │
        │  │  │  - /chat                    │    │  │
        │  │  │  - /licitaciones            │    │  │
        │  │  │  - /proveedores             │    │  │
        │  │  │  - /notificaciones          │    │  │
        │  │  └─────────────────────────────┘    │  │
        │  │                                     │  │
        │  │  ┌─────────────────────────────┐    │  │
        │  │  │  Services                   │    │  │
        │  │  │  - scraper.py               │    │  │
        │  │  │  - whatsapp.py              │    │  │
        │  │  └─────────────────────────────┘    │  │
        │  └─────────────────────────────────────┘  │
        │                                           │
        │  ┌─────────────────────────────────────┐  │
        │  │  Data (Filesystem)                  │  │
        │  │  - proveedores.csv (6.840 rows)     │  │
        │  │  - licitaciones.json (cache)        │  │
        │  └─────────────────────────────────────┘  │
        └─────────────────────┬─────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
┌───────▼──────┐    ┌─────────▼──────┐    ┌────────▼──────┐
│  Anthropic   │    │  Twilio        │    │ comodoro.gov  │
│  Claude API  │    │  WhatsApp API  │    │ (scraping)    │
└──────────────┘    └────────────────┘    └───────────────┘
```

---

## Frontend (Cliente)

### Estructura del Widget

El frontend es un **widget embebible** que se puede integrar en cualquier sitio web municipal.

#### Componentes Principales

```
┌─────────────────────────────────────────┐
│   Sitio Web Municipal (cualquier CMS)   │
│                                         │
│  ┌────────────────────────────────────┐ │
│  │  Contenido existente del sitio     │ │
│  │  (noticias, trámites, etc.)        │ │
│  └────────────────────────────────────┘ │
│                                         │
│  ┌─────────────────────────────────┐   │
│  │  Widget Codi (index.html)       │   │
│  │                                 │   │
│  │  ┌────────────────────────┐     │   │
│  │  │  FAB (Botón Flotante)  │     │   │
│  │  │  - Avatar de Codi      │     │   │
│  │  │  - Badge de notif      │     │   │
│  │  │  - Animación pulse     │     │   │
│  │  └────────────────────────┘     │   │
│  │                                 │   │
│  │  ┌────────────────────────────┐ │   │
│  │  │  Panel de Chat (oculto)    │ │   │
│  │  │  ┌──────────────────────┐  │ │   │
│  │  │  │  Header              │  │ │   │
│  │  │  │  - Avatar + Nombre   │  │ │   │
│  │  │  │  - Botón cerrar      │  │ │   │
│  │  │  └──────────────────────┘  │ │   │
│  │  │  ┌──────────────────────┐  │ │   │
│  │  │  │  Área de Mensajes    │  │ │   │
│  │  │  │  - Burbuja Bot       │  │ │   │
│  │  │  │  - Burbuja Usuario   │  │ │   │
│  │  │  │  - Chips (opciones)  │  │ │   │
│  │  │  │  - Typing indicator  │  │ │   │
│  │  │  └──────────────────────┘  │ │   │
│  │  │  ┌──────────────────────┐  │ │   │
│  │  │  │  Input de Usuario    │  │ │   │
│  │  │  │  - Textarea          │  │ │   │
│  │  │  │  - Botón enviar      │  │ │   │
│  │  │  └──────────────────────┘  │ │   │
│  │  └────────────────────────────┘ │   │
│  │                                 │   │
│  │  ┌────────────────────────────┐ │   │
│  │  │  Burbuja de Bienvenida     │ │   │
│  │  │  (aparece a los 3s)        │ │   │
│  │  └────────────────────────────┘ │   │
│  └─────────────────────────────────┘   │
└─────────────────────────────────────────┘
```

#### Tecnologías Frontend

- **HTML5**: Estructura semántica
- **CSS3**: Variables CSS, Grid, Flexbox, animations
- **JavaScript (ES6+)**:
  - Fetch API para llamadas HTTP
  - LocalStorage para persistencia de conversación
  - Event delegation para performance
  - No dependencias externas (0 KB de node_modules)

#### Gestión de Estado

```javascript
// Estado global del widget (in-memory)
const state = {
  isOpen: false,              // Panel abierto/cerrado
  conversation: [],           // Historial de mensajes
  isTyping: false,            // Indicador de carga
  currentSessionId: null      // ID de sesión (UUID)
};

// Persistencia en LocalStorage
localStorage.setItem('codi_conversation', JSON.stringify(conversation));
```

#### Comunicación con el Backend

```javascript
// Endpoint configurado dinámicamente
const API_URL = 'https://chatbot-backend.railway.app';

// POST /chat/message
async function sendMessage(message) {
  const response = await fetch(`${API_URL}/chat/message`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      message: message,
      conversation_history: state.conversation
    })
  });
  const data = await response.json();
  return data;
}
```

---

## Backend (Servidor)

### Arquitectura FastAPI

FastAPI sigue el patrón **router-based modular architecture**:

```
backend/
├── main.py                    # Entry point
├── routers/                   # Endpoints REST
│   ├── chat.py               # POST /chat/message
│   ├── licitaciones.py       # CRUD licitaciones
│   ├── proveedores.py        # Búsqueda proveedores
│   └── notificaciones.py     # WhatsApp sender
├── services/                  # Business logic
│   ├── scraper.py            # Web scraping
│   └── whatsapp.py           # Twilio wrapper
├── data/                      # Archivos de datos
│   ├── proveedores.csv       # Padrón municipal
│   └── licitaciones.json     # Caché de licitaciones
└── requirements.txt           # Dependencias pinned
```

### Routers (Endpoints)

#### 1. `/chat` - Conversación con Claude

```python
# routers/chat.py
from anthropic import Anthropic

@router.post("/message")
async def chat_message(request: ChatRequest):
    """
    Procesa un mensaje del usuario y devuelve respuesta de Claude.

    Flow:
    1. Recibe mensaje + historial de conversación
    2. Construye contexto con datos de licitaciones
    3. Llama a Claude API con system prompt
    4. Retorna respuesta + historial actualizado
    """
    client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

    # System prompt con contexto municipal
    system_prompt = """
    Sos Codi, asistente virtual de la Municipalidad de Comodoro Rivadavia.
    Tu función es ayudar con consultas sobre licitaciones públicas.
    [... contexto adicional ...]
    """

    # Construir mensajes para Claude
    messages = build_messages(request.conversation_history, request.message)

    # Llamar a Claude API
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        system=system_prompt,
        messages=messages
    )

    return {
        "response": response.content[0].text,
        "conversation_history": updated_history
    }
```

**Consideraciones de diseño**:
- Stateless: El historial de conversación se envía en cada request (no hay sesiones en servidor)
- Timeout: 30 segundos máximo por request (límite de Railway/Render)
- Retry: No implementado (el frontend debe manejar errores de red)

#### 2. `/licitaciones` - CRUD de Licitaciones

```python
# routers/licitaciones.py

# Modelo de datos
class Licitacion(BaseModel):
    id: str
    numero: str
    titulo: str
    organismo: str
    fecha_publicacion: str
    fecha_apertura: str
    monto_estimado: Optional[float]
    estado: str  # "activa", "cerrada", "suspendida"
    url_pliego: Optional[str]
    descripcion: str

# Endpoints
@router.get("/")
async def get_licitaciones(
    estado: Optional[str] = None,
    desde: Optional[str] = None
):
    """
    Obtiene licitaciones desde el JSON cache.
    Soporta filtrado por estado y fecha.
    """
    # Leer archivo JSON
    with open("data/licitaciones.json") as f:
        data = json.load(f)

    # Filtrar
    licitaciones = filter_licitaciones(data, estado, desde)

    return {"licitaciones": licitaciones, "total": len(licitaciones)}

@router.post("/")
async def create_licitacion(
    licitacion: Licitacion,
    password: str = Header(None)
):
    """
    Crea una licitación manualmente (requiere ADMIN_PASSWORD).
    Usado desde el panel admin.html.
    """
    # Validar password
    if password != os.getenv("ADMIN_PASSWORD"):
        raise HTTPException(status_code=401, detail="Unauthorized")

    # Agregar al JSON
    with open("data/licitaciones.json", "r+") as f:
        data = json.load(f)
        data["licitaciones"].append(licitacion.dict())
        f.seek(0)
        json.dump(data, f, indent=2)

    return {"message": "Licitación creada", "id": licitacion.id}
```

**Persistencia**:
- Archivo JSON en filesystem (no base de datos)
- **Limitación conocida**: No apto para alta concurrencia (race conditions en escritura)
- **Solución futura**: Migrar a PostgreSQL si se necesita multi-usuario

#### 3. `/proveedores` - Búsqueda en CSV

```python
# routers/proveedores.py
import pandas as pd

# Cargar CSV en memoria al inicio (singleton)
PROVEEDORES_DF = pd.read_csv("data/proveedores.csv")

@router.get("/")
async def buscar_proveedores(
    rubro: Optional[str] = None,
    localidad: Optional[str] = None,
    cuit: Optional[str] = None,
    limit: int = 50
):
    """
    Busca proveedores en el padrón municipal.
    Búsqueda por rubro, localidad o CUIT.
    """
    df = PROVEEDORES_DF

    # Filtros acumulativos
    if rubro:
        df = df[df['rubro'].str.contains(rubro, case=False, na=False)]
    if localidad:
        df = df[df['localidad'].str.contains(localidad, case=False, na=False)]
    if cuit:
        df = df[df['cuit'] == cuit]

    # Limitar resultados
    df = df.head(limit)

    return {
        "proveedores": df.to_dict(orient="records"),
        "total": len(df)
    }
```

**Performance**:
- CSV (6.840 filas) cargado en memoria: ~500 KB RAM
- Búsqueda con pandas: < 10 ms
- No se necesita base de datos para este volumen

#### 4. `/notificaciones` - WhatsApp vía Twilio

```python
# routers/notificaciones.py
from services.whatsapp import send_whatsapp_message

@router.post("/whatsapp")
async def enviar_notificacion(request: NotificacionRequest):
    """
    Envía notificación de nueva licitación por WhatsApp.
    Requiere ADMIN_PASSWORD.
    """
    # Validar autenticación
    if request.password != os.getenv("ADMIN_PASSWORD"):
        raise HTTPException(status_code=401)

    # Enviar WhatsApp
    result = send_whatsapp_message(
        to=request.telefono,
        message=request.mensaje
    )

    return {"status": "sent", "sid": result.sid}
```

### Services (Lógica de Negocio)

#### Scraper de Licitaciones

```python
# services/scraper.py
import httpx
from bs4 import BeautifulSoup

async def scrape_licitaciones():
    """
    Scraper de https://www.comodoro.gov.ar/secciones/licitaciones/

    Flow:
    1. GET HTML de la página
    2. Parse con BeautifulSoup4
    3. Extraer tabla de licitaciones
    4. Convertir a JSON
    5. Guardar en data/licitaciones.json

    Retry: 3 intentos con backoff exponencial
    """
    url = "https://www.comodoro.gov.ar/secciones/licitaciones/"

    async with httpx.AsyncClient(timeout=30.0) as client:
        # Retry logic
        for attempt in range(3):
            try:
                response = await client.get(url)
                response.raise_for_status()
                break
            except httpx.HTTPError as e:
                if attempt == 2:
                    raise
                await asyncio.sleep(2 ** attempt)  # 1s, 2s, 4s

    # Parse HTML
    soup = BeautifulSoup(response.text, 'html.parser')
    tabla = soup.find('table', class_='licitaciones')

    # Extraer licitaciones
    licitaciones = []
    for row in tabla.find_all('tr')[1:]:  # Skip header
        cols = row.find_all('td')
        licitaciones.append({
            "numero": cols[0].text.strip(),
            "titulo": cols[1].text.strip(),
            "fecha_publicacion": cols[2].text.strip(),
            # ... más campos
        })

    # Guardar en JSON
    with open("data/licitaciones.json", "w") as f:
        json.dump({"licitaciones": licitaciones}, f, indent=2)

    return licitaciones
```

**Ejecución**:
- Manual: `python -m services.scraper`
- Automatizado: Cron job en Railway/Render (1 vez por día)

#### WhatsApp con Twilio

```python
# services/whatsapp.py
from twilio.rest import Client

def send_whatsapp_message(to: str, message: str):
    """
    Wrapper de Twilio WhatsApp API.

    Args:
        to: Número con formato E.164 (+5492974XXXXXXX)
        message: Texto del mensaje

    Returns:
        MessageInstance de Twilio
    """
    client = Client(
        os.getenv("TWILIO_ACCOUNT_SID"),
        os.getenv("TWILIO_AUTH_TOKEN")
    )

    message = client.messages.create(
        from_=os.getenv("TWILIO_WHATSAPP_FROM"),  # whatsapp:+14155238886
        to=f"whatsapp:{to}",
        body=message
    )

    return message
```

**Limitaciones de WhatsApp Sandbox**:
- Requiere opt-in del usuario (enviar "join <palabra>" primero)
- Solo para desarrollo/testing
- Producción requiere **WhatsApp Business API** (proceso de aprobación de Meta)

---

## Flujos de Datos

### Flujo 1: Consulta de Licitación

```
┌─────────┐                ┌─────────┐                ┌──────────┐                ┌──────────┐
│ Usuario │                │ Browser │                │ Backend  │                │ Claude   │
└────┬────┘                └────┬────┘                └────┬─────┘                └────┬─────┘
     │                          │                          │                           │
     │ 1. Escribe mensaje       │                          │                           │
     │ "¿Cuáles son las         │                          │                           │
     │  licitaciones activas?"  │                          │                           │
     ├─────────────────────────>│                          │                           │
     │                          │                          │                           │
     │                          │ 2. POST /chat/message    │                           │
     │                          │    {message: "...",      │                           │
     │                          │     history: [...]}      │                           │
     │                          ├─────────────────────────>│                           │
     │                          │                          │                           │
     │                          │                          │ 3. Cargar licitaciones   │
     │                          │                          │    desde JSON             │
     │                          │                          ├────┐                      │
     │                          │                          │    │                      │
     │                          │                          │<───┘                      │
     │                          │                          │                           │
     │                          │                          │ 4. Construir system      │
     │                          │                          │    prompt con contexto   │
     │                          │                          ├────┐                      │
     │                          │                          │    │                      │
     │                          │                          │<───┘                      │
     │                          │                          │                           │
     │                          │                          │ 5. POST /messages        │
     │                          │                          │    (Claude API)          │
     │                          │                          ├──────────────────────────>│
     │                          │                          │                           │
     │                          │                          │                           │ 6. Procesar
     │                          │                          │                           │    con LLM
     │                          │                          │                           ├────┐
     │                          │                          │                           │    │
     │                          │                          │                           │<───┘
     │                          │                          │                           │
     │                          │                          │ 7. Respuesta             │
     │                          │                          │    JSON con texto        │
     │                          │                          │<──────────────────────────┤
     │                          │                          │                           │
     │                          │ 8. Response con          │                           │
     │                          │    respuesta + history   │                           │
     │                          │<─────────────────────────┤                           │
     │                          │                          │                           │
     │ 9. Renderizar burbuja    │                          │                           │
     │    del bot con texto     │                          │                           │
     │<─────────────────────────┤                          │                           │
     │                          │                          │                           │
```

**Tiempo de respuesta típico**: 2-5 segundos (mayoría es latencia de Claude API)

### Flujo 2: Scraping Automático

```
┌──────────┐         ┌──────────┐         ┌──────────────┐
│ Cron Job │         │ Scraper  │         │ comodoro.gov │
└────┬─────┘         └────┬─────┘         └──────┬───────┘
     │                    │                       │
     │ 1. Trigger diario  │                       │
     │    (ej: 6:00 AM)   │                       │
     ├───────────────────>│                       │
     │                    │                       │
     │                    │ 2. GET /licitaciones  │
     │                    ├──────────────────────>│
     │                    │                       │
     │                    │ 3. HTML response      │
     │                    │<──────────────────────┤
     │                    │                       │
     │ 4. Parse HTML      │                       │
     │    con BS4         │                       │
     ├────┐               │                       │
     │    │               │                       │
     │<───┘               │                       │
     │                    │                       │
     │ 5. Guardar en      │                       │
     │    licitaciones.json                       │
     ├────┐               │                       │
     │    │               │                       │
     │<───┘               │                       │
     │                    │                       │
     │ 6. Log resultados  │                       │
     │                    │                       │
```

**Configuración de cron** (Railway/Render):
```bash
# Ejecutar scraper diariamente a las 6 AM (UTC)
0 6 * * * cd /app && python -m services.scraper
```

---

## Integraciones Externas

### 1. Anthropic Claude API

**Endpoint**: `https://api.anthropic.com/v1/messages`

**Autenticación**: Header `x-api-key: sk-ant-...`

**Request típico**:
```json
{
  "model": "claude-sonnet-4-20250514",
  "max_tokens": 1024,
  "system": "Sos Codi, asistente de licitaciones...",
  "messages": [
    {"role": "user", "content": "¿Cuáles son las licitaciones?"}
  ]
}
```

**Response**:
```json
{
  "id": "msg_01ABC...",
  "type": "message",
  "role": "assistant",
  "content": [
    {
      "type": "text",
      "text": "Actualmente hay 3 licitaciones activas:\n\n1. ..."
    }
  ],
  "usage": {
    "input_tokens": 250,
    "output_tokens": 180
  }
}
```

**Costos** (2025):
- Input: $3/millón tokens
- Output: $15/millón tokens
- Estimado por conversación: $0.01 - $0.03

**Rate limits**:
- 50 requests/min (tier 1)
- 5 requests/sec

### 2. Twilio WhatsApp API

**Endpoint**: `https://api.twilio.com/2010-04-01/Accounts/{AccountSid}/Messages.json`

**Autenticación**: Basic Auth (AccountSid + AuthToken)

**Request**:
```json
{
  "From": "whatsapp:+14155238886",
  "To": "whatsapp:+5492974123456",
  "Body": "Nueva licitación: Servicio de limpieza N° 45/2025"
}
```

**Costos**:
- WhatsApp Sandbox: Gratis (solo desarrollo)
- WhatsApp Business: $0.005/mensaje (producción)

---

## Seguridad

### Autenticación

| Endpoint | Método de Auth | Implementado |
|----------|----------------|--------------|
| `GET /licitaciones` | Público | ✅ |
| `POST /licitaciones` | Header `password` | ✅ |
| `POST /notificaciones` | Header `password` | ✅ |
| `POST /chat/message` | Público | ✅ |

**Nota**: No hay usuarios registrados. El `ADMIN_PASSWORD` es compartido (mejorar en v2 con JWT).

### CORS

```python
# Configuración en main.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://comodoro-asistente.vercel.app",
        "http://localhost:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Secrets Management

**Desarrollo**: `.env` (no commitear)

**Producción**: Variables de entorno en Railway/Render

| Secret | Rotación | Almacenamiento |
|--------|----------|----------------|
| `ANTHROPIC_API_KEY` | Manual | Anthropic Console |
| `TWILIO_AUTH_TOKEN` | Manual | Twilio Console |
| `ADMIN_PASSWORD` | Nunca | Hardcoded en .env |

**Recomendación**: Migrar a secretos gestionados (Vault, AWS Secrets Manager) en producción.

### Validación de Input

- **Pydantic models**: Validación automática de tipos en FastAPI
- **Max length**: Mensajes limitados a 2000 caracteres (prevenir abuse)
- **Sanitización**: BeautifulSoup4 escapa HTML automáticamente

---

## Escalabilidad

### Limitaciones Actuales

| Componente | Límite | Bottleneck |
|------------|--------|------------|
| Frontend | Ilimitado (CDN) | - |
| Backend | ~100 req/s | Filesystem I/O |
| Claude API | 50 req/min | Rate limit |
| Datos | 6.840 proveedores | RAM (500 KB) |

### Estrategia de Escalamiento

#### Fase 1 (Actual): Monolito Stateless
- 1 instancia de Railway/Render
- Escalamiento vertical (más RAM/CPU)

#### Fase 2: Horizontal Scaling
- Múltiples instancias detrás de load balancer
- **Problema**: JSON cache compartido
- **Solución**: Redis para caché distribuido

#### Fase 3: Microservicios
- Separar scraper en servicio independiente
- Worker queue para notificaciones (Celery + Redis)
- PostgreSQL para licitaciones

---

## Decisiones Arquitectónicas

### ¿Por qué FastAPI?

| Alternativa | Ventaja | Desventaja |
|-------------|---------|------------|
| **FastAPI** ✅ | Type safety, docs automáticas, performance | - |
| Flask | Simplicidad | Sin validación automática |
| Django | Baterías incluidas | Overhead para API simple |
| Node.js | JavaScript full-stack | Python mejor para ML/scraping |

### ¿Por qué CSV en lugar de Base de Datos?

- 6.840 registros = 500 KB RAM
- No hay escritura frecuente (padrón actualiza 1 vez/año)
- Búsqueda con pandas: < 10 ms
- **Trade-off**: Simplicidad vs. escalabilidad

**Migrar a PostgreSQL cuando**:
- Padrón > 50.000 proveedores
- Múltiples usuarios admin concurrentes
- Necesidad de auditoria (logs de cambios)

### ¿Por qué JSON File en lugar de Base de Datos?

**Pros**:
- Cero configuración
- Deploy simple (no hay que provisionar DB)
- Git-trackable (ver cambios en diff)

**Contras**:
- Race conditions en escritura concurrente
- No hay queries complejas (ej: JOIN)
- Backup manual

**Plan de migración**: PostgreSQL en fase 2 (issue #015)

---

## Monitoreo y Logging

### Logging

```python
# main.py
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
```

**Logs importantes**:
- Cada request a Claude API (tokens usados)
- Errores de scraping (para debug manual)
- Notificaciones WhatsApp enviadas

### Métricas (Futuro)

- **Issue #008**: Integración con Sentry (error tracking)
- **Issue #009**: Dashboard de métricas (requests/día, tokens consumidos)

---

## Referencias

- [FastAPI Best Practices](https://fastapi.tiangolo.com/tutorial/)
- [Anthropic Claude API Docs](https://docs.anthropic.com)
- [Twilio WhatsApp API](https://www.twilio.com/docs/whatsapp/api)
- [Architectural Decision Records (ADRs)](https://adr.github.io/)

---

**Última actualización**: 2026-03-03
**Versión**: 1.0.0
