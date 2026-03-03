# Codi - Brief de Diseño de Personaje

## Identidad del Personaje

**Nombre**: Codi
**Origen**: Derivado de "Comodoro" (Comodoro Rivadavia)
**Rol**: Asistente virtual de compras y licitaciones de la Municipalidad de Comodoro Rivadavia

## Personalidad

- **Tono**: Amigable, cercano, profesional pero no distante
- **Estilo comunicacional**: Voseo rioplatense ("¿Cómo estás?", "Podés consultar...")
- **Carácter**: Servicial, paciente, conocedor del proceso burocrático pero capaz de explicarlo de forma simple
- **Inspiración**: Similar a "Boti" del Gobierno de la Ciudad de Buenos Aires

## Referentes Visuales

### Similar a:
- **Boti** (GCBA): Robot amigable, colores institucionales, estilo flat/minimal
- **Asistentes municipales digitales**: Diseño simple, reconocible, adaptable a diferentes tamaños

### A evitar:
- Diseños muy infantiles o caricaturescos
- Exceso de detalles que dificulten la legibilidad en tamaños pequeños
- Formas agresivas o que transmitan frialdad burocrática

## Especificaciones Técnicas

### Paleta de Colores Obligatoria
**Colores de la Municipalidad de Comodoro Rivadavia**:
- **Azul Marino**: `#0B2347` (color primario)
- **Azul**: `#1055A8` (color secundario)
- **Dorado**: `#E8A000` (acento)
- **Blanco**: `#FFFFFF`
- **Grises**: `#F5F5F5`, `#E0E0E0`, `#666666`

### Formato de Entrega
1. **SVG optimizado** (uso en web, escalable sin pérdida de calidad)
2. **PNG transparente** en múltiples resoluciones:
   - 512x512px (alta resolución)
   - 256x256px (estándar)
   - 128x128px (thumbnails)
   - 64x64px (favicon)
3. **Versiones**:
   - Avatar circular (para header del chat)
   - Ícono para FAB (Floating Action Button)
   - Versión completa del personaje (opcional, para páginas de marketing)

### Consideraciones de Uso

**Contextos de aparición**:
- Widget flotante (64x64px): debe ser reconocible en tamaño pequeño
- Header del chat (40x40px): versión simplificada si es necesario
- Burbuja de bienvenida: puede incluir medio cuerpo o cuerpo completo
- Páginas de ayuda/onboarding: versión completa del personaje

**Estados/Variaciones** (opcional):
- Estado neutral (default)
- Estado "pensando" (durante typing indicator)
- Estado "feliz" (mensaje enviado exitosamente)
- Estado "alerta" (errores o advertencias)

## Concepto Visual

### Opción 1: Robot Amigable (Recomendado)
- Cabeza geométrica simple (cuadrada/redondeada)
- Antena característica con punta dorada
- Ojos expresivos, grandes, amigables
- Sonrisa sutil
- Cuerpo opcional (torso simple si se requiere versión completa)
- Colores: cuerpo azul marino/azul, detalles en dorado

### Opción 2: Avatar Humanoide Minimalista
- Silueta humana muy simplificada
- Rasgos faciales mínimos (ojos + sonrisa)
- Posible uso de casco/gorra con logo municipal
- Colores institucionales aplicados al vestuario

### Opción 3: Símbolo Abstracto
- Forma geométrica que sugiere un personaje (círculo + detalles)
- Concepto de "asistente digital" sin ser literalmente un robot
- Alto nivel de abstracción pero manteniendo calidez

## Restricciones y Requisitos

### Obligatorios
✅ Uso exclusivo de la paleta de colores municipal
✅ Diseño escalable (debe funcionar desde 40x40px hasta tamaños grandes)
✅ Formato SVG optimizado para web (código limpio, sin elementos innecesarios)
✅ Fondo transparente en todas las versiones
✅ Expresión amigable y accesible

### Deseables
⭐ Versión animada simple (opcional, para typing indicator)
⭐ Variaciones de expresión facial (neutral, feliz, pensando)
⭐ Documentación de uso (guía de estilo del personaje)

## Inspiración y Referencias

### Estilo Visual Deseado
- **Flat design** con degradados sutiles
- **Formas redondeadas** (border-radius generoso)
- **Líneas limpias** y contrastes claros
- **Minimalismo funcional** (cada elemento tiene un propósito)

### Ejemplos de Buenas Prácticas
- Iconografía de Google Material Design (simplicidad, claridad)
- Ilustraciones de Slack (amigables, profesionales)
- Avatar de Boti (GCBA) - tono y estilo similar

## Cronograma Sugerido

1. **Concepto inicial** (sketches/bocetos): 3-5 propuestas
2. **Refinamiento** del concepto elegido
3. **Vectorización** y ajustes de color
4. **Pruebas** en diferentes tamaños y contextos
5. **Entrega final** con todos los formatos

## Contacto y Aprobación

**Aprobador**: Fernando Blanco
**Criterios de aceptación**:
- Alineación con identidad municipal
- Funcionalidad en todos los tamaños requeridos
- Transmisión de cercanía y profesionalismo
- Diferenciación clara de otros asistentes virtuales

---

**Nota**: Este documento es un brief para ilustradores profesionales. La implementación actual del proyecto usa un SVG temporal simplificado que puede ser reemplazado cuando se cuente con el diseño profesional final.
