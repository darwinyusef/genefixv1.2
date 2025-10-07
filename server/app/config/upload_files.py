import uuid
from datetime import datetime
from fastapi import UploadFile, HTTPException
from app.config.mail import AWS_BUCKET_NAME, AWS_S3_URL, s3_client
from app.logs.logs import logger

async def upload_file_helper(file: UploadFile):
    try:
        # Leer el contenido del archivo (en bytes)
        contents = await file.read()

        # Generar un nombre único
        file_extension = file.filename.split(".")[-1] if "." in file.filename else ""
        unique_id = str(uuid.uuid4())
        file_key = f"{unique_id}_{datetime.now().day}{datetime.now().month}.{file_extension}"

        # Subir directamente los bytes a S3
        s3_client.put_object(Bucket=AWS_BUCKET_NAME, Key=file_key, Body=contents)

        logger.info("Archivo subido correctamente", extra={"ms": "upload_file_helper", "file_key": file_key})

        public_url = f"{AWS_S3_URL}/{AWS_BUCKET_NAME}/{file_key}"
        return public_url

    except Exception as e:
        logger.error(
            "/activarCausacion: Error al subir el archivo",
            extra={"ms": "HTTP_401_UNAUTHORIZED", "detail": f"Error al subir el archivo: {str(e)}"},
        )
        raise HTTPException(status_code=500, detail=f"Error al subir el archivo: {str(e)}")
