from typing import List
from fastapi import APIRouter
from fastapi import File, UploadFile, Form
from fastapi.responses import JSONResponse
from mailtrap import MailtrapClient
from jinja2 import Environment, FileSystemLoader
import httpx
import boto3
import uuid
import datetime 

from dotenv import load_dotenv
load_dotenv() 
import os

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_DEFAULT_REGION = os.getenv("AWS_DEFAULT_REGION")
AWS_BUCKET_NAME = os.getenv("AWS_BUCKET_NAME")
AWS_S3_URL = os.getenv("AWS_S3_URL")

MAILTRAP_API_TOKEN = os.getenv("MAILTRAP_API_TOKEN")
mailtrap_client = MailtrapClient(token=MAILTRAP_API_TOKEN)
MAILTRAP_SANDBOX_ID = os.getenv("MAILTRAP_SANDBOX_ID")
MAILTRAP_API_URL = f"https://sandbox.api.mailtrap.io/api/send/{MAILTRAP_SANDBOX_ID}"


version = os.getenv("API_VERSION")
router = APIRouter(prefix=f"/api/{version}")

s3_client = boto3.client(
    "s3",
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_DEFAULT_REGION
)

@router.post("/uploadfile/", tags=['Send'])
async def upload_file(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        file_extension = file.filename.split(".")[-1] if "." in file.filename else ""
        unique_id = str(uuid.uuid4())
        file_key = f"{unique_id}_{datetime.datetime.now().day}{datetime.datetime.now().month}.{file_extension}"
        s3_client.put_object(Bucket=AWS_BUCKET_NAME, Key=file_key, Body=contents)
        public_url = f"{AWS_S3_URL}/{AWS_BUCKET_NAME}/{file_key}"
        return JSONResponse(content={"filename": file.filename, "upload_code": unique_id, "url": public_url})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
    

# Configuración de Jinja2
TEMPLATE_PATH = "templates"
env = Environment(loader=FileSystemLoader(TEMPLATE_PATH))

@router.post("/mail", tags=['Send'])
async def enviar_correo_con_plantilla(
    destinatario: str = Form(...),
    asunto: str = Form(...),
    nombre_usuario: str = Form(...),
    mensaje: str = Form(...),
    urlpdf: str = Form(...),
):
    try:
        template = env.get_template("email_template.html")
        html_cuerpo = template.render(
            asunto=asunto, nombre_usuario=nombre_usuario, mensaje=mensaje, pdf=urlpdf
        )

        headers = {
            "Authorization": f"Bearer {MAILTRAP_API_TOKEN}",
            "Content-Type": "application/json",
        }
        payload = {
            "from": {"email": "wsgestor@gmail.com", "name": "Genefix by Yusef Gonzalez"},
            "to": [{"email": destinatario}],
            "subject": asunto,
            "html": html_cuerpo,
            "category": "GENEFIX EMAIL",
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(MAILTRAP_API_URL, headers=headers, json=payload)
            response.raise_for_status()

            return JSONResponse({"mensaje": f"Correo con plantilla enviado exitosamente a {destinatario}"}, status_code=200)

    except httpx.HTTPStatusError as e:
        return JSONResponse({"error": f"Error al enviar el correo: {e}"}, status_code=response.status_code)
    except Exception as e:
        return JSONResponse({"error": f"Ocurrió un error: {e}"}, status_code=500)




