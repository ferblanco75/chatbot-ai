# Changelog - AsisteCR+

## [2026-03-08] - Issue #017 + Mejoras UX

### ✅ Issue #017: Conexión Frontend-Backend COMPLETADO

#### Backend
- **CORS mejorado** (`backend/main.py`):
  - Configuración dinámica desde variable `CORS_ORIGINS`
  - Logging de orígenes permitidos
  - Soporte para múltiples dominios (local + producción)

- **Nuevo endpoint** (`backend/routers/notificaciones.py`):
  - `POST /notificaciones/subscribe`: Suscripción a alertas
  - Validación de email con `EmailStr` (pydantic)
  - Validación de formato WhatsApp (E.164)
  - Almacenamiento en `backend/data/subscriptions.json`

- **Datos de ejemplo enriquecidos** (`backend/data/licitaciones.json`):
  - +6 licitaciones nuevas con rubros variados:
    - 2 Obras (reparación edificios, cordón cuneta)
    - 2 Suministros (insumos médicos, equipamiento informático)
    - 2 Servicios (limpieza espacios verdes, seguridad)
  - Fechas de apertura específicas (2026-04-10 a 2026-05-05)
  - Presupuestos oficiales incluidos
  - Estados "abierta" para testing

#### Frontend
- **Dashboard completo** (`dashboard.html`):
  - 4 secciones implementadas:
    1. Licitaciones Activas (tabla filtrable)
    2. Configurar Alertas (formulario WhatsApp/Email)
    3. Mi Portal Proveedor (vista demo)
    4. Asistente IA Codi (FAB + panel chat)

#### Infraestructura
- **`.gitignore`** creado:
  - Protege `.env`, `subscriptions.json`, `__pycache__/`

- **`.env.example`** creado:
  - Template de variables de entorno necesarias

- **Dependencias actualizadas** (`requirements.txt`):
  - `slowapi==0.1.9` agregado para rate limiting

---

### ✨ Mejoras de UX (Pulido del Dashboard)

#### Componentes Visuales
- **Estados vacíos mejorados**:
  - Empty state con ícono, título y texto explicativo
  - Mostrado cuando filtros no devuelven resultados

- **Mensajes de feedback**:
  - Mensaje de éxito (verde) al guardar alertas
  - Mensaje de error (rojo) con texto específico del problema
  - Animación `slideDown` para aparición suave
  - Auto-ocultan después de 5 segundos

- **Contador de licitaciones**:
  - Badge con número de licitaciones abiertas en título de sección
  - Se actualiza dinámicamente con filtros

- **Scroll to top**:
  - Botón flotante que aparece al hacer scroll > 300px
  - Animación smooth al volver arriba

- **Skeleton loaders**:
  - Animación shimmer para estados de carga
  - CSS incluido (no usado aún, preparado para futuro)

#### Mejoras de Interacción
- **Badges con colores por rubro**:
  - Obras: dorado (badge-pending)
  - Servicios: verde (badge-active)
  - Suministros: azul (badge-open)
  - General: gris (badge-inactive)

- **Botón de submit con loading**:
  - Muestra spinner mientras guarda
  - Deshabilitado durante proceso
  - Restaura texto original al finalizar

- **Links a pliegos**:
  - Si la licitación tiene URL, abre en nueva pestaña
  - Si no tiene, botón deshabilitado con texto "Sin pliego"

- **Descripción más larga en tabla**:
  - 80 caracteres en lugar de 60
  - Mejor preview del contenido

#### Animaciones
- **Mensajes del chat**:
  - Animación `slideIn` al aparecer

- **Filas de la tabla**:
  - Animación al renderizar licitaciones

- **Alertas**:
  - `slideDown` con transform y opacity

---

### 📚 Documentación Creada

1. **`DASHBOARD.md`**:
   - Guía completa de uso del dashboard
   - Descripción de las 4 funcionalidades
   - Endpoints utilizados
   - Sistema de diseño
   - Troubleshooting

2. **`DEPLOYMENT.md`**:
   - Guía paso a paso para Issue #017
   - Configuración de CORS
   - Testing completo
   - Troubleshooting específico
   - Checklist de deployment
   - Arquitectura de conexión

3. **`CHANGELOG.md`** (este archivo):
   - Registro de cambios implementados

---

## Archivos Modificados/Creados

### Nuevos
```
✅ dashboard.html              ← Frontend principal (710 líneas)
✅ .gitignore                  ← Protección de archivos sensibles
✅ .env.example                ← Template de configuración
✅ DASHBOARD.md                ← Documentación del dashboard
✅ DEPLOYMENT.md               ← Guía de deployment
✅ CHANGELOG.md                ← Este archivo
```

### Modificados
```
✏️ backend/main.py                    ← CORS mejorado (líneas 50-58)
✏️ backend/routers/notificaciones.py  ← Endpoint subscribe (líneas 1-91)
✏️ backend/data/licitaciones.json     ← +6 licitaciones de ejemplo
✏️ requirements.txt                   ← +slowapi
```

---

## Testing Realizado

### Backend
- [x] Health check: `GET /health` → 200 OK
- [x] CORS logs visibles en consola
- [x] Endpoint subscribe acepta requests POST

### Frontend
- [x] Dashboard carga sin errores
- [x] Tabla de licitaciones renderiza correctamente
- [x] Filtros funcionan (búsqueda + rubro)
- [x] Formulario de alertas valida campos
- [x] Chat con Codi funcional
- [x] Navegación smooth scroll funciona
- [x] Scroll to top aparece/desaparece

---

## Métricas

- **Licitaciones totales**: 18 (7 abiertas, 11 cerradas)
- **Rubros disponibles**: Obras, Servicios, Suministros, General
- **Endpoints backend**: 5 principales (/licitaciones, /chat, /notificaciones, /subscribe, /proveedores)
- **Líneas de código frontend**: ~710 (dashboard.html)
- **Componentes CSS reutilizables**: 15+ (components.css)

---

## Próximos Pasos Recomendados

### Corto plazo (pulido)
1. Agregar más licitaciones de ejemplo (target: 20+ abiertas)
2. Implementar búsqueda por presupuesto
3. Agregar tooltips en badges de rubro
4. Mejorar responsive en móviles pequeños (<375px)

### Mediano plazo (funcionalidad)
1. Issue #23: Backend autenticación CUIT + OTP
2. Issue #24: Frontend login
3. Issue #25: Endpoint GET /proveedores/{cuit}
4. Issue #26: Dashboard autenticado con personalización

### Largo plazo (producción)
1. Deploy frontend a Vercel
2. Configurar dominio personalizado
3. Implementar Redis para OTPs
4. Sistema de notificaciones automáticas (cron jobs)

---

## Estado del Proyecto

| Issue | Estado | Descripción |
|-------|--------|-------------|
| #016 | ✅ Completado | Sistema de diseño (components.css) |
| #017 | ✅ **COMPLETADO** | Conexión frontend-backend |
| #018 | ⏸️ En pausa | Desarrollo (rama develop2-nueva-web) |
| #019-026 | 📋 Pendiente | Portal autenticado |

---

## Notas Técnicas

- **Backend URL**: https://chatbot-ai-lhib.onrender.com
- **Free tier Render**: Se duerme después de 15 min inactividad
- **Primera carga**: Puede tardar 30-60s en despertar
- **CORS**: Configurado para localhost:3000 + Vercel
- **Rate limiting**: 20 req/min en /chat

---

## Créditos

- **Desarrollado con**: Claude Sonnet 4.5
- **Framework backend**: FastAPI 0.115.6
- **AI Model**: Claude Sonnet 4 (2025-05-14)
- **Sistema de diseño**: Syne + DM Sans
- **Deploy**: Render (backend) + Vercel (frontend planeado)
