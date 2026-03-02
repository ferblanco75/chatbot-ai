"""
Router para endpoints de notificaciones WhatsApp.
POST /notificaciones - Envía notificación por WhatsApp
"""

import logging
import os
from typing import Optional

from fastapi import APIRouter, HTTPException, Header
from pydantic import BaseModel, Field

from services.whatsapp import send_whatsapp_message

logger = logging.getLogger(__name__)

router = APIRouter()


class NotificacionRequest(BaseModel):
    """Modelo para solicitud de notificación."""
    to: str = Field(..., description="Número de teléfono destino (formato E.164: +549XXXXXXXXXX)")
    mensaje: str = Field(..., min_length=10, max_length=1600, description="Mensaje a enviar")
    tipo: Optional[str] = Field("informativo", description="Tipo de notificación: informativo, urgente, recordatorio")


class NotificacionResponse(BaseModel):
    """Modelo para respuesta de notificación."""
    status: str
    message_sid: Optional[str] = None
    mensaje: str


@router.post("", response_model=NotificacionResponse, status_code=201)
async def enviar_notificacion(
    notificacion: NotificacionRequest,
    x_admin_password: Optional[str] = Header(None)
):
    """
    Envía una notificación por WhatsApp.

    Requiere autenticación admin mediante el header X-Admin-Password.

    - **to**: Número de teléfono en formato E.164 (ej: +5492974123456)
    - **mensaje**: Texto del mensaje (10-1600 caracteres)
    - **tipo**: Tipo de notificación (informativo, urgente, recordatorio)
    """
    # Validar password de admin
    admin_password = os.getenv("ADMIN_PASSWORD")
    if not admin_password or x_admin_password != admin_password:
        raise HTTPException(status_code=401, detail={"error": "No autorizado"})

    # Validar formato de teléfono
    if not notificacion.to.startswith("+"):
        raise HTTPException(
            status_code=400,
            detail={"error": "El número de teléfono debe estar en formato E.164 (comenzar con +)"}
        )

    try:
        # Preparar mensaje con prefijo según tipo
        prefijos = {
            "urgente": "🚨 URGENTE\n",
            "recordatorio": "🔔 Recordatorio\n",
            "informativo": "ℹ️ Información\n"
        }

        prefijo = prefijos.get(notificacion.tipo, "")
        mensaje_completo = f"{prefijo}{notificacion.mensaje}\n\nMunicipalidad de Comodoro Rivadavia"

        # Enviar mensaje
        message_sid = await send_whatsapp_message(
            to=notificacion.to,
            body=mensaje_completo
        )

        logger.info(f"Notificación enviada a {notificacion.to}: {message_sid}")

        return NotificacionResponse(
            status="enviado",
            message_sid=message_sid,
            mensaje="Notificación enviada correctamente"
        )

    except Exception as e:
        logger.error(f"Error enviando notificación: {e}")
        raise HTTPException(
            status_code=500,
            detail={"error": f"Error al enviar notificación: {str(e)}"}
        )


@router.post("/test")
async def test_notificacion(x_admin_password: Optional[str] = Header(None)):
    """
    Endpoint de prueba para verificar la configuración de Twilio.
    Envía un mensaje de prueba al número configurado en TWILIO_TEST_NUMBER.
    """
    # Validar password de admin
    admin_password = os.getenv("ADMIN_PASSWORD")
    if not admin_password or x_admin_password != admin_password:
        raise HTTPException(status_code=401, detail={"error": "No autorizado"})

    test_number = os.getenv("TWILIO_TEST_NUMBER")
    if not test_number:
        raise HTTPException(
            status_code=400,
            detail={"error": "No hay número de prueba configurado (TWILIO_TEST_NUMBER)"}
        )

    try:
        mensaje = "🧪 Mensaje de prueba del Asistente de Compras - Municipalidad de Comodoro Rivadavia"

        message_sid = await send_whatsapp_message(
            to=test_number,
            body=mensaje
        )

        return {
            "status": "ok",
            "mensaje": "Mensaje de prueba enviado correctamente",
            "message_sid": message_sid,
            "to": test_number
        }

    except Exception as e:
        logger.error(f"Error en prueba de notificación: {e}")
        raise HTTPException(
            status_code=500,
            detail={"error": f"Error en prueba: {str(e)}"}
        )
