# Assets de Documentación

Este directorio contiene imágenes, screenshots y otros assets para la documentación del proyecto.

## Screenshots Necesarios

### Para el README.md

1. **demo-screenshot.png** (referenciado en README.md:10)
   - Screenshot del widget de Codi en acción
   - Resolución recomendada: 1200x800px
   - Formato: PNG con transparencia si es posible
   - Contenido sugerido:
     - Sitio web municipal de fondo
     - Widget abierto mostrando una conversación
     - Al menos 2-3 intercambios (usuario + bot)
     - Visible el FAB, el header y los chips de respuesta rápida

### Para docs/architecture.md

Opcionalmente, se pueden agregar:
- Diagramas de flujo de datos
- Diagramas de secuencia
- Capturas de la API docs (Swagger UI)

### Para docs/development.md

Opcionalmente:
- Screenshot de VS Code con el proyecto abierto
- Screenshot de los tests corriendo
- Screenshot del panel de administración

## Cómo Agregar Screenshots

1. Tomar screenshot (usar herramientas como:
   - **Windows**: Snipping Tool o Win+Shift+S
   - **Mac**: Cmd+Shift+4
   - **Linux**: Flameshot, GNOME Screenshot

2. Optimizar imagen:
   - Usar herramientas como TinyPNG (https://tinypng.com)
   - Objetivo: < 500 KB por imagen

3. Colocar en este directorio (`docs/assets/`)

4. Referenciar en los archivos markdown:
   ```markdown
   ![Descripción](docs/assets/nombre-archivo.png)
   ```

## Archivos Actuales

- README.md (este archivo)

## Archivos Pendientes

- [ ] demo-screenshot.png (para README principal)
