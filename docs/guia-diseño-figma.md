# Guía de Diseño Figma - Issue #004

## ¿Qué es Figma y para qué lo necesitamos?

**Figma** es una herramienta de diseño colaborativo en la nube (similar a Photoshop pero orientada a UI/UX). La usamos para:

1. **Documentar visualmente** la identidad del asistente
2. **Crear componentes reutilizables** que luego se traducen a código
3. **Diseñar los estados** de la interfaz (idle, cargando, error, etc.)
4. **Probar responsividad** (desktop, tablet, mobile)
5. **Facilitar handoff** entre diseño y desarrollo

---

## ¿Qué debe contener el archivo Figma?

Según el issue #004, se necesitan:

### 1. Componentes del Widget

Cada uno debe ser un **componente Figma** (reutilizable) con sus variantes:

#### a) FAB (Floating Action Button)
- **Estados**:
  - Default (cerrado)
  - Hover
  - Pressed
  - Open (cuando el panel está abierto)
- **Medidas**: 64x64px (móvil: 56x56px)
- **Contenido**: Avatar de Codi centrado

#### b) Panel de Chat
- **Medidas**: 400x600px (desktop), full screen mobile
- **Estructura completa**:
  - Header con avatar + nombre
  - Área de mensajes (scrolleable)
  - Input con botón enviar
- **Estados**:
  - Empty (sin mensajes)
  - Con conversación
  - Scrolled

#### c) Burbuja Bot (mensaje del asistente)
- **Estilo**: Fondo blanco, borde redondeado (16px), sombra sutil
- **Alineación**: Izquierda
- **Estados**:
  - Normal
  - Typing (con animación de "...")
  - Con chips de respuesta rápida

#### d) Burbuja Usuario
- **Estilo**: Fondo azul (#1055A8), texto blanco, bordes redondeados
- **Alineación**: Derecha
- **Estados**: Normal

#### e) Chips (botones de respuesta rápida)
- **Estilo**: Borde azul, fondo blanco, padding 8x16px
- **Estados**:
  - Default
  - Hover (fondo azul, texto blanco)
  - Pressed

#### f) Burbuja de Bienvenida
- **Ubicación**: Flotante sobre el FAB
- **Contenido**: Texto + botón cerrar
- **Estados**: Show/Hide con animación

---

### 2. Estados del Chat

El archivo Figma debe mostrar **pantallas completas** (frames) de estos escenarios:

#### Estado: Idle (Inicial)
- Panel cerrado
- FAB visible
- Burbuja de bienvenida visible (aparece a los 3 segundos)

#### Estado: Typing (Escribiendo)
- Panel abierto
- Mensaje del usuario enviado
- Burbuja bot con "..." (indicador de carga)

#### Estado: Error
- Panel abierto
- Mensaje de error en burbuja bot
- Ejemplo: "Disculpá, hubo un error al conectar con el servidor..."

#### Estado: Conversación Activa
- Panel abierto con varios mensajes
- Mezcla de burbujas user/bot
- Algunos mensajes con chips
- Área de scroll visible

---

### 3. Versión Mobile

Todas las pantallas anteriores deben tener su versión mobile:

- **Panel**: Ocupa toda la pantalla (full screen menos 16px de margen)
- **FAB**: 56x56px en vez de 64x64px
- **Chips**: Texto más pequeño (0.8rem)
- **Burbuja de bienvenida**: Ancho máximo reducido

**Breakpoints**:
- Desktop: 768px+
- Tablet: 480-768px
- Mobile: <480px

---

## Paleta de Colores a Usar

Ya está definida en el código actual:

```css
Azul Marino:  #0B2347  (fondos oscuros, textos principales)
Azul:         #1055A8  (botones, enlaces, header)
Dorado:       #E8A000  (acentos, antena del avatar)
Blanco:       #FFFFFF  (fondos, textos en azul)
Gris Claro:   #F5F5F5  (fondo del área de mensajes)
Gris Medio:   #E0E0E0  (bordes)
Gris Texto:   #666666  (textos secundarios)
```

---

## Tipografía

**Fuente principal**: Nunito (Google Fonts)

**Pesos a usar**:
- Regular (400): Textos normales
- SemiBold (600): Chips, subtítulos
- Bold (700): Títulos, nombres
- ExtraBold (800): Encabezados principales

**Tamaños**:
- Mensajes: 0.95rem
- Chips: 0.85rem
- Título chat: 1rem
- Subtítulo: 0.8rem

---

## Avatar de Codi

El avatar actual es un **SVG placeholder** en `assets/codi-avatar.svg`.

**Tarea de la diseñadora**:
1. Revisar el SVG actual (robot simple con antena dorada)
2. Decidir si:
   - **Opción A**: Mejorarlo manteniendo el concepto (robot minimalista)
   - **Opción B**: Crear uno completamente nuevo (puede ser otro estilo: ilustración, mascota, icono abstracto)
3. Entregar el nuevo avatar en **formato SVG vectorial** optimizado
4. Incluir versiones en diferentes tamaños si fuera necesario

**Requisitos del avatar**:
- Debe funcionar bien en círculo (FAB y header)
- Debe ser legible en 40x40px (tamaño mínimo)
- Usar colores de la paleta definida
- Transmitir confianza y accesibilidad

---

## Guía de Tono de Voz

**Pendiente de definir** - La diseñadora debe documentar 3-4 principios:

**Ejemplo sugerido**:

1. **Claro y directo**: Evitamos jerga técnica, explicamos en lenguaje cotidiano
2. **Amigable sin ser informal**: Tuteamos (vos sos, podés, consultá) pero mantenemos profesionalismo
3. **Proactivo y útil**: Anticipamos necesidades con chips de respuesta rápida
4. **Empático con errores**: Si algo falla, nos disculpamos y damos alternativas

La diseñadora puede ajustar estos principios según su visión del personaje de Codi.

---

## Entregables Esperados

Al completar el issue #004, la diseñadora debe entregar:

1. ✅ **Link al archivo Figma** con:
   - Página de componentes (FAB, burbujas, chips, panel)
   - Página de estados (idle, typing, error, conversación)
   - Página de versión mobile

2. ✅ **Avatar en SVG** optimizado (reemplaza el actual)

3. ✅ **Documento de tono de voz** (puede ser en Figma o markdown)

4. ✅ **Paleta de colores documentada** en Figma con:
   - Nombres de cada color
   - Códigos hex
   - Usos recomendados (ej: "Azul Marino para títulos")

---

## Flujo de Trabajo Recomendado

1. **Revisar implementación actual**:
   - Abrir `index.html` en el navegador
   - Interactuar con el widget (abrir, cerrar, enviar mensajes)
   - Identificar qué mejorar

2. **Crear file en Figma**:
   - Importar tipografía Nunito
   - Crear auto-layout components
   - Usar variables de color (Design Tokens)

3. **Diseñar componentes base**:
   - Empezar por el FAB (más simple)
   - Seguir con burbujas
   - Luego el panel completo

4. **Crear estados**:
   - Duplicar componentes y mostrar variantes
   - Usar animaciones/prototipos para transiciones

5. **Versión mobile**:
   - Duplicar frames desktop
   - Ajustar medidas según breakpoints

6. **Handoff**:
   - Compartir link de Figma con acceso de "comentarios"
   - Marcar qué componentes son prioritarios
   - Exportar assets (SVG del avatar)

---

## Preguntas Frecuentes

### ¿Puedo cambiar la paleta de colores?
**Sí**, pero debe estar justificado (ej: contraste insuficiente, no cumple accesibilidad WCAG). Si hay cambios, documentarlos claramente.

### ¿Puedo cambiar el nombre "Codi"?
**No sin aprobación**. El nombre ya está en producción. Si hay una propuesta mejor, plantearla en el issue.

### ¿Necesito diseñar la web municipal completa?
**No**. Solo el widget del chatbot (FAB + panel). La web municipal es solo contexto.

### ¿Qué hago si el avatar actual no me convence?
Proponer alternativas en Figma. Mostrar 2-3 opciones y justificar cuál recomendás.

---

## Recursos Útiles

- **Archivo Figma de referencia**: [Boti GCBA](https://buenosaires.gob.ar/jefaturadegabinete/innovacion/boti) (inspiración, no copiar)
- **Guía de accesibilidad**: [WCAG 2.1](https://www.w3.org/WAI/WCAG21/quickref/)
- **Contraste de colores**: [Contrast Checker](https://webaim.org/resources/contrastchecker/)
- **Iconografía**: [Heroicons](https://heroicons.com/), [Lucide](https://lucide.dev/)

---

## Contacto

Para consultas sobre el issue #004:
- **GitHub**: github.com/ferblanco75/chatbot-ai/issues/4
- **Repo**: github.com/ferblanco75/chatbot-ai
