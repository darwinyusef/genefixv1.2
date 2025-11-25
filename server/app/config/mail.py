from typing import List
from fastapi import APIRouter, HTTPException
from fastapi import File, UploadFile, Form
from fastapi.responses import JSONResponse
from jinja2 import Environment, FileSystemLoader
from app.logs.logs import logger
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import httpx
import boto3
import uuid
import datetime

from dotenv import load_dotenv
load_dotenv()
import os

# AWS Configuration
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_DEFAULT_REGION = os.getenv("AWS_DEFAULT_REGION")
AWS_BUCKET_NAME = os.getenv("AWS_BUCKET_NAME")
AWS_S3_URL = os.getenv("AWS_S3_URL")

# Email Configuration - Gmail SMTP
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USERNAME = os.getenv("SMTP_USERNAME", "wsgestor@gmail.com")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")  # App Password de Gmail
SMTP_FROM_EMAIL = os.getenv("SMTP_FROM_EMAIL", "wsgestor@gmail.com")
SMTP_FROM_NAME = os.getenv("SMTP_FROM_NAME", "Genefix by Yusef Gonzalez")

# Mailtrap Configuration (para testing)
MAILTRAP_API_TOKEN = os.getenv("MAILTRAP_API_TOKEN")
MAILTRAP_SANDBOX_ID = os.getenv("MAILTRAP_SANDBOX_ID")
USE_MAILTRAP = os.getenv("USE_MAILTRAP", "false").lower() == "true"

version = os.getenv("API_VERSION")
router = APIRouter(prefix=f"/api/{version}")

s3_client = boto3.client(
    "s3",
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_DEFAULT_REGION
)

# Configuración de Jinja2
TEMPLATE_PATH = "templates"
env = Environment(loader=FileSystemLoader(TEMPLATE_PATH))


def enviar_email_gmail(
    destinatario: str,
    asunto: str,
    html_body: str,
    attachments: List[str] = None
) -> dict:
    """
    Envía un email usando Gmail SMTP

    Args:
        destinatario: Email del destinatario
        asunto: Asunto del email
        html_body: Cuerpo del email en HTML
        attachments: Lista de rutas de archivos para adjuntar (opcional)

    Returns:
        dict: Resultado del envío

    Raises:
        Exception: Si hay algún error al enviar el email
    """
    try:
        # Validar configuración
        if not SMTP_PASSWORD:
            logger.error("SMTP_PASSWORD no está configurado. Configure una App Password de Gmail.")
            raise ValueError(
                "Email no configurado. Por favor configure SMTP_PASSWORD en las variables de entorno."
            )

        # Crear mensaje
        msg = MIMEMultipart('alternative')
        msg['From'] = f"{SMTP_FROM_NAME} <{SMTP_FROM_EMAIL}>"
        msg['To'] = destinatario
        msg['Subject'] = asunto

        # Adjuntar cuerpo HTML
        html_part = MIMEText(html_body, 'html', 'utf-8')
        msg.attach(html_part)

        # Adjuntar archivos si existen
        if attachments:
            for file_path in attachments:
                try:
                    with open(file_path, 'rb') as attachment_file:
                        part = MIMEBase('application', 'octet-stream')
                        part.set_payload(attachment_file.read())
                        encoders.encode_base64(part)
                        part.add_header(
                            'Content-Disposition',
                            f'attachment; filename= {os.path.basename(file_path)}'
                        )
                        msg.attach(part)
                except Exception as e:
                    logger.warning(f"No se pudo adjuntar el archivo {file_path}: {e}")

        # Conectar y enviar
        logger.info(f"Conectando a {SMTP_SERVER}:{SMTP_PORT}...")

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.set_debuglevel(0)  # Cambiar a 1 para debug
            server.starttls()  # Habilitar seguridad TLS

            logger.info(f"Autenticando con {SMTP_USERNAME}...")
            server.login(SMTP_USERNAME, SMTP_PASSWORD)

            logger.info(f"Enviando email a {destinatario}...")
            server.send_message(msg)

        logger.info(f"Email enviado exitosamente a {destinatario}")

        return {
            "success": True,
            "message": f"Correo enviado exitosamente a {destinatario}",
            "destinatario": destinatario
        }

    except smtplib.SMTPAuthenticationError as e:
        logger.error(f"Error de autenticación SMTP: {e}")
        raise Exception(
            "Error de autenticación. Verifique que:\n"
            "1. Ha habilitado la verificación en 2 pasos en su cuenta de Gmail\n"
            "2. Ha generado una 'App Password' en https://myaccount.google.com/apppasswords\n"
            "3. Está usando la App Password (no su contraseña normal)"
        )

    except smtplib.SMTPException as e:
        logger.error(f"Error SMTP: {e}")
        raise Exception(f"Error al enviar email: {str(e)}")

    except Exception as e:
        logger.error(f"Error inesperado al enviar email: {e}")
        raise Exception(f"Error inesperado: {str(e)}")


async def enviar_email_mailtrap(
    destinatario: str,
    asunto: str,
    html_body: str
) -> dict:
    """
    Envía un email usando Mailtrap (para testing)
    """
    try:
        if not MAILTRAP_API_TOKEN:
            raise ValueError("MAILTRAP_API_TOKEN no está configurado")

        MAILTRAP_API_URL = f"https://sandbox.api.mailtrap.io/api/send/{MAILTRAP_SANDBOX_ID}"

        headers = {
            "Authorization": f"Bearer {MAILTRAP_API_TOKEN}",
            "Content-Type": "application/json",
        }

        payload = {
            "from": {"email": SMTP_FROM_EMAIL, "name": SMTP_FROM_NAME},
            "to": [{"email": destinatario}],
            "subject": asunto,
            "html": html_body,
            "category": "GENEFIX EMAIL",
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(MAILTRAP_API_URL, headers=headers, json=payload)
            response.raise_for_status()

            return {
                "success": True,
                "message": f"Correo de prueba enviado a Mailtrap para {destinatario}",
                "destinatario": destinatario
            }

    except Exception as e:
        logger.error(f"Error al enviar email con Mailtrap: {e}")
        raise Exception(f"Error con Mailtrap: {str(e)}")


async def enviar_correo_con_plantilla(
    destinatario: str = Form(...),
    asunto: str = Form(...),
    nombre_usuario: str = Form(...),
    mensaje: str = Form(...),
    urlpdf: str = Form(None),
):
    """
    Envía un correo electrónico usando una plantilla HTML

    Args:
        destinatario: Email del destinatario
        asunto: Asunto del correo
        nombre_usuario: Nombre del usuario para personalizar el correo
        mensaje: Mensaje del correo
        urlpdf: URL del PDF adjunto (opcional)

    Returns:
        JSONResponse con el resultado del envío
    """
    try:
        # Renderizar plantilla
        template = env.get_template("email_template.html")
        html_cuerpo = template.render(
            asunto=asunto,
            nombre_usuario=nombre_usuario,
            mensaje=mensaje,
            pdf=urlpdf
        )

        # Decidir qué método usar (Gmail o Mailtrap)
        if USE_MAILTRAP:
            logger.info("Usando Mailtrap para enviar email (modo testing)")
            result = await enviar_email_mailtrap(destinatario, asunto, html_cuerpo)
        else:
            logger.info("Usando Gmail SMTP para enviar email (modo producción)")
            result = enviar_email_gmail(destinatario, asunto, html_cuerpo)

        return JSONResponse(result, status_code=200)

    except ValueError as e:
        logger.error(f"Error de configuración: {e}")
        return JSONResponse(
            {"error": f"Error de configuración: {str(e)}"},
            status_code=500
        )

    except Exception as e:
        logger.error(f"Error al enviar correo: {e}")
        return JSONResponse(
            {"error": f"Error al enviar el correo: {str(e)}"},
            status_code=500
        )


def enviar_email_simple(
    destinatario: str,
    asunto: str,
    mensaje: str,
    es_html: bool = False
) -> dict:
    """
    Envía un email simple sin plantilla

    Args:
        destinatario: Email del destinatario
        asunto: Asunto del email
        mensaje: Contenido del email
        es_html: Si el mensaje es HTML (True) o texto plano (False)

    Returns:
        dict: Resultado del envío
    """
    if es_html:
        html_body = mensaje
    else:
        # Convertir texto plano a HTML básico
        html_body = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
        </head>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                <p>{mensaje.replace(chr(10), '<br>')}</p>
                <hr style="border: none; border-top: 1px solid #ddd; margin: 20px 0;">
                <p style="font-size: 12px; color: #666;">
                    Este es un correo automático de GeneFIX. Por favor no responder.
                </p>
            </div>
        </body>
        </html>
        """

    return enviar_email_gmail(destinatario, asunto, html_body)
