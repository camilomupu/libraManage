import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os
import boto3
from dotenv import load_dotenv
from fastapi import FastAPI, UploadFile, File, Request

# Cargar variables de entorno desde el archivo .env
load_dotenv('.env')

# Obtener configuración de la base de datos desde las variables de entorno
db_host = os.getenv('DB_HOST')
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')
db_name = os.getenv('DB_NAME')
db_port = os.getenv('DB_PORT')

# Crear la URL de la base de datos
DB_URL = f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'
#DB_URL = f'mysql+mysqlconnector://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'

# Declarar la base para los modelos SQLAlchemy
Base = declarative_base()

# Crear el motor de la base de datos
engine = create_engine(DB_URL, echo=True, future=True)

# Crear una sesión de la base de datos utilizando el motor
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    """
    La función get_db() devuelve una sesión de base de datos y se asegura de que se cierre después de su uso.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        

# Configuración de credenciales de AWS
s3 = boto3.resource(
    service_name='s3',
    region_name=os.getenv('AWS_DEFAULT_REGION'),
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
)


async def upload_img(file: UploadFile = File(...)):
    """
    Sube una imagen al servicio de almacenamiento en la nube de AWS S3.
    Args:
        file (UploadFile): Archivo de imagen a subir.
    Returns:
        str: URL del archivo subido.
    """
    s3_bucket_name = 'libramanage'
    folder_name = "imagenes"
    #Si el nombre tiene un espacio en la mitad se reemplaza por +
    file_name = file.filename.replace(" ", "+")
    path = f'{folder_name}/{file_name}'
    s3.Bucket(s3_bucket_name).put_object(Key= path, Body=file.file)
    #obtener el url del archivo
    url = f'https://{s3_bucket_name}.s3.amazonaws.com/{path}'
    return url

async def upload_pdfs(file: UploadFile = File(...)):
    """
    Sube un archivo PDF al servicio de almacenamiento en la nube de AWS S3.
    Args:
        file (UploadFile): Archivo PDF a subir.
    Returns:
        str: URL del archivo subido.
    """
    s3_bucket_name = 'libramanage'
    folder_name = "pdfs"
    #Si el nombre tiene un espacio en la mitad se reemplaza por +
    file_name = file.filename.replace(" ", "+")
    path = f'{folder_name}/{file_name}'
    s3.Bucket(s3_bucket_name).put_object(Key= path, Body=file.file)
    #obtener el url del archivo
    url = f'https://{s3_bucket_name}.s3.amazonaws.com/{path}'

    return url
