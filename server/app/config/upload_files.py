import tempfile
import os
import uuid
from datetime import datetime
from fastapi import UploadFile, HTTPException
from app.config.mail import AWS_BUCKET_NAME, AWS_S3_URL, s3_client
from app.logs.logs import logger

async def upload_file_helper(file: UploadFile):
    try:
        # Crear un archivo temporal
        suffix = "." + (file.filename.split(".")[-1] if "." in file.filename else "")
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            contents = await file.read()
            tmp.write(contents)
            tmp_path = tmp.name

        # Leer el archivo temporal para subirlo a S3
        with open(tmp_path, "rb") as f:
            file_extension = file.filename.split(".")[-1] if "." in file.filename else ""
            unique_id = str(uuid.uuid4())
            file_key = f"{unique_id}_{datetime.now().day}{datetime.now().month}.{file_extension}"
            s3_client.put_object(Bucket=AWS_BUCKET_NAME, Key=file_key, Body=f)
            logger.info("Archivo subido correctamente", extra={"ms": "upload_file_helper", "file_key": file_key})

        # Eliminar archivo temporal
        # os.remove(tmp_path)

        public_url = f"{AWS_S3_URL}/{AWS_BUCKET_NAME}/{file_key}"
        return public_url

    except Exception as e:
        logger.error(
            "/activarCausacion: Error al subir el archivo",
            extra={"ms": "HTTP_401_UNAUTHORIZED", "detail": f"Error al subir el archivo: {str(e)}"},
        )
        raise HTTPException(status_code=500, detail=f"Error al subir el archivo: {str(e)}")