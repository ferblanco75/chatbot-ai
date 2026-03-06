# Sistema de Diseño - AsisteCR+ Portal del Proveedor

Documentación completa del sistema de componentes reutilizables, tokens de diseño y guía de uso para developers.

---

## Tabla de Contenidos

- [Tokens de Diseño](#tokens-de-diseño)
  - [Paleta de Colores](#paleta-de-colores)
  - [Tipografía](#tipografía)
  - [Sombras y Radios](#sombras-y-radios)
- [Componentes](#componentes)
  - [Badges](#badges)
  - [Cards](#cards)
  - [Stat Cards](#stat-cards)
  - [Alert Banners](#alert-banners)
  - [Botones](#botones)
  - [Data Tables](#data-tables)
  - [Chips](#chips)
  - [Sidebar Navigation](#sidebar-navigation)
- [Utilidades](#utilidades)
  - [Grids](#grids)
  - [Flex Helpers](#flex-helpers)
  - [Espaciado](#espaciado)
  - [Texto](#texto)
  - [Progress Bar](#progress-bar)
- [Responsive](#responsive)

---

## Tokens de Diseño

### Paleta de Colores

Todas las variables CSS están definidas en `components.css` bajo `:root`.

#### Colores Primarios

| Variable | Hex | Uso |
|----------|-----|-----|
| `--navy` | `#0B2347` | Sidebar, hero, headings principales |
| `--blue` | `#1055A8` | Botón primario, links, acciones principales |
| `--sky` | `#2278D4` | Acento activo, navegación, bordes de foco |
| `--gold` | `#E8A000` | Alertas importantes, brand accent, notificaciones |

#### Colores Semánticos

| Variable | Hex | Uso |
|----------|-----|-----|
| `--green` | `#0F7A45` | Estados activos, adjudicaciones, success |
| `--red` | `#C0302A` | Errores, licitaciones no adjudicadas, destructive actions |

#### Colores Light (Fondos)

| Variable | Hex | Uso |
|----------|-----|-----|
| `--sky-l` | `#EDF4FF` | Fondos de chips y badges open, hover states |
| `--gold-l` | `#FFF8E6` | Fondos de alertas gold |
| `--green-l` | `#E6F5EE` | Fondos de badges activos |

#### Escala de Grises

| Variable | Hex | Uso |
|----------|-----|-----|
| `--gray-1` | `#F4F7FC` | Fondo de página general |
| `--gray-2` | `#E8EDF5` | Bordes, separadores, dividers |
| `--gray-3` | `#9CA8BD` | Texto disabled, placeholders |
| `--gray-4` | `#6B7A90` | Texto secundario, labels |

#### Neutros

| Variable | Hex | Uso |
|----------|-----|-----|
| `--white` | `#FFFFFF` | Fondos de cards, contenedores |
| `--text` | `#2A3342` | Texto principal del body |

---

### Tipografía

**Fuentes**: Syne (headings) + DM Sans (cuerpo)

#### Headings - Syne

```css
h1, h2, h3, h4, h5, h6 {
  font-family: 'Syne', sans-serif;
  line-height: 1.2;
  color: var(--navy);
}
```

**Pesos disponibles**: 600 (SemiBold), 700 (Bold), 800 (ExtraBold)

**Uso recomendado**:
- **800**: Títulos principales, brand, KPIs, stats
- **700**: Subtítulos, headings de secciones
- **600**: Labels importantes, nav activo

#### Body - DM Sans

```css
body {
  font-family: 'DM Sans', sans-serif;
  font-size: 14px;
  line-height: 1.6;
}
```

**Pesos disponibles**: 400 (Regular), 500 (Medium), 600 (SemiBold)

**Uso recomendado**:
- **400**: Texto de párrafos, descripciones
- **500**: Nav items, botones, labels
- **600**: Texto enfatizado, headers de tablas

---

### Sombras y Radios

#### Sombras

| Variable | Valor | Uso |
|----------|-------|-----|
| `--shadow-sm` | `0 1px 3px rgba(11,35,71,.08)` | Cards, componentes elevados sutiles |
| `--shadow-md` | `0 4px 12px rgba(11,35,71,.12)` | Hover states, dropdowns |
| `--shadow-lg` | `0 8px 24px rgba(11,35,71,.16)` | Modales, popovers, elementos flotantes |

#### Radios de Borde

| Variable | Valor | Uso |
|----------|-------|-----|
| `--radius` | `10px` | Componentes estándar |
| `--radius-sm` | `6px` | Botones pequeños, inputs |
| `--radius-lg` | `14px` | Cards principales |
| `--radius-xl` | `20px` | Contenedores hero, secciones grandes |

---

## Componentes

### Badges

Indicadores de estado para licitaciones, proveedores y documentos.

#### Variantes

| Clase | Color | Uso |
|-------|-------|-----|
| `.badge-active` | Verde | Estado activo, vigente |
| `.badge-pending` | Gold | Pendiente, en evaluación |
| `.badge-inactive` | Gris | Inactivo, vencido |
| `.badge-open` | Azul | Licitación abierta |
| `.badge-closed` | Rojo | Licitación cerrada |

#### Ejemplo de Uso

```html
<!-- Badge de licitación abierta -->
<span class="badge badge-open">Abierta</span>

<!-- Badge de estado activo -->
<span class="badge badge-active">Vigente</span>

<!-- Badge pendiente -->
<span class="badge badge-pending">En evaluación</span>
```

#### Anatomía

- Dot indicator de 6px antes del texto
- Padding: `4px 10px`
- Font size: `11px`
- Font weight: `600`
- Text transform: `uppercase`
- Border radius: `20px` (pill shape)

---

### Cards

Contenedores principales de contenido.

#### Card Básica

```html
<div class="card">
  <div class="card-header">
    <h3>Título de la Card</h3>
  </div>
  <div class="card-body">
    <p>Contenido de la card...</p>
  </div>
</div>
```

#### Especificaciones

**Card container**:
- Background: `var(--white)`
- Border: `1px solid var(--gray-2)`
- Border radius: `var(--radius-lg)` (14px)
- Box shadow: `var(--shadow-sm)`

**Card header**:
- Padding: `20px 24px 16px`
- Border bottom: `1px solid var(--gray-2)`
- Display: `flex` con `justify-content: space-between`

**Card body**:
- Padding: `20px 24px`

---

### Stat Cards

Cards especializadas para mostrar KPIs con accent color superior.

#### Variantes de Color

| Clase | Color del Accent | Uso |
|-------|------------------|-----|
| `.c-blue` | Azul | Licitaciones, general |
| `.c-green` | Verde | Adjudicaciones, success metrics |
| `.c-gold` | Gold | Alertas, notificaciones |
| `.c-sky` | Sky | Actividad, engagement |

#### Ejemplo de Uso

```html
<div class="stat-card c-blue">
  <div class="stat-icon">📊</div>
  <div class="stat-val">23</div>
  <div class="stat-label">Licitaciones compatibles</div>
</div>
```

#### Anatomía

- Border top de 3px con color del accent
- Padding: `18px 20px`
- Hover: `translateY(-2px)` con shadow-md
- **stat-val**: Syne 800, 26px, navy
- **stat-label**: DM Sans 400, 12px, gray-4

#### Ejemplo de Grid con 4 Stats

```html
<div class="grid-4">
  <div class="stat-card c-blue">
    <div class="stat-val">23</div>
    <div class="stat-label">Licitaciones compatibles</div>
  </div>
  <div class="stat-card c-green">
    <div class="stat-val">12</div>
    <div class="stat-label">Adjudicaciones obtenidas</div>
  </div>
  <div class="stat-card c-gold">
    <div class="stat-val">5</div>
    <div class="stat-label">Alertas recibidas</div>
  </div>
  <div class="stat-card c-sky">
    <div class="stat-val">78%</div>
    <div class="stat-label">Completitud legajo</div>
  </div>
</div>
```

---

### Alert Banners

Alertas contextuales para mensajes importantes.

#### Variantes

| Clase | Color | Uso |
|-------|-------|-----|
| `.alert-gold` | Gold | Advertencias importantes, documentación por vencer |
| `.alert-green` | Verde | Mensajes de éxito, confirmaciones |
| `.alert-blue` | Azul | Información general, tips |

#### Ejemplo de Uso

```html
<div class="alert-banner alert-gold">
  <div class="alert-icon">⚠️</div>
  <div class="alert-text">
    <div class="alert-title">Documentación por vencer</div>
    <div class="alert-sub">Tu constancia de inscripción vence en 12 días</div>
  </div>
  <div class="alert-action">
    <button class="btn-ghost">Renovar</button>
  </div>
</div>
```

#### Anatomía

- Padding: `14px 18px`
- Display: `flex` con `align-items: flex-start`
- Gap: `12px`
- Margin bottom: `20px`
- Border radius: `var(--radius)` (10px)

---

### Botones

#### Variantes Principales

| Clase | Uso |
|-------|-----|
| `.btn-primary` | Acción principal (guardar, enviar, confirmar) |
| `.btn-ghost` | Acción secundaria (cancelar, ver más) |
| `.btn-hero-primary` | CTA principal del landing (gold, bold) |
| `.btn-hero-ghost` | CTA secundario del landing (transparente) |

#### Ejemplos

```html
<!-- Botón primario -->
<button class="btn btn-primary">Guardar cambios</button>

<!-- Botón ghost -->
<button class="btn btn-ghost">Cancelar</button>

<!-- Botón con ícono -->
<button class="btn btn-primary">
  <svg>...</svg>
  Descargar pliego
</button>
```

#### Especificaciones

**btn-primary**:
- Background: `var(--blue)`
- Color: `#fff`
- Padding: `9px 20px`
- Border radius: `8px`
- Hover: background → `var(--sky)`, translateY(-1px)

**btn-ghost**:
- Background: `transparent`
- Border: `1.5px solid var(--gray-2)`
- Color: `var(--gray-4)`
- Hover: border-color → `var(--blue)`, color → `var(--blue)`

**btn-hero-primary**:
- Background: `var(--gold)`
- Color: `var(--navy)`
- Padding: `12px 28px`
- Font: Syne 700, 14px
- Hover: background → `#F5B420`, translateY(-2px), shadow dorado

---

### Data Tables

Tablas optimizadas para licitaciones, ofertas e historial.

#### Ejemplo de Uso

```html
<table class="data-table">
  <thead>
    <tr>
      <th>Licitación</th>
      <th>Estado</th>
      <th>Fecha</th>
      <th>Monto</th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <div class="td-main">Licitación N° 45/2025</div>
        <div class="td-sub">Servicio de limpieza</div>
      </td>
      <td><span class="badge badge-open">Abierta</span></td>
      <td>15/03/2026</td>
      <td>$2.500.000</td>
      <td><button class="btn-ghost">Ver</button></td>
    </tr>
  </tbody>
</table>
```

#### Especificaciones

**thead th**:
- Padding: `11px 14px`
- Font size: `11px`
- Font weight: `700`
- Color: `var(--gray-4)`
- Text transform: `uppercase`
- Letter spacing: `0.06em`
- Border bottom: `1.5px solid var(--gray-2)`

**tbody td**:
- Padding: `13px 14px`
- Font size: `13px`
- Border bottom: `1px solid var(--gray-2)`
- Hover: background → `var(--sky-l)`

**td-main / td-sub**:
- `.td-main`: font-weight 500, color navy
- `.td-sub`: font-size 11px, color gray-4, margin-top 2px

---

### Chips

Quick actions para chat, filtros y acciones rápidas.

#### Ejemplo de Uso

```html
<!-- Chip individual -->
<span class="chip">¿Cuáles son las licitaciones activas?</span>

<!-- Grupo de chips -->
<div style="display: flex; gap: 8px; flex-wrap: wrap;">
  <span class="chip">Licitaciones abiertas</span>
  <span class="chip">Requisitos para participar</span>
  <span class="chip">Consultar normativa</span>
</div>
```

#### Especificaciones

- Background: `var(--sky-l)`
- Border: `1px solid rgba(34,120,212,.25)`
- Color: `var(--blue)`
- Border radius: `20px`
- Padding: `5px 12px`
- Font size: `12px`
- Font weight: `500`
- Hover: background → `var(--blue)`, color → `#fff`, translateY(-1px)

---

### Sidebar Navigation

Navegación principal del portal (desktop) ubicada en el lado izquierdo.

#### Estructura

```html
<aside class="sidebar">
  <!-- Brand -->
  <div class="sidebar-brand">
    <h1>AsisteCR+</h1>
    <p>Portal del Proveedor</p>
  </div>

  <!-- User info -->
  <div class="sidebar-user">
    <div class="user-avatar">TH</div>
    <div class="user-info">
      <h3>Transportes Huemul</h3>
      <p>20-28734190-4</p>
    </div>
  </div>

  <!-- Nav items -->
  <nav class="sidebar-nav">
    <a href="#dashboard" class="nav-item active">
      <svg class="nav-icon">...</svg>
      Dashboard
    </a>
    <a href="#licitaciones" class="nav-item">
      <svg class="nav-icon">...</svg>
      Licitaciones
      <span class="nav-badge">3</span>
    </a>
  </nav>
</aside>
```

#### Especificaciones

**Sidebar container**:
- Width: `260px`
- Background: `var(--navy)`
- Height: `100vh`
- Position: `sticky`, top 0
- Display: `flex`, `flex-direction: column`

**Nav item**:
- Padding: `12px 20px`
- Color: `rgba(255,255,255,.7)`
- Font size: `14px`
- Hover: background `rgba(255,255,255,.05)`

**Nav item active**:
- Background: `rgba(34,120,212,.15)`
- Color: `var(--white)`
- Border left: `3px solid var(--sky)`

**Nav badge**:
- Background: `var(--gold)`
- Color: `var(--navy)`
- Padding: `2px 8px`
- Border radius: `12px`
- Font size: `11px`
- Margin left: `auto`

---

## Utilidades

### Grids

Sistemas de grid predefinidos con gap de 20px.

```html
<!-- Grid 2 columnas -->
<div class="grid-2">
  <div class="card">...</div>
  <div class="card">...</div>
</div>

<!-- Grid 3 columnas -->
<div class="grid-3">
  <div>...</div>
  <div>...</div>
  <div>...</div>
</div>

<!-- Grid 4 columnas (stats) -->
<div class="grid-4">
  <div class="stat-card">...</div>
  <div class="stat-card">...</div>
  <div class="stat-card">...</div>
  <div class="stat-card">...</div>
</div>
```

**Responsive**: En mobile (max-width: 768px) todos los grids colapsan a 1 columna.

---

### Flex Helpers

```html
<!-- Flex con space-between -->
<div class="flex-between">
  <h3>Título</h3>
  <button>Acción</button>
</div>
```

**Definición**:
```css
.flex-between {
  display: flex;
  align-items: center;
  justify-content: space-between;
}
```

---

### Espaciado

#### Gaps

Clases de utilidad para espaciado con flexbox/grid:

| Clase | Gap |
|-------|-----|
| `.gap-8` | `8px` |
| `.gap-12` | `12px` |
| `.gap-16` | `16px` |
| `.gap-20` | `20px` |

```html
<div style="display: flex;" class="gap-12">
  <span class="chip">Chip 1</span>
  <span class="chip">Chip 2</span>
</div>
```

#### Divider

```html
<hr class="divider">
```

**Especificaciones**:
- Border: `none`
- Border top: `1px solid var(--gray-2)`
- Margin: `20px 0`

---

### Texto

#### Clases de utilidad

```html
<!-- Texto pequeño secundario -->
<p class="text-small">Última actualización: 05/03/2026</p>

<!-- Texto monoespaciado (CUIT, códigos) -->
<span class="text-mono">20-28734190-4</span>
```

**Especificaciones**:
- `.text-small`: font-size `12px`, color `var(--gray-4)`
- `.text-mono`: font-family `monospace`, font-size `12px`

---

### Progress Bar

Barra de progreso para completitud de legajo.

```html
<div class="progress-track">
  <div class="progress-bar" style="width: 78%"></div>
</div>
<p class="text-small">78% completado</p>
```

**Especificaciones**:

**progress-track**:
- Background: `var(--gray-2)`
- Border radius: `4px`
- Height: `6px`
- Margin: `6px 0`

**progress-bar**:
- Background: `var(--blue)`
- Height: `100%`
- Border radius: `4px`
- Transition: `width 0.3s ease`

---

## Responsive

### Breakpoints

| Breakpoint | Width | Comportamiento |
|------------|-------|----------------|
| **Mobile** | `≤ 768px` | Grids colapsan a 1 col, sidebar oculto, bottom nav visible |
| **Tablet** | `769px - 1024px` | Sidebar visible, grids en 2-3 columnas |
| **Desktop** | `≥ 1025px` | Layout completo, grids en 3-4 columnas |

### Mobile: Bottom Nav

En mobile, la sidebar se oculta y aparece una bottom navigation con 4 ítems principales:

```html
<nav class="bottom-nav">
  <a href="#dashboard" class="bottom-nav-item active">
    <svg class="bottom-nav-icon">...</svg>
    Inicio
  </a>
  <a href="#licitaciones" class="bottom-nav-item">
    <svg class="bottom-nav-icon">...</svg>
    Licitaciones
  </a>
  <a href="#chat" class="bottom-nav-item">
    <svg class="bottom-nav-icon">...</svg>
    Asistente
  </a>
  <a href="#legajo" class="bottom-nav-item">
    <svg class="bottom-nav-icon">...</svg>
    Perfil
  </a>
</nav>
```

**Especificaciones**:
- Display: `grid` con 4 columnas iguales
- Position: `sticky`, bottom 0
- Background: `var(--white)`
- Border top: `1px solid var(--gray-2)`
- Padding: `8px 0`

---

## Convenciones de Uso

### 1. Jerarquía de Color

- **Navy** para headings y elementos de máxima jerarquía
- **Blue/Sky** para acciones y elementos interactivos
- **Gold** para destacar notificaciones y alertas importantes
- **Green** para feedback positivo
- **Red** solo para errores y acciones destructivas

### 2. Consistencia en Espaciado

Usar múltiplos de 4px para padding/margin:
- **8px**: gaps mínimos
- **12px**: espaciado compacto
- **16px**: espaciado estándar
- **20px**: separación entre secciones
- **24px**: padding de cards

### 3. Tipografía

- **Syne** solo para headings, stats y brand
- **DM Sans** para todo el texto de UI
- No mezclar weights inconsistentes (usar 400, 500, 600/700 solamente)

### 4. Interactividad

Todos los elementos clickeables deben tener:
- `cursor: pointer`
- Transición suave (`transition: all 0.2s`)
- Estado hover visible
- Feedback visual (color change, shadow, transform)

---

## Extensión del Sistema

### Agregar Nuevos Componentes

1. **Definir en `components.css`** con comentarios descriptivos
2. **Documentar en este archivo** con:
   - Descripción del componente
   - Variantes disponibles
   - Ejemplo de código HTML
   - Especificaciones técnicas
3. **Seguir convenciones** de naming: `.nombre-componente-variante`
4. **Usar tokens** existentes (no hardcodear colores/tamaños)

### Ejemplo de Nuevo Componente

```css
/* ═══════════════════════════════════════════════════════════════
   TOOLTIP (nuevo componente)
   ═══════════════════════════════════════════════════════════════ */
.tooltip {
  position: relative;
  display: inline-block;
}

.tooltip-text {
  visibility: hidden;
  background: var(--navy);
  color: var(--white);
  text-align: center;
  padding: 6px 10px;
  border-radius: var(--radius-sm);
  position: absolute;
  z-index: 1;
  bottom: 125%;
  left: 50%;
  transform: translateX(-50%);
  font-size: 12px;
  white-space: nowrap;
}

.tooltip:hover .tooltip-text {
  visibility: visible;
}
```

---

## Changelog del Sistema

| Versión | Fecha | Cambios |
|---------|-------|---------|
| 1.0.0 | 2026-03-05 | Sistema inicial con todos los componentes base del portal |

---

**Última actualización**: 2026-03-05
**Mantenedor**: Fernando Blanco (@ferblanco75)
**Archivo fuente**: `/components.css`
