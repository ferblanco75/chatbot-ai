/**
 * Configuración de API según entorno
 * Detecta automáticamente si estamos en local o producción
 */

// Detectar entorno
const isLocal = window.location.hostname === 'localhost' ||
                window.location.hostname === '127.0.0.1' ||
                window.location.hostname === '';

// URLs del backend
const API_CONFIG = {
    local: 'http://localhost:8000',
    production: 'https://chatbot-ai-lhib.onrender.com'
};

// Exportar URL según entorno
const API_URL = isLocal ? API_CONFIG.local : API_CONFIG.production;

// Log para debugging (solo en desarrollo)
if (isLocal) {
    console.log('🔧 Modo desarrollo - Backend:', API_URL);
} else {
    console.log('🚀 Modo producción - Backend:', API_URL);
}

// Exportar para uso en otros scripts
window.API_URL = API_URL;
