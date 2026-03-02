"""
Wrapper para envío de mensajes WhatsApp usando Twilio.

Documentación: https://www.twilio.com/docs/whatsapp/quickstart/python
"""

import logging
import os
from typing import Optional

from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException

logger = logging.getLogger(__name__)


def get_twilio_client() -> Optional[Client]:
    """
    Obtiene un cliente de Twilio configurado con las credenciales del entorno.

    Returns:
        Cliente de Twilio o None si no hay credenciales configuradas
    """
    account_sid = os.getenv("TWILIO_ACCOUNT_SID")
    auth_token = os.getenv("TWILIO_AUTH_TOKEN")

    if not account_sid or not auth_token:
        logger.error("Credenciales de Twilio no configuradas")
        return None

    return Client(account_sid, auth_token)


async def send_whatsapp_message(to: str, body: str) -> str:
    """
    Envía un mensaje de WhatsApp usando Twilio.

    Args:
        to: Número de teléfono destino en formato E.164 (ej: +5492974123456)
        body: Contenido del mensaje (máx. 1600 caracteres)

    Returns:
        SID del mensaje enviado

    Raises:
        Exception: Si falla el envío
    """
    client = get_twilio_client()

    if not client:
        raise Exception("Cliente de Twilio no disponible. Verificar credenciales.")

    whatsapp_from = os.getenv("TWILIO_WHATSAPP_FROM")
    if not whatsapp_from:
        raise Exception("Número de WhatsApp origen no configurado (TWILIO_WHATSAPP_FROM)")

    # Validar formato del número destino
    if not to.startswith("whatsapp:"):
        to = f"whatsapp:{to}"

    if not whatsapp_from.startswith("whatsapp:"):
        whatsapp_from = f"whatsapp:{whatsapp_from}"

    try:
        logger.info(f"Enviando mensaje WhatsApp a {to}")

        message = client.messages.create(
            from_=whatsapp_from,
            body=body,
            to=to
        )

        logger.info(f"Mensaje enviado exitosamente. SID: {message.sid}")

        return message.sid

    except TwilioRestException as e:
        logger.error(f"Error de Twilio al enviar mensaje: {e.msg} (código: {e.code})")
        raise Exception(f"Error de Twilio: {e.msg}")

    except Exception as e:
        logger.error(f"Error inesperado al enviar mensaje: {e}")
        raise


async def verify_twilio_config() -> dict:
    """
    Verifica la configuración de Twilio sin enviar mensajes.

    Returns:
        Dict con información de la configuración
    """
    client = get_twilio_client()

    if not client:
        return {
            "configured": False,
            "error": "Credenciales no configuradas"
        }

    try:
        # Obtener información de la cuenta
        account = client.api.accounts(os.getenv("TWILIO_ACCOUNT_SID")).fetch()

        return {
            "configured": True,
            "account_sid": account.sid,
            "status": account.status,
            "whatsapp_from": os.getenv("TWILIO_WHATSAPP_FROM")
        }

    except TwilioRestException as e:
        return {
            "configured": False,
            "error": f"Error de autenticación: {e.msg}"
        }

    except Exception as e:
        return {
            "configured": False,
            "error": f"Error inesperado: {str(e)}"
        }
