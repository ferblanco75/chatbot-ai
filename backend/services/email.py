"""
Servicio de envío de emails via Resend.
Documentación: https://resend.com/docs/send-with-python
"""

import logging
import os

import httpx

logger = logging.getLogger(__name__)


async def send_otp_email(to: str, otp: str, razon_social: str) -> str:
    """
    Envía el código OTP por email usando Resend.

    Args:
        to: Email destino
        otp: Código OTP de 6 caracteres
        razon_social: Nombre del proveedor para personalizar el mensaje

    Returns:
        ID del mensaje enviado

    Raises:
        Exception si el envío falla
    """
    api_key = os.getenv("RESEND_API_KEY")
    email_from = os.getenv("EMAIL_FROM", "AsisteCR+ <noreply@asistecr.com>")

    if not api_key:
        raise ValueError("RESEND_API_KEY no configurada")

    html_body = f"""
    <div style="font-family: Arial, sans-serif; max-width: 480px; margin: 0 auto; padding: 32px 24px; background: #F4F7FC; border-radius: 12px;">
        <div style="text-align: center; margin-bottom: 24px;">
            <h1 style="color: #0B2347; font-size: 22px; margin: 0;">AsisteCR+</h1>
            <p style="color: #6B7A90; font-size: 13px; margin: 4px 0 0 0;">Municipalidad de Comodoro Rivadavia</p>
        </div>

        <div style="background: #FFFFFF; border-radius: 10px; padding: 28px 24px; border: 1px solid #E8EDF5;">
            <p style="color: #2A3342; font-size: 15px; margin: 0 0 16px 0;">Hola <strong>{razon_social}</strong>,</p>
            <p style="color: #2A3342; font-size: 14px; margin: 0 0 24px 0;">
                Tu código de acceso al Portal del Proveedor es:
            </p>

            <div style="background: #EDF4FF; border-radius: 8px; padding: 20px; text-align: center; margin-bottom: 24px;">
                <span style="font-family: monospace; font-size: 36px; font-weight: 700; color: #1055A8; letter-spacing: 8px;">{otp}</span>
            </div>

            <p style="color: #6B7A90; font-size: 13px; margin: 0 0 8px 0;">
                Este código es válido por <strong>30 minutos</strong>.
            </p>
            <p style="color: #6B7A90; font-size: 13px; margin: 0;">
                Si no solicitaste este código, ignorá este email.
            </p>
        </div>

        <p style="color: #9CA8BD; font-size: 12px; text-align: center; margin: 20px 0 0 0;">
            Municipalidad de Comodoro Rivadavia · Namuncurá 26 · Chubut, Argentina
        </p>
    </div>
    """

    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://api.resend.com/emails",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            },
            json={
                "from": email_from,
                "to": [to],
                "subject": f"Tu código de acceso al Portal del Proveedor: {otp}",
                "html": html_body
            },
            timeout=10.0
        )

    if response.status_code not in (200, 201):
        logger.error(f"Error Resend: {response.status_code} - {response.text}")
        raise Exception(f"Error al enviar email: {response.status_code}")

    data = response.json()
    logger.info(f"Email OTP enviado a {to} (ID: {data.get('id')})")
    return data.get("id", "ok")
