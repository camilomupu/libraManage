import os
import boto3
from dotenv import load_dotenv
from fastapi import FastAPI, UploadFile, File, Request
from io import BytesIO
from typing import List, Optional

load_dotenv('.env')

# Credenciales de AWS
s3 = boto3.resource(
    service_name='s3',
    region_name=os.getenv('AWS_DEFAULT_REGION'),
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
)

async def upload_file(file: UploadFile = File(...)):
    """
    Sube un archivo al servicio de almacenamiento S3 y devuelve la URL del archivo.
    Args:
        file (UploadFile): Archivo a ser subido.
    Returns:
        str: URL del archivo almacenado en S3.
    """
    # Nombre del bucket en S3
    s3_bucket_name = 'libramanage'
    # Carpeta en la que se almacenarán los archivos
    folder_name = "pdfs"
    # Reemplaza los espacios en el nombre del archivo con '+'
    file_name = file.filename.replace(" ", "+")
    # Ruta completa del archivo en S3
    path = f'{folder_name}/{file_name}'
    # Sube el archivo al bucket de S3
    s3.Bucket(s3_bucket_name).put_object(Key= path, Body=file.file)
    
    #Obtiene la URL del archivo almacenado en S3
    url = f'https://{s3_bucket_name}.s3.amazonaws.com/{path}'
    return url

