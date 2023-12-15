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
    s3_bucket_name = 'libramanage'
    folder_name = "pdfs"
    #Si el nombre tiene un espacio en la mitad se reemplaza por +
    file_name = file.filename.replace(" ", "+")
    path = f'{folder_name}/{file_name}'
    s3.Bucket(s3_bucket_name).put_object(Key= path, Body=file.file)
    
    #obtener el url del archivo
    url = f'https://{s3_bucket_name}.s3.amazonaws.com/{path}'
    return url

