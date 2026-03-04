# Plan de Issues y Roadmap - AsisteCR+

Este documento define el roadmap completo del proyecto, desde el MVP hasta la versión de producción.

---

## Tabla de Contenidos

- [Visión del Producto](#visión-del-producto)
- [Fases del Proyecto](#fases-del-proyecto)
- [Issues Completados](#issues-completados)
- [Issues en Progreso](#issues-en-progreso)
- [Portal del Proveedor (Sprint 4-5)](#portal-del-proveedor-sprint-4-5)
- [Backlog Priorizado](#backlog-priorizado)
- [Futuro (Post v1.0)](#futuro-post-v10)

---

## Visión del Producto

**Objetivo**: Facilitar el acceso a información sobre licitaciones municipales mediante un asistente conversacional inteligente y un portal completo para proveedores.

**Usuarios**:
1. **Proveedores**: Buscan licitaciones para participar, gestionan su legajo y reciben alertas
2. **Ciudadanos**: Consultan sobre procesos de compra pública
3. **Funcionarios municipales**: Administran licitaciones y notificaciones

**Métricas de éxito**:
- Reducir en 50% el tiempo promedio de consulta sobre licitaciones
- 80% de las consultas resueltas sin intervención humana
- 100+ conversaciones mensuales en los primeros 3 meses
- 50+ proveedores activos usando el portal en el primer trimestre

---

## Fases del Proyecto

```
┌──────────────────────────────────────────────────────────────┐
│  FASE 1: Chatbot MVP (Sprints 1-3)                           │
│  Timeline: 4 semanas                                         │
│  Issues: #001 - #005                                         │
│  Estado: ✅ COMPLETADO                                       │
└──────────────────────────────────────────────────────────────┘
                             │
                             ▼
┌──────────────────────────────────────────────────────────────┐
│  FASE 2: Portal del Proveedor (Sprints 4-5)                  │
│  Timeline: 2 semanas                                         │
│  Issues: #016 - #029                                         │
│  Estado: 🆕 EN DESARROLLO                                    │
└──────────────────────────────────────────────────────────────┘
                             │
                             ▼
┌──────────────────────────────────────────────────────────────┐
│  FASE 3: Deploy, Testing y Producción                        │
│  Timeline: 3 semanas                                         │
│  Issues: #030 - #032                                         │
└──────────────────────────────────────────────────────────────┘
                             │
                             ▼
┌──────────────────────────────────────────────────────────────┐
│  FASE 4: Features Avanzadas                                  │
│  Timeline: 6 semanas                                         │
│  Issues: #033 - #038                                         │
└──────────────────────────────────────────────────────────────┘
                             │
                             ▼
┌──────────────────────────────────────────────────────────────┐
│  FASE 5: Escalabilidad y Post v1.0                           │
│  Timeline: Por determinar                                    │
│  Issues: #039 - #042                                         │
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

## Portal del Proveedor (Sprint 4-5)

Esta sección contiene los 14 issues del nuevo Portal del Proveedor basados en el UX proposal navegable (`docs/ux-proposal.html`).

**Estimación total**: 33 horas · 2 semanas

---

### 🎨 Issue #016: Sistema de navegación y sidebar del portal del proveedor

**Prioridad**: CRÍTICA
**Estimación**: 3 horas
**Labels**: `design`, `ux`
**Dependencias**: Ninguna

**Descripción**: Definir con la diseñadora: paleta final (navy/blue/sky/gold), tipografía Syne + DM Sans, sidebar navegación, sidebar brand, user avatar, nav items con estado active/hover/badge.

**Entregables**:
- Componentes Figma con especificaciones de espaciado
- Tokens de color documentados
- Sistema de navegación completo
- Estados: active, hover, badge notifications

**Tareas**:
- [ ] Definir paleta final de colores
- [ ] Especificar tipografía (Syne para títulos, DM Sans para cuerpo)
- [ ] Diseñar sidebar con brand y user info
- [ ] Diseñar nav items y sus estados
- [ ] Documentar spacing y tokens

**Criterios de aceptación**:
- [ ] Figma file con todos los componentes
- [ ] Documentación de design tokens
- [ ] Guía de uso para developers

**Bloquea**: #017, #027, #029

**Semana**: 4

---

### 🔧 Issue #017: Layout base del portal: sidebar + main area + responsive

**Prioridad**: CRÍTICA
**Estimación**: 2 horas
**Labels**: `frontend`
**Dependencias**: #016

**Descripción**: Crear `portal.html` con estructura CSS Grid (260px sidebar + 1fr main). Sidebar fijo sticky. Main con overflow-y. Header de página reutilizable. Responsive: en mobile la sidebar se convierte en bottom nav.

**Archivos a crear**:
- `portal.html`
- `styles/portal.css`

**Tareas**:
- [ ] Estructura HTML base con CSS Grid
- [ ] Sidebar sticky 260px
- [ ] Main area con overflow-y
- [ ] Header de página reutilizable
- [ ] Media queries para responsive (mobile: bottom nav)

**Criterios de aceptación**:
- [ ] Layout funciona en los 6 screens del portal
- [ ] Sidebar sticky correctamente posicionada
- [ ] Responsive en mobile, tablet, desktop
- [ ] Navegación entre secciones sin reload (SPA)

**Semana**: 4

---

### 🔐 Issue #018: Endpoint de autenticación por CUIT + código OTP (WhatsApp)

**Prioridad**: CRÍTICA
**Estimación**: 3 horas
**Labels**: `backend`
**Dependencias**: Setup básico de Twilio WhatsApp

**Descripción**: Implementar autenticación passwordless con OTP enviado por WhatsApp.

**Endpoints a crear**:
1. `POST /auth/request-code {cuit}`
   - Busca proveedor en CSV
   - Genera código 6 chars alfanumérico
   - Envía por WhatsApp vía Twilio
   - Guarda en memoria con TTL 30 min

2. `POST /auth/verify {cuit, code}`
   - Valida código OTP
   - Retorna JWT firmado (cuit, nombre, rubros)
   - Expira en 8 horas

**Archivos a crear/modificar**:
- `backend/routers/auth.py`
- `backend/services/auth_service.py`
- `backend/services/whatsapp.py` (básico para OTP)

**Dependencias externas**:
- Twilio WhatsApp API (setup básico)
- PyJWT para generación de tokens

**Tareas**:
- [ ] Setup básico de Twilio para enviar mensajes
- [ ] Endpoint POST /auth/request-code
- [ ] Generación de códigos OTP aleatorios
- [ ] Almacenamiento en memoria (dict) con TTL
- [ ] Endpoint POST /auth/verify
- [ ] Generación y firma de JWT
- [ ] Manejo de errores (CUIT no encontrado, código inválido, expirado)

**Criterios de aceptación**:
- [ ] OTP se envía correctamente por WhatsApp
- [ ] Códigos expiran después de 30 minutos
- [ ] JWT válido por 8 horas
- [ ] Manejo de errores apropiado
- [ ] Logging de intentos de autenticación

**Variables de entorno necesarias**:
```bash
TWILIO_ACCOUNT_SID=AC...
TWILIO_AUTH_TOKEN=...
TWILIO_WHATSAPP_FROM=whatsapp:+14155238886
JWT_SECRET=secret-key-here
JWT_EXPIRES_HOURS=8
```

**Nota**: Este issue incorpora el setup básico de Twilio WhatsApp necesario para el Portal. El sistema completo de suscripciones y alertas automáticas se implementará en el issue #035.

**Semana**: 4

---

### 🎨 Issue #019: Pantalla de login: CUIT + código OTP, sin contraseña

**Prioridad**: CRÍTICA
**Estimación**: 2 horas
**Labels**: `frontend`, `ux`
**Dependencias**: #017, #018

**Descripción**: Formulario de login passwordless con flujo de dos pasos.

**Flujo**:
1. Usuario ingresa CUIT → POST /auth/request-code
2. Mensaje: "Te enviamos un código por WhatsApp"
3. Input del código → POST /auth/verify
4. Guarda JWT en sessionStorage → redirect a portal.html

**Archivos a crear**:
- `login.html`
- `styles/login.css`
- `scripts/auth.js`

**Tareas**:
- [ ] Formulario con input CUIT (formato validado)
- [ ] Botón "Enviar código"
- [ ] Input para código OTP (6 caracteres)
- [ ] Estados de carga (spinner)
- [ ] Mensajes de error inline
- [ ] Guardar JWT en sessionStorage
- [ ] Redirect a portal.html tras login exitoso

**Criterios de aceptación**:
- [ ] Validación de formato CUIT (XX-XXXXXXXX-X)
- [ ] Estados de carga visibles
- [ ] Mensajes de error claros
- [ ] JWT almacenado correctamente
- [ ] Redirect automático tras login

**Semana**: 4

---

### 📊 Issue #020: Endpoint GET /proveedor/perfil — datos del legajo autenticado

**Prioridad**: ALTA
**Estimación**: 2 horas
**Labels**: `backend`
**Dependencias**: #018

**Descripción**: Endpoint protegido que retorna los datos del proveedor autenticado.

**Endpoint**:
- `GET /proveedores/{cuit}`
- Header: `Authorization: Bearer <JWT>`

**Response**:
```json
{
  "cuit": "20-28734190-4",
  "razon_social": "Transportes Huemul SA",
  "rubro": "Transporte y Logística",
  "localidad": "Kilómetro 3 Sur",
  "email": "admin@huemul.com.ar",
  "whatsapp": "+54 297 412-3890",
  "estado_inscripcion": "activo",
  "completitud_legajo": 78,
  "fecha_inscripcion": "2026-01-15"
}
```

**Archivos a crear/modificar**:
- `backend/routers/proveedores.py`
- `backend/middleware/auth.py` (verificación JWT)

**Tareas**:
- [ ] Middleware de verificación JWT
- [ ] Endpoint GET con autenticación
- [ ] Lectura de datos del CSV
- [ ] Cálculo de completitud del legajo
- [ ] Manejo de errores (JWT inválido, proveedor no encontrado)

**Criterios de aceptación**:
- [ ] Solo accesible con JWT válido
- [ ] Retorna datos completos del proveedor
- [ ] Error 401 si JWT inválido o expirado
- [ ] Error 404 si CUIT no existe

**Semana**: 4

---

### 📊 Issue #021: Screen Dashboard: KPIs, licitaciones compatibles y estado de inscripción

**Prioridad**: ALTA
**Estimación**: 3 horas
**Labels**: `frontend`, `ux`
**Dependencias**: #017, #020, #003 (scraper)

**Descripción**: Primera pantalla del portal tras login. Muestra resumen ejecutivo del proveedor.

**Componentes**:
1. **4 Stat Cards** (KPIs):
   - Licitaciones compatibles activas
   - Ofertas presentadas (total)
   - Adjudicaciones obtenidas
   - Alertas recibidas este mes

2. **Tabla de licitaciones activas**:
   - Filtradas por rubro del proveedor
   - Ordenadas por fecha de cierre
   - Badge "Para vos" en compatibles

3. **Timeline de inscripción**:
   - Estado actual (activo/pendiente/vencido)
   - Hitos completados
   - Acciones pendientes

4. **Alert banner** (condicional):
   - Si hay documentación por vencer (< 14 días)

**Archivos a modificar**:
- `portal.html` (agregar section #dashboard)
- `scripts/dashboard.js`

**Tareas**:
- [ ] Crear layout de dashboard
- [ ] Implementar 4 stat cards con íconos
- [ ] Tabla de licitaciones compatibles (filtrar por rubro)
- [ ] Timeline de estado de inscripción
- [ ] Alert banner condicional (lógica: fecha_venc < hoy + 14 días)
- [ ] Fetch de datos desde API

**Criterios de aceptación**:
- [ ] KPIs calculados correctamente
- [ ] Licitaciones filtradas por rubro del proveedor
- [ ] Timeline muestra estado actual
- [ ] Alert banner aparece solo si aplica

**Semana**: 4

---

### 📄 Issue #022: Screen Mi Legajo: datos, documentación y rubros

**Prioridad**: MEDIA
**Estimación**: 2 horas
**Labels**: `frontend`
**Dependencias**: #017, #020

**Descripción**: Pantalla con información completa del proveedor.

**Secciones**:
1. **Card: Datos de la empresa**
   - Field grid 2 columnas
   - Razón social, CUIT, rubro, localidad, email, WhatsApp
   - Fecha de inscripción, N° Padrón

2. **Card: Documentación**
   - Tabla con estado de documentos
   - Estados: vigente, por vencer, pendiente
   - Columnas: Documento, Estado, Vencimiento

3. **Card: Rubros habilitados**
   - Lista de rubros con badges

**Archivos a modificar**:
- `portal.html` (agregar section #legajo)
- `scripts/legajo.js`

**Tareas**:
- [ ] Layout con 3 cards
- [ ] Field grid para datos de empresa
- [ ] Tabla de documentación con badges de estado
- [ ] Lista de rubros con badges
- [ ] Botón "Actualizar datos" (placeholder)

**Nota**: En el prototipo, los datos de documentación son estáticos/simulados ya que el CSV de proveedores no tiene esa columna aún. Dejar hooks comentados para integración futura.

**Criterios de aceptación**:
- [ ] Datos cargados desde endpoint /proveedores/{cuit}
- [ ] Documentación simulada pero estructura lista
- [ ] Rubros mostrados como badges
- [ ] Responsive en mobile

**Semana**: 5

---

### 📋 Issue #023: Screen Licitaciones: tabla con filtros y tag "Para vos"

**Prioridad**: ALTA
**Estimación**: 2 horas
**Labels**: `frontend`, `ux`
**Dependencias**: #017, #003 (scraper), #019

**Descripción**: Tabla completa de licitaciones con filtros y personalización.

**Features**:
- Tabla de todas las licitaciones (GET /licitaciones)
- Filtros por rubro y estado
- Tag "Para vos" en licitaciones compatibles con rubro del proveedor
- Botón "Ver con IA" para compatibles (abre chat con contexto)
- Botón "Ver pliego" para las demás

**Archivos a modificar**:
- `portal.html` (agregar section #licitaciones)
- `scripts/licitaciones.js`

**Tareas**:
- [ ] Tabla de licitaciones con data del scraper
- [ ] Filtros: dropdown rubro, dropdown estado
- [ ] Lógica de matching rubro proveedor vs licitación
- [ ] Tag visual "Para vos" en compatibles
- [ ] Botón primario "Ver con IA" → abre #chat con contexto
- [ ] Botón ghost "Ver pliego" → abre URL externa

**Criterios de aceptación**:
- [ ] Tabla muestra todas las licitaciones
- [ ] Filtros funcionan correctamente
- [ ] Tag "Para vos" solo en licitaciones compatibles
- [ ] Botones contextuales según compatibilidad
- [ ] Click en "Ver con IA" abre chat con licitación precargada

**Semana**: 5

---

### 📊 Issue #024: Screen Mis Ofertas: historial con estado y métricas

**Prioridad**: MEDIA
**Estimación**: 1.5 horas
**Labels**: `frontend`
**Dependencias**: #017, #019

**Descripción**: Pantalla de historial de ofertas presentadas (simulado en v1).

**Componentes**:
1. **Stat row** (4 KPIs):
   - Total ofertado (monto)
   - Adjudicaciones obtenidas
   - En evaluación
   - Tasa de éxito (%)

2. **Tabla de historial**:
   - Licitación, Fecha presentación, Monto ofertado, Estado
   - Badge por estado: adjudicada (verde), en evaluación (gold), no adjudicada (rojo)

**Archivos a modificar**:
- `portal.html` (agregar section #ofertas)
- `scripts/ofertas.js`

**Tareas**:
- [ ] Stat row con 4 KPIs
- [ ] Tabla de historial
- [ ] Badges de estado (adjudicada, en evaluación, no adjudicada)
- [ ] Datos simulados hardcodeados por CUIT

**Nota**: En prototipo, datos simulados/hardcodeados. Estructura de tabla lista para integrar con backend real en sprint posterior.

**Criterios de aceptación**:
- [ ] KPIs calculados desde datos simulados
- [ ] Tabla con badges de estado correctos
- [ ] Estructura lista para backend real
- [ ] Responsive

**Semana**: 5

---

### 📚 Issue #025: Screen Normativa: lista navegable con acceso al chat IA

**Prioridad**: BAJA
**Estimación**: 1.5 horas
**Labels**: `frontend`
**Dependencias**: #017

**Descripción**: Lista de documentos normativos con enlaces y acceso al asistente.

**Documentos a incluir**:
- Ley II N°76 (Contrataciones Chubut)
- Ley N°4829 (Compre Chubut)
- Decreto 777/06
- Pliego de Bases y Condiciones Generales (PBCG)
- Formularios oficiales

**Componentes**:
- Lista navegable de documentos
- Cada item clickeable (abre documento en nueva pestaña o muestra resumen inline)
- Banner superior: "¿Tenés dudas sobre la normativa? Consultá al asistente IA"
- Quick-chips con preguntas frecuentes

**Archivos a modificar**:
- `portal.html` (agregar section #normativa)
- `scripts/normativa.js`

**Tareas**:
- [ ] Lista de documentos normativos
- [ ] Links a PDFs (externos o assets)
- [ ] Banner CTA al asistente IA
- [ ] Quick-chips con preguntas frecuentes sobre normativa
- [ ] Click en chip → abre #chat con pregunta precargada

**Criterios de aceptación**:
- [ ] Todos los documentos listados
- [ ] Links funcionales
- [ ] Banner invita a usar el asistente
- [ ] Quick-chips abren chat con contexto

**Semana**: 5

---

### 🤖 Issue #026: Screen Asistente IA: chat embebido con contexto del proveedor

**Prioridad**: ALTA
**Estimación**: 3 horas
**Labels**: `frontend`, `backend`
**Dependencias**: #017, #003 (scraper), #019, #023

**Descripción**: Mover el widget flotante del index.html a esta pantalla dedicada con contexto personalizado.

**Features**:
- Chat lee JWT del proveedor
- Pasa rubro, CUIT y licitaciones compatibles al endpoint POST /chat
- System prompt incluye contexto del proveedor
- Streaming (SSE o chunked) para respuesta fluida
- Quick-chips contextuales según la pantalla desde la que se accede

**Archivos a modificar**:
- `portal.html` (agregar section #chat)
- `backend/routers/chat.py` (agregar contexto del proveedor)
- `scripts/chat.js`

**Tareas**:
- [ ] Layout de chat embebido en portal
- [ ] Lectura de JWT para extraer datos del proveedor
- [ ] Modificar endpoint POST /chat para aceptar contexto adicional
- [ ] Actualizar system prompt con datos del proveedor
- [ ] Implementar streaming (SSE)
- [ ] Quick-chips contextuales (ej: si viene de #licitaciones, ofrecer preguntar sobre esa licitación)
- [ ] Historial de conversación persistente

**System prompt actualizado**:
```
Sos Codi, asistente virtual de la Municipalidad de Comodoro Rivadavia.
Estás hablando con {nombre_proveedor}, CUIT {cuit}, del rubro {rubro}.

Licitaciones compatibles con su rubro:
- {lista_de_licitaciones}

Tu función es ayudar con consultas personalizadas sobre licitaciones,
normativa y procesos municipales.

Tono: Amigable, profesional, voseo rioplatense.
```

**Criterios de aceptación**:
- [ ] Chat carga contexto del proveedor desde JWT
- [ ] Respuestas personalizadas según rubro
- [ ] Streaming funciona correctamente
- [ ] Quick-chips contextuales según origen
- [ ] Historial se mantiene durante la sesión

**Semana**: 5

---

### 🎨 Issue #027: Reemplazar widget flotante del index.html por CTA y preview card

**Prioridad**: MEDIA
**Estimación**: 2 horas
**Labels**: `design`, `frontend`
**Dependencias**: #016, #017

**Descripción**: El botón FAB flotante del index se reemplaza por elementos integrados en la página.

**Cambios en index.html**:
1. **Hero section**:
   - CTA prominente "Acceder como proveedor" → lleva a login.html
   - Botón secundario "Ver licitaciones activas" (público)

2. **Feature cards** (6 cards en grid 3×2):
   - Mi Portal de Proveedor
   - Licitaciones Activas
   - Asistente IA
   - Normativa
   - Calendario de Aperturas
   - Alertas WhatsApp

3. **Preview del asistente** (card inferior):
   - Mensaje de bienvenida del bot
   - 4 chips de consultas frecuentes
   - Botón "Abrir chat completo" → lleva a portal.html#chat

**Archivos a modificar**:
- `index.html` (remover FAB, agregar nuevo layout)
- `styles/index.css`

**Tareas**:
- [ ] Diseñar hero section con gradiente navy
- [ ] CTA primario "Acceder como proveedor"
- [ ] Grid de 6 feature cards
- [ ] Preview card del asistente
- [ ] Chips de consultas frecuentes
- [ ] Eliminar completamente el widget flotante (FAB)

**Criterios de aceptación**:
- [ ] FAB flotante completamente removido
- [ ] Hero atractivo con CTAs claros
- [ ] Feature cards descriptivas y clickeables
- [ ] Preview del asistente invita a probar

**Semana**: 4

---

### 🔐 Issue #028: Routing y protección de rutas del portal (JWT check)

**Prioridad**: CRÍTICA
**Estimación**: 1 hora
**Labels**: `infra`, `frontend`
**Dependencias**: #018, #019

**Descripción**: Lógica de routing y protección de rutas del portal.

**Funcionalidad**:
- `portal.html` al cargar verifica JWT en sessionStorage
- Si no existe o está expirado → redirect a login.html
- Cada screen del portal comparte este guard
- Logout: botón en sidebar que borra JWT y redirige a index.html
- Chat y licitaciones públicas NO requieren JWT

**Archivos a crear**:
- `scripts/router.js`
- `scripts/auth-guard.js`

**Tareas**:
- [ ] Función de verificación JWT al cargar portal.html
- [ ] Redirect a login.html si JWT inválido/expirado
- [ ] Sistema de routing entre secciones (hash navigation)
- [ ] Botón logout en sidebar
- [ ] Excepciones para rutas públicas

**Criterios de aceptación**:
- [ ] Portal solo accesible con JWT válido
- [ ] Redirect automático a login si no autenticado
- [ ] Navegación entre secciones sin reload
- [ ] Logout funcional
- [ ] Rutas públicas accesibles sin JWT

**Semana**: 4

---

### 🎨 Issue #029: Componentes UI reutilizables: badges, cards, tablas, alerts

**Prioridad**: ALTA
**Estimación**: 2 horas
**Labels**: `design`, `frontend`
**Dependencias**: #016

**Descripción**: Crear sistema de componentes reutilizables documentado.

**Archivos a crear**:
- `components.css`
- `docs/components.md` (documentación)

**Componentes a incluir**:
1. **Badges**:
   - `badge-active` (verde)
   - `badge-pending` (gold)
   - `badge-inactive` (gris)
   - `badge-open` (azul)
   - `badge-closed` (rojo)

2. **Stat card**:
   - Con accent top (`.c-blue`, `.c-green`, `.c-gold`, `.c-sky`)
   - Icono, valor, label

3. **Data table**:
   - Hover y zebra stripes
   - Headers sticky (opcional)

4. **Alert banner**:
   - Variantes: `alert-gold`, `alert-green`, `alert-blue`
   - Con icono y acción

5. **Botones**:
   - `btn-primary`
   - `btn-ghost`
   - `btn-hero-primary`

6. **Chat chip**:
   - Para quick-actions

**Tareas**:
- [ ] Crear components.css con todos los componentes
- [ ] Documentar cada componente en components.md
- [ ] Ejemplos de uso en HTML
- [ ] Variables CSS (tokens) para colores y spacing

**Criterios de aceptación**:
- [ ] Todos los componentes funcionales
- [ ] Documentación clara con ejemplos
- [ ] Tokens CSS bien definidos
- [ ] Fácil de extender por diseñadora

**Semana**: 4

---

## Backlog Priorizado

Los siguientes issues corresponden a features avanzadas que se implementarán después del Portal del Proveedor.

---

### 🔴 Issue #030: Deploy en Railway + Vercel

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

### 🔴 Issue #031: Tests automatizados (pytest)

**Prioridad**: ALTA
**Estimación**: 1.5 semanas
**Dependencias**: #030

**Descripción**: Suite de tests para garantizar calidad del código.

**Tareas**:
- [ ] Setup de pytest + pytest-asyncio
- [ ] Tests unitarios de routers:
  - [ ] `test_chat.py` (POST /chat/message)
  - [ ] `test_licitaciones.py` (CRUD)
  - [ ] `test_proveedores.py` (búsqueda)
  - [ ] `test_auth.py` (OTP y JWT)
- [ ] Tests de servicios:
  - [ ] `test_scraper.py` (parsing HTML)
  - [ ] `test_whatsapp.py` (mock de Twilio)
  - [ ] `test_auth_service.py` (generación OTP/JWT)
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

### 🟡 Issue #032: Métricas y analytics

**Prioridad**: MEDIA
**Estimación**: 1 semana
**Dependencias**: #031

**Descripción**: Implementar tracking de métricas para monitorear uso y performance.

**Métricas a trackear**:
- Número de conversaciones (total, diarias, semanales)
- Mensajes por conversación (promedio)
- Tokens consumidos de Claude API
- Tiempo de respuesta promedio
- Errores (4xx, 5xx)
- Temas más consultados (licitaciones, proveedores, normativa)
- Logins exitosos vs fallidos
- Proveedores activos (diarios, semanales)

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

### 🟡 Issue #033: Panel admin completo

**Prioridad**: MEDIA
**Estimación**: 2 semanas
**Dependencias**: #030

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

### 🟡 Issue #034: Mejoras y automatización del scraper

**Prioridad**: MEDIA
**Estimación**: 1 semana
**Dependencias**: #030

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

### 🟡 Issue #035: Notificaciones WhatsApp automáticas

**Prioridad**: MEDIA
**Estimación**: 1.5 semanas
**Dependencias**: #034

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
- Migrar de JSON files a PostgreSQL (issue #040)
- Twilio WhatsApp Business API (requiere aprobación de Meta)

---

### 🟢 Issue #036: Mejoras de UX en el widget

**Prioridad**: BAJA
**Estimación**: 1 semana
**Dependencias**: #032

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

### 🟢 Issue #037: Soporte multiidioma

**Prioridad**: BAJA
**Estimación**: 2 semanas
**Dependencias**: #036

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

### 🟢 Issue #038: Caché de respuestas frecuentes

**Prioridad**: BAJA
**Estimación**: 1 semana
**Dependencias**: #032

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

### 🔵 Issue #039: Integración con Google Calendar

**Prioridad**: NICE-TO-HAVE
**Estimación**: 2 semanas
**Dependencias**: #035

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

### 🔵 Issue #040: Migración a PostgreSQL

**Prioridad**: NICE-TO-HAVE
**Estimación**: 2 semanas
**Dependencias**: #035

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

### 🔵 Issue #041: Dashboard público de licitaciones

**Prioridad**: NICE-TO-HAVE
**Estimación**: 3 semanas
**Dependencias**: #040

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

### 🔵 Issue #042: Análisis de sentimiento y temas

**Prioridad**: NICE-TO-HAVE
**Estimación**: 2 semanas
**Dependencias**: #032, #040

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

1. **Issue #043**: Integración con sistema de compras municipal (ERP)
2. **Issue #044**: Chatbot por voz (Speech-to-Text + Text-to-Speech)
3. **Issue #045**: Widget embebible para otros municipios (white-label)
4. **Issue #046**: Asistente para armado de ofertas (ayuda a proveedores a completar formularios)
5. **Issue #047**: Blockchain para trazabilidad de licitaciones
6. **Issue #048**: Gamificación (badges para proveedores activos)
7. **Issue #049**: Extensión de Chrome (widget en cualquier sitio)

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
Alta │ #016 🔴     │   #037 🟢
Comp │ #017 🔴     │   #039 🔵
lejid│ #018 🔴     │   #042 🔵
ad   │ #019 🔴     │
     │ #021 🔴     │
     │ #023 🔴     │
─────┼──────────────┼──────────────
Baja │ #030 🟡     │   #036 🟢
Comp │ #031 🟡     │   #038 🟢
lejid│ #033 🟡     │   #040 🔵
ad   │ #034 🟡     │   #041 🔵
     │ #035 🟡     │
```

**Leyenda**:
- 🔴 CRÍTICA: Bloquea el Portal (hacer YA)
- 🟡 ALTA: Importante para producción
- 🟢 MEDIA/BAJA: Nice-to-have
- 🔵 FUTURO: Post v1.0

---

## Estimaciones de Esfuerzo

### Sprint 4-5: Portal del Proveedor

| Issue | Estimación | Sprint |
|-------|------------|--------|
| #016 | 3 hs | Sprint 4 |
| #017 | 2 hs | Sprint 4 |
| #018 | 3 hs | Sprint 4 |
| #019 | 2 hs | Sprint 4 |
| #020 | 2 hs | Sprint 4 |
| #021 | 3 hs | Sprint 4 |
| #027 | 2 hs | Sprint 4 |
| #028 | 1 hs | Sprint 4 |
| #029 | 2 hs | Sprint 4 |
| #022 | 2 hs | Sprint 5 |
| #023 | 2 hs | Sprint 5 |
| #024 | 1.5 hs | Sprint 5 |
| #025 | 1.5 hs | Sprint 5 |
| #026 | 3 hs | Sprint 5 |

**Total Portal**: 33 horas · 2 semanas

### Post-Portal

| Issue | Estimación | Fase |
|-------|------------|------|
| #030 | 1 semana | Fase 3 |
| #031 | 1.5 semanas | Fase 3 |
| #032 | 1 semana | Fase 3 |
| #033 | 2 semanas | Fase 4 |
| #034 | 1 semana | Fase 4 |
| #035 | 1.5 semanas | Fase 4 |
| #036 | 1 semana | Fase 4 |
| #037 | 2 semanas | Fase 4 |
| #038 | 1 semana | Fase 4 |
| #039 | 2 semanas | Fase 5 |
| #040 | 2 semanas | Fase 5 |
| #041 | 3 semanas | Fase 5 |
| #042 | 2 semanas | Fase 5 |

**Total para v1.0 (hasta #038)**: ~19 semanas (~4.5 meses)

---

## Changelog

| Versión | Fecha | Cambios |
|---------|-------|---------|
| 0.1.0 | 2025-02-15 | MVP inicial (#001-#004) |
| 0.2.0 | 2025-03-03 | Documentación completa (#005) |
| 0.3.0 | 2026-03-04 | **Reorganización completa de issues** |
|  |  | - Insertados issues #016-#029 (Portal del Proveedor) |
|  |  | - Renumerados issues #006-#018 → #030-#042 |
|  |  | - Actualizada estructura de fases |
| 1.0.0 | TBD | Deploy + tests + Portal completo (#030-#035) |
| 1.1.0 | TBD | Features avanzadas (#036-#038) |
| 2.0.0 | TBD | PostgreSQL + dashboard público (#040-#042) |

---

## Resumen ejecutivo

### ✅ Completado (Sprints 1-3)
- Chatbot MVP con widget flotante
- Integración Claude API
- Scraper de licitaciones
- Diseño Figma
- Documentación base

### 🆕 En desarrollo (Sprints 4-5)
- **14 issues nuevos** para Portal del Proveedor
- **33 horas estimadas**
- Autenticación OTP por WhatsApp
- 6 secciones del portal
- Sistema de diseño completo

### 📦 Próximamente
- Deploy en producción
- Tests automatizados
- Panel admin completo
- Notificaciones automáticas
- PostgreSQL y escalabilidad

---

**Última actualización**: 2026-03-04
**Versión del documento**: 2.0.0
**Responsable**: Fernando Blanco (@ferblanco75)
