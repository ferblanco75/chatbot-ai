# AsisteCR+ · Guía de Deployment y Conexión

Guía completa para deployar el backend en Render y conectarlo con el frontend.

---

## 🎯 Issue #017: Conexión Frontend-Backend

Esta guía resuelve el **Issue #017** implementando la conexión entre:
- **Frontend**: `dashboard.html` (puede ser deployado en Vercel o servido localmente)
- **Backend**: FastAPI en Render (https://chatbot-ai-lhib.onrender.com)

---

## 📦 Pre-requisitos

### Backend (Render)
- [x] Cuenta en Render (https://render.com)
- [x] Repositorio conectado a Render
- [x] Variables de entorno configuradas

### Frontend
- [x] Navegador moderno (Chrome, Firefox, Edge, Safari)
- [x] Opcionalmente: servidor HTTP local o deploy en Vercel

---

## 🚀 Paso 1: Verificar Backend en Render

### 1.1. Health Check

Verificar que el backend esté activo:

```bash
curl https://chatbot-ai-lhib.onrender.com/health
# Respuesta esperada: {"status":"healthy"}
```

### 1.2. Verificar Endpoints Críticos

```bash
# Licitaciones
curl https://chatbot-ai-lhib.onrender.com/licitaciones | jq

# Root
curl https://chatbot-ai-lhib.onrender.com/ | jq
```

### 1.3. Configurar Variables de Entorno en Render

En el panel de Render (Dashboard > Service > Environment):

```bash
ANTHROPIC_API_KEY=sk-ant-api03-...
TWILIO_ACCOUNT_SID=AC...
TWILIO_AUTH_TOKEN=...
TWILIO_WHATSAPP_FROM=whatsapp:+14155238886
ADMIN_PASSWORD=tu-password-seguro
CORS_ORIGINS=http://localhost:3000,https://tu-dominio.vercel.app
```

**IMPORTANTE**: El `CORS_ORIGINS` debe incluir el origen desde donde se accede al dashboard.

---

## 🌐 Paso 2: CORS - Configuración Crítica

El backend ya tiene configurado CORS en `backend/main.py`:

```python
# backend/main.py (líneas 50-58)
cors_origins_str = os.getenv("CORS_ORIGINS", "http://localhost:3000,https://chatbot-ai-eta.vercel.app")
cors_origins = [origin.strip() for origin in cors_origins_str.split(",")]
logger.info(f"CORS habilitado para: {cors_origins}")

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Solución de problemas CORS:

Si ves errores como `Access-Control-Allow-Origin` en la consola del navegador:

1. **Verificar que el origen esté en CORS_ORIGINS**:
   ```bash
   # En Render, agregar a CORS_ORIGINS:
   CORS_ORIGINS=http://localhost:3000,https://tu-dominio.vercel.app,file://
   ```

2. **Usar servidor HTTP local** (no abrir `dashboard.html` directamente):
   ```bash
   python -m http.server 3000
   # Acceder a: http://localhost:3000/dashboard.html
   ```

3. **Verificar logs en Render**:
   - Panel de Render > Logs
   - Buscar línea: `CORS habilitado para: [...]`
   - Confirmar que incluye tu origen

---

## 📱 Paso 3: Configurar Dashboard (Frontend)

### 3.1. URL del Backend

En `dashboard.html` línea **742**, configurar:

```javascript
// Para desarrollo local con backend en Render
const BACKEND_URL = 'https://chatbot-ai-lhib.onrender.com';

// Para desarrollo local con backend local
// const BACKEND_URL = 'http://localhost:8000';
```

### 3.2. Abrir Dashboard

**Opción A: Servidor HTTP local (recomendado)**

```bash
# Desde el root del proyecto
python -m http.server 3000

# Abrir en navegador:
# http://localhost:3000/dashboard.html
```

**Opción B: Directamente (puede tener problemas CORS)**

```bash
open dashboard.html
# O doble clic en el archivo
```

**Opción C: Deploy en Vercel**

```bash
vercel --prod
# Configurar BACKEND_URL antes de deployar
```

---

## 🧪 Paso 4: Testing Completo

### 4.1. Licitaciones Activas

- ✅ Tabla carga automáticamente al abrir dashboard
- ✅ Filtro por búsqueda funciona
- ✅ Filtro por rubro funciona
- ✅ Botón "Actualizar" ejecuta scraper y recarga
- ✅ Contador de licitaciones abiertas aparece en título

### 4.2. Configurar Alertas

- ✅ Formulario valida campos requeridos
- ✅ Al menos un canal (email o WhatsApp) es requerido
- ✅ Al menos un rubro debe seleccionarse
- ✅ Mensaje de éxito aparece al guardar
- ✅ Mensaje de error aparece si falla
- ✅ Botón muestra spinner mientras guarda

### 4.3. Mi Portal Proveedor (Demo)

- ✅ KPIs se muestran correctamente
- ✅ Datos de ejemplo visibles
- ✅ Banner de "Vista demo" presente

### 4.4. Asistente IA Codi

- ✅ FAB (botón flotante) abre panel chat
- ✅ Chips de respuestas rápidas funcionan
- ✅ Input acepta texto y Enter
- ✅ Respuestas del bot aparecen con animación
- ✅ Scroll automático al último mensaje

### Testing desde Consola del Navegador:

```javascript
// Test 1: Cargar licitaciones
fetch('https://chatbot-ai-lhib.onrender.com/licitaciones')
  .then(r => r.json())
  .then(d => console.log('Licitaciones:', d.length));

// Test 2: Suscripción
fetch('https://chatbot-ai-lhib.onrender.com/notificaciones/subscribe', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({
    nombre: 'Test User',
    email: 'test@example.com',
    rubros: ['obras']
  })
}).then(r => r.json()).then(console.log);

// Test 3: Chat
fetch('https://chatbot-ai-lhib.onrender.com/chat/', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({
    messages: [{role: 'user', content: 'Hola'}]
  })
}).then(r => r.json()).then(console.log);
```

---

## 🐛 Troubleshooting

### Problema: "Error al cargar licitaciones"

**Causa**: Backend no responde o CORS bloqueado

**Solución**:
```bash
# 1. Verificar que backend esté activo
curl https://chatbot-ai-lhib.onrender.com/health

# 2. Ver logs en Render
# Panel > Logs > Buscar errores

# 3. Verificar CORS_ORIGINS incluye tu origen
```

---

### Problema: "Mixed Content" (HTTP/HTTPS)

**Causa**: Frontend en HTTPS intenta llamar backend HTTP

**Solución**:
- Render usa HTTPS por defecto
- Asegurarse que `BACKEND_URL` use `https://`
- Si frontend está en `file://`, usar servidor HTTP local

---

### Problema: Backend "dormido" (Render Free Tier)

**Causa**: Render Free Tier duerme servicios después de 15 min de inactividad

**Solución**:
```bash
# Primera llamada puede tardar 30-60 segundos
# El backend se "despierta" automáticamente
curl https://chatbot-ai-lhib.onrender.com/health

# Esperar respuesta, luego refrescar dashboard
```

---

### Problema: "Error al guardar configuración" (Alertas)

**Causa**: Validación falla o backend rechaza request

**Solución**:
1. Verificar formato WhatsApp: `+549XXXXXXXXXX`
2. Ver consola del navegador (F12) para detalles del error
3. Verificar que `backend/data/` tenga permisos de escritura en Render

---

## 📊 Arquitectura de Conexión

```
┌─────────────────────────────────────────────────┐
│  dashboard.html (Frontend)                      │
│  • JavaScript vanilla                           │
│  • Fetch API para HTTP requests                 │
│  • BACKEND_URL configurado                      │
└────────────┬────────────────────────────────────┘
             │
             │ HTTP/HTTPS
             │
┌────────────▼────────────────────────────────────┐
│  Render (Backend)                               │
│  https://chatbot-ai-lhib.onrender.com          │
│  • FastAPI + uvicorn                            │
│  • CORS configurado                             │
│  • Variables de entorno                         │
└────────────┬────────────────────────────────────┘
             │
             ├─► Anthropic API (Claude)
             ├─► Twilio API (WhatsApp)
             └─► backend/data/ (JSON/CSV)
```

---

## 🔐 Seguridad

### Variables de Entorno Sensibles

**NUNCA commitear**:
- `.env`
- `ANTHROPIC_API_KEY`
- `TWILIO_AUTH_TOKEN`
- `ADMIN_PASSWORD`

**Usar en su lugar**:
- `.env.example` (template sin valores reales)
- Variables de entorno en Render
- `.gitignore` protege archivos sensibles

### CORS Restrictivo

En producción, limitar `CORS_ORIGINS` solo a dominios autorizados:

```bash
# Desarrollo
CORS_ORIGINS=http://localhost:3000

# Producción
CORS_ORIGINS=https://asistecr-demo.vercel.app
```

---

## 📝 Checklist de Deployment

### Backend (Render)

- [ ] Servicio creado en Render
- [ ] Repositorio conectado
- [ ] Branch `master` o `develop2-nueva-web` configurado
- [ ] Variables de entorno configuradas
- [ ] Build command: `pip install -r requirements.txt`
- [ ] Start command: `uvicorn backend.main:app --host 0.0.0.0 --port $PORT`
- [ ] Health check: `/health` responde 200

### Frontend

- [ ] `BACKEND_URL` apunta a Render
- [ ] CORS incluye origen del frontend
- [ ] Dashboard abre sin errores de consola
- [ ] Las 4 funcionalidades probadas

### Testing

- [ ] Licitaciones cargan correctamente
- [ ] Filtros funcionan
- [ ] Formulario de alertas guarda
- [ ] Chat con Codi responde
- [ ] Scroll to top aparece al bajar

---

## 🎉 Issue #017 Completado

Una vez que:
1. ✅ Backend en Render responde correctamente
2. ✅ CORS configurado para permitir frontend
3. ✅ Dashboard carga y funciona sin errores
4. ✅ Las 4 funcionalidades probadas

**El Issue #017 está resuelto**.

---

## 📞 Soporte

- **Backend logs**: Panel de Render > Logs
- **Frontend errors**: Consola del navegador (F12)
- **API testing**: Postman, curl, o consola del navegador

---

## 🔗 Links Útiles

- **Backend Render**: https://dashboard.render.com
- **Render Docs**: https://render.com/docs
- **FastAPI CORS**: https://fastapi.tiangolo.com/tutorial/cors/
- **Vercel Deploy**: https://vercel.com/docs
