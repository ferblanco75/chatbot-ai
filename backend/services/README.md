# Backend Services

Servicios auxiliares del backend de AsisteCR+.

---

## Scraper de Licitaciones

### Descripción

El scraper extrae las licitaciones publicadas en el sitio oficial de la Municipalidad de Comodoro Rivadavia:
- **URL**: https://www.comodoro.gov.ar/secciones/licitaciones/
- **Output**: `backend/data/licitaciones.json`

### Uso

#### Ejecución manual

```bash
# Desde la raíz del proyecto
python -m backend.services.scraper
```

El scraper:
1. Descarga el HTML del sitio oficial
2. Parsea los elementos `<article>` con BeautifulSoup
3. Extrae: título, número de expediente, fecha de publicación, estado, URL
4. Guarda los resultados en `backend/data/licitaciones.json`

#### Ejecución desde código

```python
from backend.services.scraper import scrape_licitaciones

# Scraping con guardado automático
licitaciones = await scrape_licitaciones(save_to_file=True)

# Scraping sin guardar (solo retorna datos)
licitaciones = await scrape_licitaciones(save_to_file=False)
```

#### Integración con API

El endpoint `GET /licitaciones?refresh=true` ejecuta automáticamente el scraper y combina los resultados con las licitaciones existentes.

### Características

- **Retry automático**: 3 intentos con backoff exponencial (2^n segundos)
- **Headers realistas**: User-Agent y Accept configurados para evitar bloqueos
- **Manejo de errores**: Logging detallado de cada intento y error
- **Parsing robusto**: Múltiples selectores CSS como fallback
- **Formato de salida**: JSON con array de objetos normalizados

### Estructura de datos

Cada licitación incluye:

```json
{
  "id": "SCRAPE-123456789",
  "titulo": "Licitación Pública Nº 01/2026...",
  "descripcion": "...",
  "numero_expediente": "01/2026",
  "fecha_publicacion": "2026-02-11",
  "fecha_apertura": "Ver detalle",
  "presupuesto_oficial": null,
  "rubro": "general",
  "estado": "abierta",
  "url_pliego": "https://www.comodoro.gov.ar/...",
  "contacto": "licitacionesyconcursos@comodoro.gov.ar"
}
```

### Estados posibles

- `abierta`: Licitación activa, acepta ofertas
- `cerrada`: Licitación finalizada (detectada por palabra "finalizada" en título)

### Logging

El scraper usa el módulo `logging` de Python. Para ver logs detallados:

```python
import logging
logging.basicConfig(level=logging.INFO)
```

### Troubleshooting

**Error: No se encontraron licitaciones**
- Verificar que el sitio https://www.comodoro.gov.ar/secciones/licitaciones/ esté accesible
- El selector CSS puede haber cambiado. Revisar `scraper.py:186-192`

**Error: Timeout después de 30s**
- Problema de conectividad o sitio caído
- El retry automático reintentará hasta 3 veces

**Error: No se pudo guardar el archivo**
- Verificar permisos de escritura en `backend/data/`
- Verificar que el directorio exista (se crea automáticamente)

---

## Otros servicios

### WhatsApp (Twilio)

Wrapper para envío de notificaciones por WhatsApp (implementar en `whatsapp.py`).

### Auth Service

Gestión de OTPs y JWTs para autenticación del Portal del Proveedor (implementar en `auth_service.py`).
