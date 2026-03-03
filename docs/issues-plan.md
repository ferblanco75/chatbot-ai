# Plan de Issues y Roadmap - Codi

Este documento define el roadmap completo del proyecto, desde el MVP hasta la versión de producción.

---

## Tabla de Contenidos

- [Visión del Producto](#visión-del-producto)
- [Fases del Proyecto](#fases-del-proyecto)
- [Issues Completados](#issues-completados)
- [Issues en Progreso](#issues-en-progreso)
- [Backlog Priorizado](#backlog-priorizado)
- [Futuro (Post v1.0)](#futuro-post-v10)

---

## Visión del Producto

**Objetivo**: Facilitar el acceso a información sobre licitaciones municipales mediante un asistente conversacional inteligente.

**Usuarios**:
1. **Proveedores**: Buscan licitaciones para participar
2. **Ciudadanos**: Consultan sobre procesos de compra pública
3. **Funcionarios municipales**: Administran licitaciones y notificaciones

**Métricas de éxito**:
- Reducir en 50% el tiempo promedio de consulta sobre licitaciones
- 80% de las consultas resueltas sin intervención humana
- 100+ conversaciones mensuales en los primeros 3 meses

---

## Fases del Proyecto

```
┌──────────────────────────────────────────────────────────────┐
│  FASE 1: MVP (Minimum Viable Product)                        │
│  Timeline: 4 semanas                                         │
│  Issues: #001 - #005                                         │
└──────────────────────────────────────────────────────────────┘
                             │
                             ▼
┌──────────────────────────────────────────────────────────────┐
│  FASE 2: Deploy y Testing                                    │
│  Timeline: 2 semanas                                         │
│  Issues: #006 - #008                                         │
└──────────────────────────────────────────────────────────────┘
                             │
                             ▼
┌──────────────────────────────────────────────────────────────┐
│  FASE 3: Features de Administración y Automatización         │
│  Timeline: 4.5 semanas                                       │
│  Issues: #009 - #011                                         │
└──────────────────────────────────────────────────────────────┘
                             │
                             ▼
┌──────────────────────────────────────────────────────────────┐
│  FASE 4: UX y Optimización                                   │
│  Timeline: 4 semanas                                         │
│  Issues: #012 - #014                                         │
└──────────────────────────────────────────────────────────────┘
                             │
                             ▼
┌──────────────────────────────────────────────────────────────┐
│  FASE 5: Features Avanzadas (Post v1.0)                      │
│  Timeline: Por determinar                                    │
│  Issues: #015 - #018                                         │
└──────────────────────────────────────────────────────────────┘
```

---

## Issues Completados

### ✅ Issue #001: Widget flotante HTML/CSS

**Descripción**: Crear el widget embebible del chatbot con diseño responsive.

**Componentes**:
- FAB (Floating Action Button) con avatar de Codi
- Panel de chat colapsable
- Burbujas de conversación (usuario y bot)
- Burbuja de bienvenida con animación
- Chips de respuesta rápida
- Typing indicator

**Archivos creados**:
- `index.html` (HTML + CSS + JS embebido)
- `assets/codi-avatar.svg` (placeholder)

**Criterios de aceptación**:
- [x] Widget aparece en esquina inferior derecha
- [x] Responsive en mobile, tablet y desktop
- [x] Animaciones suaves (open/close panel)
- [x] Estilos según paleta de colores municipal

**Fecha de completado**: 2025-02-15

---

### ✅ Issue #002: Integración con Claude API

**Descripción**: Conectar el backend con Anthropic Claude para procesamiento de lenguaje natural.

**Tareas**:
- [x] Crear endpoint `POST /chat/message`
- [x] Configurar Anthropic Python SDK
- [x] Diseñar system prompt con contexto municipal
- [x] Manejar historial de conversación
- [x] Implementar retry logic para errores de API

**System Prompt Base**:
```
Sos Codi, asistente virtual de la Municipalidad de Comodoro Rivadavia.
Tu función es ayudar con consultas sobre licitaciones públicas.

Contexto:
- Licitaciones activas: [DATA]
- Proveedores registrados: [DATA]
- Normativa: Ley II N°76, Ley N°4829

Tono: Amigable, profesional, voseo rioplatense.
```

**Archivos modificados**:
- `backend/routers/chat.py` (creado)
- `backend/requirements.txt` (agregado `anthropic`)

**Fecha de completado**: 2025-02-22

---

### ✅ Issue #003: Scraper de licitaciones

**Descripción**: Automatizar la extracción de licitaciones desde el sitio oficial.

**Tareas**:
- [x] Scraper con httpx + BeautifulSoup4
- [x] Parser de tabla HTML de licitaciones
- [x] Guardar en `data/licitaciones.json`
- [x] Retry con backoff exponencial (3 intentos)
- [x] Logging de errores

**Target URL**: https://www.comodoro.gov.ar/secciones/licitaciones/

**Archivos creados**:
- `backend/services/scraper.py`
- `backend/data/licitaciones.json` (cache)

**Ejecución**:
```bash
# Manual
python -m backend.services.scraper

# Automatizado (futuro)
# Cron job 1 vez por día
```

**Fecha de completado**: 2025-03-01

---

### ✅ Issue #004: Diseño en Figma (avatar + componentes)

**Descripción**: Diseño profesional de la identidad visual de Codi.

**Entregables**:
- [x] Avatar de Codi en SVG optimizado
- [x] Componentes del widget (FAB, burbujas, chips)
- [x] Estados del chat (idle, typing, error)
- [x] Versión mobile
- [x] Guía de tono de voz

**Archivos creados**:
- `docs/codi-design-brief.md` (brief para diseñadores)
- `docs/guia-diseño-figma.md` (guía de implementación)

**Colores definidos**:
- Azul Marino: `#0B2347`
- Azul: `#1055A8`
- Dorado: `#E8A000`

**Fecha de completado**: 2025-03-02

---

## Issues en Progreso

### 🚧 Issue #005: README completo + documentación de desarrollo

**Descripción**: Documentación completa para desarrolladores y usuarios del proyecto.

**Tareas**:
- [x] README.md principal con badges
- [x] docs/architecture.md (arquitectura técnica)
- [x] docs/development.md (guía de desarrollo)
- [x] docs/issues-plan.md (este archivo)
- [ ] Agregar screenshots al README
- [ ] Crear archivo LICENSE (MIT)
- [ ] Revisar y corregir typos

**Archivos**:
- `README.md`
- `docs/architecture.md`
- `docs/development.md`
- `docs/issues-plan.md`

**Estado**: 85% completado

**Fecha estimada de completado**: 2026-03-05

---

## Backlog Priorizado

### 🔴 Issue #006: Deploy en Railway + Vercel

**Prioridad**: ALTA
**Estimación**: 1 semana
**Dependencias**: #005

**Descripción**: Deploy del MVP en producción.

**Tareas**:
- [ ] Configurar proyecto en Railway (backend)
- [ ] Configurar variables de entorno en Railway
- [ ] Conectar repositorio a Vercel (frontend)
- [ ] Configurar dominio personalizado (opcional)
- [ ] Configurar CI/CD con GitHub Actions
- [ ] Smoke tests post-deploy

**Criterios de aceptación**:
- [ ] Backend accesible en `https://chatbot-backend.railway.app`
- [ ] Frontend accesible en `https://comodoro-asistente.vercel.app`
- [ ] Deploy automático con cada push a `master`
- [ ] Health check endpoint (`/health`) responde OK

**Documentación**:
- Agregar sección "Deployment" al README.md
- Crear archivo `.github/workflows/deploy.yml` (GitHub Actions)

---

### 🔴 Issue #007: Tests automatizados (pytest)

**Prioridad**: ALTA
**Estimación**: 1.5 semanas
**Dependencias**: #006

**Descripción**: Suite de tests para garantizar calidad del código.

**Tareas**:
- [ ] Setup de pytest + pytest-asyncio
- [ ] Tests unitarios de routers:
  - [ ] `test_chat.py` (POST /chat/message)
  - [ ] `test_licitaciones.py` (CRUD)
  - [ ] `test_proveedores.py` (búsqueda)
  - [ ] `test_notificaciones.py` (WhatsApp)
- [ ] Tests de servicios:
  - [ ] `test_scraper.py` (parsing HTML)
  - [ ] `test_whatsapp.py` (mock de Twilio)
- [ ] Mocks de APIs externas (Anthropic, Twilio)
- [ ] Coverage report (objetivo: >80%)

**Archivos a crear**:
- `backend/tests/test_*.py`
- `backend/tests/conftest.py` (fixtures)
- `.github/workflows/test.yml` (CI)

**Comando**:
```bash
pytest backend/tests/ --cov=backend --cov-report=html
```

**Criterios de aceptación**:
- [ ] Coverage > 80%
- [ ] Tests corren en GitHub Actions en cada PR
- [ ] PRs bloqueados si tests fallan

---

### 🟡 Issue #008: Métricas y analytics

**Prioridad**: MEDIA
**Estimación**: 1 semana
**Dependencias**: #007

**Descripción**: Implementar tracking de métricas para monitorear uso y performance.

**Métricas a trackear**:
- Número de conversaciones (total, diarias, semanales)
- Mensajes por conversación (promedio)
- Tokens consumidos de Claude API
- Tiempo de respuesta promedio
- Errores (4xx, 5xx)
- Temas más consultados (licitaciones, proveedores, normativa)

**Herramientas**:
- **Sentry**: Error tracking y performance monitoring
- **Google Analytics** (opcional): Interacciones del widget
- **Custom logging**: Logs estructurados en JSON

**Tareas**:
- [ ] Integrar Sentry SDK
- [ ] Crear dashboard de métricas (Sentry Dashboard)
- [ ] Logging estructurado en JSON
- [ ] Endpoint `/metrics` para Prometheus (futuro)

**Ejemplo de log estructurado**:
```json
{
  "timestamp": "2025-03-15T10:30:00Z",
  "event": "chat_message",
  "user_id": "anon_abc123",
  "message_length": 45,
  "tokens_input": 250,
  "tokens_output": 180,
  "response_time_ms": 2340
}
```

---

### 🟡 Issue #009: Panel admin completo

**Prioridad**: MEDIA
**Estimación**: 2 semanas
**Dependencias**: #006

**Descripción**: Mejorar el panel de administración (`admin.html`) para gestión completa.

**Features**:
- [ ] Autenticación con usuario/password (no solo password global)
- [ ] CRUD completo de licitaciones:
  - [ ] Crear
  - [ ] Editar
  - [ ] Eliminar
  - [ ] Ver historial de cambios
- [ ] Trigger manual del scraper (botón "Actualizar licitaciones")
- [ ] Gestión de proveedores:
  - [ ] Ver listado completo
  - [ ] Búsqueda y filtros
  - [ ] Agregar proveedor manualmente
- [ ] Envío de notificaciones WhatsApp:
  - [ ] Seleccionar destinatarios (individual o por rubro)
  - [ ] Plantillas de mensajes
  - [ ] Historial de notificaciones enviadas
- [ ] Dashboard con estadísticas:
  - [ ] Licitaciones activas/cerradas
  - [ ] Consultas del chatbot (últimas 24h)
  - [ ] Tokens consumidos (Claude API)

**Archivos a modificar**:
- `admin.html` (UI completo)
- `backend/routers/admin.py` (nuevo router)
- `backend/routers/licitaciones.py` (agregar PUT, DELETE)

**Diseño**:
- Framework CSS: **Bootstrap 5** (o Tailwind CSS)
- Componentes: Tablas, modales, formularios

---

### 🟡 Issue #010: Mejoras y automatización del scraper

**Prioridad**: MEDIA
**Estimación**: 1 semana
**Dependencias**: #006

**Descripción**: Mejorar el scraper de licitaciones con automatización y extracción de datos más completa.

**Tareas**:
- [ ] Configurar cron job para scraping automático diario
  - [ ] Configurar schedule en Railway/Render (ej: 6:00 AM diario)
  - [ ] Implementar endpoint `/scraper/run` para trigger manual
  - [ ] Logging de ejecuciones (timestamp, licitaciones nuevas, errores)
- [ ] Mejorar el scraper para extraer más detalles
  - [ ] Entrar a cada URL individual de licitación
  - [ ] Extraer descripción completa (no solo título)
  - [ ] Extraer adjuntos/pliegos disponibles
  - [ ] Extraer contacto responsable
  - [ ] Extraer presupuesto estimado
- [ ] Agregar filtros por rubro/categoría
  - [ ] Detectar rubro automáticamente desde título/descripción
  - [ ] Categorizar licitaciones (construcción, servicios, tecnología, etc.)
  - [ ] Agregar campo `categoria` y `rubro` al JSON de licitaciones
  - [ ] Endpoint GET `/licitaciones?rubro=limpieza&categoria=servicios`

**Archivos a modificar**:
- `backend/services/scraper.py` (mejoras de parsing)
- `backend/routers/licitaciones.py` (agregar filtros)
- `backend/data/licitaciones.json` (nuevos campos)

**Configuración de cron** (Railway/Render):
```bash
# Ejecutar scraper diariamente a las 6 AM (UTC)
0 6 * * * curl -X POST https://chatbot-backend.railway.app/scraper/run
```

**Criterios de aceptación**:
- [ ] Scraper corre automáticamente 1 vez por día
- [ ] Extrae al menos 5 campos adicionales por licitación
- [ ] Endpoint `/licitaciones` soporta filtros por rubro/categoría
- [ ] Logs de scraper visibles en Railway/Render dashboard

---

### 🟡 Issue #011: Notificaciones WhatsApp automáticas

**Prioridad**: MEDIA
**Estimación**: 1.5 semanas
**Dependencias**: #010

**Descripción**: Sistema de suscripciones para recibir alertas de nuevas licitaciones.

**Flow**:
1. Usuario envía mensaje al número WhatsApp de Codi
2. Bot responde: "¡Hola! ¿Querés recibir notificaciones de licitaciones? Respondé SÍ"
3. Usuario responde "SÍ"
4. Bot pregunta: "¿De qué rubros? (ej: limpieza, construcción, tecnología)"
5. Usuario especifica rubros
6. Sistema guarda suscripción en base de datos
7. Cuando hay nueva licitación que coincide, envía WhatsApp

**Tareas**:
- [ ] Webhook de Twilio para recibir mensajes entrantes
- [ ] Endpoint `POST /webhooks/whatsapp` (recibir mensajes)
- [ ] Base de datos para suscripciones (PostgreSQL o SQLite)
- [ ] Tabla `suscripciones` con columnas:
  - `id`, `telefono`, `rubros[]`, `activa`, `created_at`
- [ ] Lógica de matching (nueva licitación → rubros → enviar notif)
- [ ] Cron job para chequear nuevas licitaciones y notificar

**Archivos**:
- `backend/routers/webhooks.py` (nuevo)
- `backend/models.py` (modelos de DB)
- `backend/database.py` (conexión a PostgreSQL)

**Consideraciones**:
- Migrar de JSON files a PostgreSQL (issue #016)
- Twilio WhatsApp Business API (requiere aprobación de Meta)

---

### 🟢 Issue #012: Mejoras de UX en el widget

**Prioridad**: BAJA
**Estimación**: 1 semana
**Dependencias**: #008

**Descripción**: Refinamientos de la experiencia de usuario.

**Features**:
- [ ] Animación del avatar mientras el bot "piensa"
- [ ] Sonido de notificación (opcional, con toggle)
- [ ] Botón "Copiar respuesta" en burbujas del bot
- [ ] Botón "Enviar por email" (mailto: con contenido de la conversación)
- [ ] Modo oscuro (dark mode)
- [ ] Persistencia de preferencias (LocalStorage)
- [ ] Widget minimizable a solo avatar (sin panel)
- [ ] Historial de conversaciones (pestañas "Nueva" / "Historial")

**Archivos**:
- `index.html` (CSS y JS)

**A/B Testing** (opcional):
- Variante A: Burbuja de bienvenida a los 3s
- Variante B: Burbuja aparece solo al hacer hover en FAB

---

### 🟢 Issue #013: Soporte multiidioma

**Prioridad**: BAJA
**Estimación**: 2 semanas
**Dependencias**: #012

**Descripción**: Widget en español e inglés.

**Idiomas**:
- Español (default, voseo rioplatense)
- Inglés (para proveedores extranjeros)

**Implementación**:
- Dropdown en el header del chat para cambiar idioma
- System prompt de Claude con instrucción de idioma
- Strings del UI en archivo JSON de i18n

**Archivos**:
- `assets/i18n/es.json`
- `assets/i18n/en.json`
- `index.html` (lógica de i18n)

**Ejemplo**:
```json
// es.json
{
  "welcome": "¡Hola! Soy Codi. ¿En qué puedo ayudarte?",
  "placeholder": "Escribí tu consulta..."
}

// en.json
{
  "welcome": "Hello! I'm Codi. How can I help you?",
  "placeholder": "Type your question..."
}
```

---

### 🟢 Issue #014: Caché de respuestas frecuentes

**Prioridad**: BAJA
**Estimación**: 1 semana
**Dependencias**: #008

**Descripción**: Cachear respuestas a preguntas frecuentes para reducir costos de Claude API.

**Implementación**:
- Redis (o in-memory dict) para caché de respuestas
- Key: hash del mensaje (normalizado)
- TTL: 1 hora

**Flow**:
```
1. Usuario pregunta: "¿Cuáles son las licitaciones activas?"
2. Backend hashea mensaje → busca en caché
3. Si existe caché → retorna inmediatamente
4. Si no existe → llama Claude API → guarda en caché
```

**Tareas**:
- [ ] Integrar Redis (o usar dict in-memory como MVP)
- [ ] Normalizar mensajes (lowercase, quitar acentos, etc.)
- [ ] Configurar TTL de caché
- [ ] Endpoint `/cache/clear` (admin)

**Ahorro estimado**: 30-50% de requests a Claude API

---

### 🔵 Issue #015: Integración con Google Calendar

**Prioridad**: NICE-TO-HAVE
**Estimación**: 2 semanas
**Dependencias**: #011

**Descripción**: Permitir a proveedores agregar fechas de apertura de licitaciones a Google Calendar.

**Flow**:
1. Bot muestra licitación con fecha de apertura
2. Chip: "Agregar a mi calendario"
3. Usuario clickea → genera `.ics` o link de Google Calendar
4. Usuario confirma y se agrega el evento

**Tareas**:
- [ ] Generar archivo `.ics` (estándar iCalendar)
- [ ] Link de Google Calendar con parámetros pre-filled
- [ ] Botón "Agregar a calendario" en burbujas del bot

**Ejemplo de link**:
```
https://calendar.google.com/calendar/render?action=TEMPLATE
&text=Licitación+N°+45/2025
&dates=20250415T100000Z/20250415T110000Z
&details=Servicio+de+limpieza
&location=Namuncurá+26,+Comodoro+Rivadavia
```

---

### 🔵 Issue #016: Migración a PostgreSQL

**Prioridad**: NICE-TO-HAVE
**Estimación**: 2 semanas
**Dependencias**: #011

**Descripción**: Reemplazar archivos JSON/CSV por base de datos relacional.

**Motivación**:
- Soportar múltiples usuarios admin concurrentes
- Queries complejas (JOINs, índices)
- Auditoria (logs de cambios)
- Escalabilidad

**Tablas**:
```sql
CREATE TABLE licitaciones (
  id SERIAL PRIMARY KEY,
  numero VARCHAR(50) UNIQUE NOT NULL,
  titulo TEXT NOT NULL,
  organismo VARCHAR(255),
  fecha_publicacion DATE,
  fecha_apertura DATE,
  monto_estimado NUMERIC(15,2),
  estado VARCHAR(20) CHECK (estado IN ('activa', 'cerrada', 'suspendida')),
  url_pliego TEXT,
  descripcion TEXT,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE proveedores (
  id SERIAL PRIMARY KEY,
  cuit VARCHAR(13) UNIQUE NOT NULL,
  razon_social VARCHAR(255) NOT NULL,
  rubro VARCHAR(100),
  localidad VARCHAR(100),
  created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE suscripciones (
  id SERIAL PRIMARY KEY,
  telefono VARCHAR(20) NOT NULL,
  rubros TEXT[],
  activa BOOLEAN DEFAULT TRUE,
  created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE conversaciones (
  id SERIAL PRIMARY KEY,
  session_id UUID NOT NULL,
  messages JSONB,
  created_at TIMESTAMP DEFAULT NOW()
);
```

**Tareas**:
- [ ] Setup de PostgreSQL (Railway o Render)
- [ ] Crear schema con Alembic (migrations)
- [ ] Migrar datos de JSON/CSV a PostgreSQL
- [ ] Adaptar routers para usar SQLAlchemy ORM
- [ ] Actualizar tests

**Archivos**:
- `backend/database.py` (conexión PostgreSQL)
- `backend/models.py` (SQLAlchemy models)
- `backend/migrations/` (Alembic)

---

### 🔵 Issue #017: Dashboard público de licitaciones

**Prioridad**: NICE-TO-HAVE
**Estimación**: 3 semanas
**Dependencias**: #016

**Descripción**: Sitio web público (fuera del chatbot) con tabla de licitaciones.

**Features**:
- Tabla de licitaciones con filtros (estado, fecha, organismo)
- Búsqueda por palabra clave
- Vista detalle de cada licitación
- Export a Excel/PDF
- RSS feed de nuevas licitaciones

**Stack**:
- **Frontend**: Next.js (React) o SvelteKit
- **Backend**: Reutilizar API de FastAPI
- **Hosting**: Vercel

**URL**: https://licitaciones.comodoro.gov.ar (o subdominio)

**Archivos**:
- Nuevo repo: `chatbot-ai-dashboard`

---

### 🔵 Issue #018: Análisis de sentimiento y temas

**Prioridad**: NICE-TO-HAVE
**Estimación**: 2 semanas
**Dependencias**: #008, #016

**Descripción**: Análisis automático de las consultas para mejorar el servicio.

**Análisis**:
1. **Temas más consultados**:
   - Clustering de mensajes (ej: "licitaciones", "proveedores", "requisitos")
2. **Sentimiento**:
   - Positivo/negativo/neutro
   - Detectar frustración (ej: "no entiendo", "no funciona")
3. **Preguntas sin respuesta**:
   - Detectar cuando Claude dice "no tengo información sobre eso"
   - Dashboard de "gaps de conocimiento"

**Herramientas**:
- Claude API (ya tenemos acceso)
- PostgreSQL (guardar análisis)

**Tareas**:
- [ ] Endpoint `/analytics/topics` (temas más consultados)
- [ ] Endpoint `/analytics/sentiment` (distribución de sentimiento)
- [ ] Dashboard en `admin.html` con gráficos (Chart.js)

**Output esperado**:
```json
{
  "temas": [
    {"tema": "licitaciones_activas", "count": 450},
    {"tema": "requisitos_participacion", "count": 320},
    {"tema": "proveedores", "count": 180}
  ],
  "sentimiento": {
    "positivo": 65,
    "neutral": 30,
    "negativo": 5
  }
}
```

---

## Futuro (Post v1.0)

**Ideas para versiones futuras**:

1. **Issue #019**: Integración con sistema de compras municipal (ERP)
2. **Issue #020**: Chatbot por voz (Speech-to-Text + Text-to-Speech)
3. **Issue #021**: Widget embebible para otros municipios (white-label)
4. **Issue #022**: Asistente para armado de ofertas (ayuda a proveedores a completar formularios)
5. **Issue #023**: Blockchain para trazabilidad de licitaciones
6. **Issue #024**: Gamificación (badges para proveedores activos)
7. **Issue #025**: Extensión de Chrome (widget en cualquier sitio)

---

## Priorización de Issues

### Criterios de Priorización

| Criterio | Peso | Descripción |
|----------|------|-------------|
| Impacto en usuarios | 40% | ¿Cuántos usuarios se benefician? |
| Complejidad técnica | 30% | ¿Qué tan difícil es implementar? |
| Dependencias | 20% | ¿Bloquea otros issues? |
| Urgencia | 10% | ¿Es crítico para el MVP? |

### Matriz de Priorización

```
     │ Alto Impacto │ Bajo Impacto
─────┼──────────────┼──────────────
Alta │   #006 🔴   │   #013 🟢
Comp │   #007 🔴   │   #015 🔵
lejid│   #010 🟡   │   #018 🔵
ad   │   #011 🟡   │
─────┼──────────────┼──────────────
Baja │   #008 🟡   │   #012 🟢
Comp │   #009 🟡   │   #014 🟢
lejid│   #016 🔵   │   #017 🔵
ad   │              │
```

**Leyenda**:
- 🔴 ALTA: Hacer ahora
- 🟡 MEDIA: Hacer después del MVP
- 🟢 BAJA: Nice-to-have
- 🔵 FUTURO: Post v1.0

---

## Estimaciones de Esfuerzo

| Issue | Estimación | Días-persona | Sprint |
|-------|------------|--------------|--------|
| #006 | 1 semana | 5 días | Sprint 1 |
| #007 | 1.5 semanas | 7 días | Sprint 2 |
| #008 | 1 semana | 5 días | Sprint 3 |
| #009 | 2 semanas | 10 días | Sprint 4-5 |
| #010 | 1 semana | 5 días | Sprint 6 |
| #011 | 1.5 semanas | 7 días | Sprint 7 |
| #012 | 1 semana | 5 días | Sprint 8 |
| #013 | 2 semanas | 10 días | Sprint 9-10 |
| #014 | 1 semana | 5 días | Sprint 11 |
| #015 | 2 semanas | 10 días | Backlog |
| #016 | 2 semanas | 10 días | Backlog |
| #017 | 3 semanas | 15 días | Backlog |
| #018 | 2 semanas | 10 días | Backlog |

**Total para v1.0 (issues #006-#014)**: ~14 semanas (~3.5 meses)

---

## Changelog

| Versión | Fecha | Cambios |
|---------|-------|---------|
| 0.1.0 | 2025-02-15 | MVP inicial (#001-#004) |
| 0.2.0 | 2025-03-03 | Documentación completa (#005) |
| 1.0.0 | 2025-06-15 (est.) | Deploy + tests + admin (#006-#009) |
| 1.1.0 | 2025-08-01 (est.) | Scraper automático + notificaciones (#010-#011) |
| 2.0.0 | 2025-10-15 (est.) | PostgreSQL + dashboard público (#016-#017) |

---

**Última actualización**: 2026-03-03
**Versión del documento**: 1.1.0
**Responsable**: Fernando Blanco (@ferblanco75)
