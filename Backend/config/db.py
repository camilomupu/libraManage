import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os
import boto3
from dotenv import load_dotenv
from fastapi import FastAPI, UploadFile, File, Request


load_dotenv('.env')

db_host = os.getenv('DB_HOST')
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')
db_name = os.getenv('DB_NAME')
db_port = os.getenv('DB_PORT')

DB_URL = f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'
#DB_URL = f'mysql+mysqlconnector://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'
Base = declarative_base()
engine = create_engine(DB_URL, echo=True, future=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        

# Credenciales de AWS
s3 = boto3.resource(
    service_name='s3',
    region_name=os.getenv('AWS_DEFAULT_REGION'),
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
)


async def upload_img(file: UploadFile = File(...)):
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
    s3_bucket_name = 'libramanage'
    folder_name = "pdfs"
    #Si el nombre tiene un espacio en la mitad se reemplaza por +
    file_name = file.filename.replace(" ", "+")
    path = f'{folder_name}/{file_name}'
    s3.Bucket(s3_bucket_name).put_object(Key= path, Body=file.file)
    #obtener el url del archivo
    url = f'https://{s3_bucket_name}.s3.amazonaws.com/{path}'

    return url



