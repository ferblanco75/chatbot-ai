# AsisteCR+ Dashboard · Guía de Uso

Dashboard público sin autenticación que integra las 4 funcionalidades principales de la plataforma.

---

## 🎯 Funcionalidades

### 1. Licitaciones Activas
- **Visualización en tabla**: Muestra todas las licitaciones abiertas desde el backend
- **Filtros**: Búsqueda por título/expediente y filtro por rubro
- **Actualización manual**: Botón para refrescar datos desde el scraper
- **Endpoint**: `GET /licitaciones` (con parámetro opcional `?refresh=true`)

### 2. Configurar Alertas
- **Formulario de suscripción**: Permite registrarse para recibir notificaciones
- **Canales**: WhatsApp y/o Email (al menos uno requerido)
- **Rubros de interés**: Checkbox múltiple para seleccionar categorías
- **Endpoint**: `POST /notificaciones/subscribe`
- **Persistencia**: Guarda suscripciones en `backend/data/subscriptions.json`

### 3. Mi Portal Proveedor (Demo)
- **Vista estática**: Muestra datos de ejemplo sin autenticación
- **KPIs simulados**: Licitaciones compatibles, estado de inscripción, alertas, ofertas
- **Datos de ejemplo**: CUIT, razón social, rubros, documentación
- **Propósito**: Demostrar capacidades del portal para proveedores

### 4. Asistente IA Codi
- **Chat conversacional**: Implementa el endpoint `POST /chat/` con streaming SSE
- **Contexto**: System prompt incluye licitaciones abiertas actuales
- **Quick actions**: Chips con preguntas predefinidas
- **Animaciones**: FAB (Floating Action Button) y panel deslizable

---

## 🚀 Cómo usar

### Requisitos previos
1. **Backend corriendo**: El dashboard consume la API en `BACKEND_URL` (configurado en línea 742 de dashboard.html)
2. **Variables de entorno**: Configurar `.env` según `.env.example`
3. **Dependencias instaladas**: `pip install -r requirements.txt`

### Paso 1: Levantar el backend

```bash
cd backend
pip install -r ../requirements.txt
uvicorn main:app --reload --port 8000
```

### Paso 2: Abrir el dashboard

```bash
# Opción 1: Abrir directamente el archivo HTML
open dashboard.html

# Opción 2: Servir con un servidor HTTP simple
python -m http.server 3000
# Luego navegar a http://localhost:3000/dashboard.html
```

### Paso 3: Verificar configuración del backend

Asegurarse de que en `dashboard.html` línea 742, `BACKEND_URL` apunte a tu backend:

```javascript
const BACKEND_URL = 'https://chatbot-ai-lhib.onrender.com'; // Para producción
// O
const BACKEND_URL = 'http://localhost:8000'; // Para desarrollo local
```

---

## 📁 Archivos relacionados

```
/
├── dashboard.html          ← Frontend: página principal del dashboard
├── components.css          ← Sistema de diseño compartido
├── .env.example            ← Template de variables de entorno
├── backend/
│   ├── main.py             ← Entry point FastAPI
│   ├── routers/
│   │   ├── licitaciones.py ← GET /licitaciones, POST /licitaciones
│   │   ├── notificaciones.py ← POST /notificaciones/subscribe
│   │   └── chat.py         ← POST /chat/ (streaming SSE)
│   └── data/
│       ├── licitaciones.json     ← Cache de licitaciones
│       └── subscriptions.json    ← Suscripciones a alertas (gitignored)
```

---

## 🔧 Endpoints utilizados

| Endpoint | Método | Descripción | Usado en sección |
|----------|--------|-------------|------------------|
| `/licitaciones` | GET | Lista todas las licitaciones | Licitaciones Activas |
| `/licitaciones?refresh=true` | GET | Actualiza scraper y retorna licitaciones | Botón "Actualizar" |
| `/notificaciones/subscribe` | POST | Crea suscripción a alertas | Configurar Alertas |
| `/chat/` | POST | Chat con Codi (streaming SSE) | Asistente IA |

---

## 🎨 Sistema de diseño

El dashboard reutiliza `components.css` con:

- **Paleta**: Navy (#0B2347), Blue (#1055A8), Gold (#E8A000), Green (#0F7A45)
- **Tipografía**: Syne (headings), DM Sans (body)
- **Componentes**:
  - `.card`, `.stat-card` (tarjetas de contenido)
  - `.badge-active`, `.badge-open`, etc. (estados)
  - `.btn-primary`, `.btn-ghost` (botones)
  - `.data-table` (tablas con hover)
  - `.chip` (quick actions del chat)
  - `.alert-banner` (notificaciones contextuales)

---

## 🧪 Funcionalidades por implementar (futuro)

- [ ] **Login con CUIT**: Integrar `login.html` para autenticación
- [ ] **Portal autenticado**: Migrar a `portal.html` después del login
- [ ] **Filtros avanzados**: Por fecha, presupuesto, localidad
- [ ] **Descargar pliego**: Endpoints para archivos PDF
- [ ] **Notificaciones push**: WebSockets o Server-Sent Events
- [ ] **Panel admin**: Crear/editar licitaciones desde `admin.html`

---

## 🐛 Troubleshooting

### Error: "Error al cargar licitaciones"
- Verificar que el backend esté corriendo
- Revisar CORS en `backend/main.py` (debe incluir el origen del frontend)
- Checkear logs del backend: `uvicorn` imprime errores en consola

### Error: "Error al guardar configuración" (Alertas)
- Verificar que el endpoint `/notificaciones/subscribe` exista
- Revisar que `backend/data/` tenga permisos de escritura
- Validar formato de WhatsApp (debe empezar con `+`)

### Chat no responde
- Verificar variable de entorno `ANTHROPIC_API_KEY` en backend
- Revisar que el modelo `claude-sonnet-4-20250514` esté disponible
- Checkear límites de rate limiting (20 mensajes/minuto)

---

## 📝 Notas de desarrollo

- **Sin estado**: El dashboard no usa sessionStorage ni localStorage (sin login)
- **CORS**: Configurar en backend con `CORS_ORIGINS` en `.env`
- **Rate limiting**: 20 mensajes/minuto en `/chat/` (configurado en `chat.py`)
- **Datos de ejemplo**: La sección "Mi Portal Proveedor" usa datos hardcoded
- **Scraper**: El botón "Actualizar" ejecuta `scraper.py` vía `?refresh=true`

---

## 🚢 Deploy

### Frontend (Vercel)
```bash
# dashboard.html se sirve como página estática
# Configurar BACKEND_URL en el código antes de deployar
vercel --prod
```

### Backend (Railway/Render)
```bash
# Configurar variables de entorno en el panel de Railway/Render
# ANTHROPIC_API_KEY, TWILIO_*, ADMIN_PASSWORD, CORS_ORIGINS
git push origin master  # Auto-deploy configurado
```

---

## 📞 Contacto y soporte

- **Email oficial**: licitacionesyconcursos@comodoro.gov.ar
- **Dirección**: Namuncurá 26, Comodoro Rivadavia, Chubut
- **Horario**: Lunes a Viernes 8:00 - 14:00 hs
