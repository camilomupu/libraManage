#Toca importar la base y hacer consultas acá
import os
from openai import OpenAI
from dotenv import load_dotenv
from config.db import get_db
from fastapi import Depends
from sqlalchemy.orm import Session
from models.tables import Prestamo
from fastapi import APIRouter

load_dotenv(".env")
#db = next(get_db())
router = APIRouter()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

#Información del proyecto
informacion_empresa_proyecto = {
    "nombre_empresa": "LibraTech Solutions",
    "descripcion_empresa": (
        "LibraTech Solutions es una empresa dedicada al desarrollo de soluciones tecnológicas para bibliotecas, "
        "centradas en la gestión eficiente de recursos físicos y digitales, reservas, préstamos y análisis de datos."
    ),
    "descripcion_proyecto": (
        "Desarrollar un sistema integral de gestión de libros denominado 'LibraManage', que proporciona un portal unificado "
        "para acceder a libros digitales, gestionar reservas y préstamos de libros físicos, y ofrece a los administradores "
        "herramientas eficientes para la gestión de inventario y análisis de datos de uso y préstamos."
    ),
    "requisitos_funcionales": (
        "Los usuarios podrán registrarse proporcionando información personal como nombre, dirección de correo electrónico y contraseña. "
        "Existirán diferentes roles de usuario (administradores, bibliotecarios y usuarios generales) con diferentes niveles de acceso y privilegios. "
        "El sistema permitirá a los administradores registrar libros físicos y digitales en la biblioteca, realizar búsquedas de libros, "
        "realizar reservas, gestionar préstamos, mostrar información detallada de los libros y mostrar estadísticas."
    ),
    "requisitos_no_funcionales": (
        "El sistema será fácil de usar y navegar, intuitivo y fácil de aprender. Será capaz de manejar un gran número de usuarios y libros sin comprometer su rendimiento. "
        "Será seguro y protegerá la información personal de los usuarios, con medidas de seguridad contra el acceso no autorizado. "
        "Será fácil de mantener y actualizar, con una arquitectura modular que permita agregar nuevas funcionalidades. "
        "Estará disponible en todo momento para los usuarios, con medidas de contingencia en caso de fallas del sistema."
    ),
    "casos_de_uso": [
        "Registro de usuarios. (Actores: Administrador, Usuario, Bibliotecario)",
        "Login. (Actores: Administrador, Usuario, Bibliotecario y sistema)",
        "Ver disponibilidad de libros. (Actores: Sistema, Usuario, Bibliotecario)",
        "Buscar libros (Actores: Administrador, Usuario y Bibliotecario)",
        "Reserva de libro físico (Actores: Usuario, Bibliotecario)",
        "Comprar libro digital (Actores: Usuario)",
        "Consultar Multas y Plazos: (Actores: Usuario)",
        "Agregar Libro a la plataforma: (Actores: Administrador, Bibliotecario)",
        "Gestionar Multas (Actores: Administrador y Bibliotecario)",
        "Generar informe de análisis de datos (Actores: Administrador)"
    ],
}
    
#Consultas
#cuantos libros se van a vender, cuantos libros se van a prestar y cuantos libros no se van a entregar   

#No se implementa por falta de fechas de ventas
def obtener_estimadoVentas(db):
    libros = 0
    return libros

#Se va a utilizar para pasarle las fechas de los prestamos al chatgpt y que las interprete obteniendo el numero de libros que se van a prestar
def obtener_fechasPrestamos(db):
    """
    Obtiene las fechas de préstamo de la base de datos.
    Args:
        db: Sesión de la base de datos.
    Returns:
        List[str]: Lista de fechas de préstamo en formato de cadena.
    """
    # Consulta para obtener las fechas de préstamo desde la tabla de préstamos
    fechas_prestamo = db.query(Prestamo.fechaPrestamo).all()

    # Convertir el resultado a una lista de fechas en formato de cadena
    lista_fechas_prestamo = [str(fecha[0]) for fecha in fechas_prestamo]

    return lista_fechas_prestamo

#se va a utilizar para pasar las fechas y estado del prestamo al chatgpt y que las interprete obteniendo el numero de libros que no se van a entregar
def obtener_estadoPrestamos(db):
    """
    Obtiene la información de las fechas de vencimiento y el estado de los préstamos.
    Args:
        db: Sesión de la base de datos.
    Returns:
        List[Dict[str, Union[str, bool]]]: Lista de diccionarios con información de los préstamos.
    """
    # Consulta para obtener la información de préstamos desde la tabla de préstamos
    prestamos_info = db.query(Prestamo.fechaVencimiento, Prestamo.devuelto).all()

    # Convertir el resultado a un diccionario
    info_diccionario = [{"fecha_vencimiento": str(prestamo.fechaVencimiento), "devuelto": prestamo.devuelto} for prestamo in prestamos_info]

    return info_diccionario
    #
#Pregunta respuesta
@router.get("/consultaChatGPT/{pregunta}")
def pregunta_chatGPT(pregunta: str, db: Session = Depends(get_db)):
    """
    Interactúa con el modelo de lenguaje GPT-3.5 Turbo de OpenAI para obtener respuestas a preguntas específicas de la app.
    Args:
        pregunta (str): Pregunta del usuario.
        db: Sesión de la base de datos.
    Returns:
        Dict[str, str]: Respuesta del modelo de lenguaje.
    """
    #Obtenemos las fechas de los prestamos
    fechas_prestamo = obtener_fechasPrestamos(db)
    #Obtenemos las fechas y el estado de los prestamos
    info_prestamos = obtener_estadoPrestamos(db)
    #Contexto del asistente
    messages = [
        {
            "role": "system",
            "content": f"Cuando el usuario te pida el número de libros que se van a prestar, interpreta estos datos {fechas_prestamo} y da un estimado de libros que se van a prestar en el mes siguiente."
                        f"También, da un estimado de los libros que no se van a devolver en el siguiente mes utilizando estos datos {info_prestamos} y la información de los préstamos."
                        f"Vas a ser un chat de una sola respuesta por eso no importa que no cuentes con los datos suficientes; interpreta las fechas y el estado de los préstamos y da un estimado de las consultas en primera instancia."
                        f"Información de la empresa y el proyecto: {informacion_empresa_proyecto}. Intenta ser un sistema solo de ayuda para Libra Manaage"
        }
    ]
    
    # Aquí, convertimos la pregunta a minuscúlas para que sea más fácil de interpretar
    pregunta = pregunta.lower()
    #Agregamos la pregunta del usuario
    messages.append({"role": "user", "content": pregunta})
    
    #Hacemos la solicitud al chat
    response = client.chat.completions.create(
        model="gpt-3.5-turbo", messages=messages)
    
    response_content = response.choices[0].message.content
    return {"respuesta": response_content}
