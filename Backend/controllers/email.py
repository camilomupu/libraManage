import os
import locale
from dotenv import load_dotenv
from fastapi_mail import FastMail, ConnectionConfig, MessageSchema
from fastapi import Request, HTTPException
from schemas.user import User
from schemas.digitalBook import DigitalBookCreate
from schemas.physicalBook import PhysicalBook
from schemas.loan import loanDueDate
from starlette.responses import JSONResponse


# Establecer la configuración regional a español
locale.setlocale(locale.LC_TIME, "es_ES")

load_dotenv(".env")

smtp_password = os.getenv("SMTP_PASSWORD")
smpt_from = os.getenv("SMTP_FROM")

conf = ConnectionConfig(
    MAIL_USERNAME=smpt_from,
    MAIL_PASSWORD=smtp_password,
    MAIL_FROM=smpt_from,
    MAIL_PORT=587,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_FROM_NAME="Libra Manage",
    MAIL_STARTTLS=True,  # Puedes ajustar según tus necesidades
    MAIL_SSL_TLS=False,  # Puedes ajustar según tus necesidades
)


async def sendEmailSaleConfirmation(
    email: str, book: DigitalBookCreate, instance: User
):
    template = f"""
        <!DOCTYPE html>
        <html>
            <head>
                <meta charset="utf-8">
                <title>Correo de confirmación y agradecimiento por tu compra</title>
                <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css">
                <style>
                    body {{
                        font-family: 'Caslon';
                        background-color: #fff;
                        margin: 0;
                        padding: 0;
                    }}
                    .container {{
                        max-width: 600px;
                        margin: 20px auto;
                        background-color: #EFEFEF;
                        padding-bottom: 20px;
                        border-radius: 8px;
                        box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                    }}
                    .container h2 {{
                        color: #FFF;
                        margin: 0px -40px;
                        border-radius: 8px 8px 0 0;
                        background-color:#DECDAC;
                        padding: 15px;
                        text-align: center;
                    }}
                    .container p {{
                        color: #555;
                        line-height: 1.6;
                    }}
                    .btn {{
                        display: inline-block;
                        padding: 10px 20px;
                        text-aling: center;
                        background-color: #007bff;
                        color: #fff;
                        text-decoration: none;
                        border-radius: 5px;
                    }}
                    .btn:hover {{
                        background-color: #0056b3;
                    }}
                    .footer {{
                        margin-top: 20px;
                        text-align: center;
                        color: #777;
                    }}
                    .conten {{
                        margin: 0px 20px;
                    }}
                </style>
            </head>
            <body>
                <div class="container">
                    <h2>Agradecimiento por tu Compra</h2>
                    <div class = "conten">
                        <p>Estimado {instance.nombre},</p>
                        <p>Gracias por tu compra en nuestra plataforma. Tu compra del libro digital "<strong>{book.titulo}</strong>" ha sido confirmada, 
                        con un valor de $<strong>{book.precio}</strong> pesos.</p>
                        <p>Para descargar tu libro digital, haz clic en el siguiente enlace:</p>
                        <a href="[Enlace de Descarga]" class="btn">Descargar libro</a>
                        <p>Esperamos que disfrutes de tu lectura.</p>
                    <p>Si tienes alguna pregunta o necesitas ayuda, no dudes en contactarnos.</p>
                </div>
                </div>
                <div class="footer">
                    <p>© 2023 Fentalabs | Todos los derechos reservados</p>
                </div>
            </body>
        </html>
"""

    message = MessageSchema(
        subject="Confirmación de compra",
        recipients=[email],
        body=template,
        subtype="html",
    )

    print(conf)
    print(message)

    fm = FastMail(conf)
    try:
        await fm.send_message(message=message)
        return JSONResponse(status_code=200, content={"message": "email has been sent"})
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error al enviar el correo electrónico: {str(e)}"
        )


async def sendEmaiLoanConfirmation(
    email: str, book: PhysicalBook, loan: loanDueDate, instance: User
):
    text_loan_date = loan.fechaPrestamo.strftime("%A, %d de %B de %Y")
    text_loan_date_end = loan.fechaVemcimiento.strftime("%A, %d de %B de %Y")

    template = f"""
         <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>Confirmación y Agradecimiento por tu Préstamo</title>
            <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css">
            <style>
                body {{
                    font-family: 'Caslon';
                    background-color: #fff;
                    margin: 0;
                    padding: 0;
                }}
                .container {{
                    max-width: 600px;
                    margin: 20px auto;
                    background-color: #EFEFEF;
                    padding-bottom: 20px;
                    border-radius: 8px;
                    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                }}
                .container h2 {{
                    color: #FFF;
                    margin: 0px -40px;
                    border-radius: 8px 8px 0 0;
                    background-color: #DECDAC;
                    padding: 15px;
                    text-align: center;
                }}
                .container p {{
                    color: #555;
                    line-height: 1.6;
                }}
                .container strong {{
                    color: #555;
                    line-height: 1.6;
                }}
                .btn {{
                    display: inline-block;
                    padding: 10px 20px;
                    text-align: center;
                    background-color: #007bff;
                    color: #fff;
                    text-decoration: none;
                    border-radius: 5px;
                }}
                .btn:hover {{
                    background-color: #0056b3;
                }}
                .footer {{
                    margin-top: 20px;
                    text-align: center;
                    color: #777;
                }}
                .conten {{
                    margin: 0px 20px;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <h2>Agradecimiento por tu Préstamo</h2>
                <div class="conten">
                    <p>Estimado {instance.nombre},</p>
                    <p>Gracias por realizar el préstamo del libro "<strong>{book.titulo}</strong>" en nuestra biblioteca. 
                    Tu préstamo ha sido registrado con éxito.</p>
                    <p>Detalles del Préstamo:</p>
                    <ul>
                        <strong>
                        <li>Fecha de Préstamo: {text_loan_date}.</li>
                        <li>Fecha de Devolución: {text_loan_date_end}.</li>
                        </strong>
                    </ul>
                    <p>Para más detalles sobre el préstamo y las condiciones, por favor revisa tu cuenta en nuestra plataforma.</p>
                    <p>Esperamos que disfrutes de la lectura y que el libro te sea de gran provecho.</p>
                    <p>Si tienes alguna pregunta o necesitas ayuda, no dudes en contactarnos.</p>
                </div>
            </div>
            <div class="footer">
                <p>© 2023 Biblioteca Virtual | Todos los derechos reservados</p>
            </div>
        </body>
        </html>
"""

    message = MessageSchema(
        subject="Confirmación de prestamo",
        recipients=[email],
        body=template,
        subtype="html",
    )

    print(conf)
    print(message)

    fm = FastMail(conf)
    try:
        await fm.send_message(message=message)
        return JSONResponse(status_code=200, content={"message": "email has been sent"})
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error al enviar el correo electrónico: {str(e)}"
        )


# Función para enviar correo electrónico de bienvenida
async def send_welcome_email(email: str, username: str, request: Request):
    template = f"""
         <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>Te damos la bienvenida a Libra Manage gracias por registrarte en nuestra aplicación</title>
            <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css">
            <style>
                body {{
                    font-family: 'Caslon';
                    background-color: #fff;
                    margin: 0;
                    padding: 0;
                }}
                .container {{
                    max-width: 600px;
                    margin: 20px auto;
                    background-color: #EFEFEF;
                    padding-bottom: 20px;
                    border-radius: 8px;
                    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                }}
                .container h2 {{
                    color: #FFF;
                    margin: 0px -40px;
                    border-radius: 8px 8px 0 0;
                    background-color: #DECDAC;
                    padding: 15px;
                    text-align: center;
                }}
                .container p {{
                    color: #555;
                    line-height: 1.6;
                }}
                .container strong {{
                    color: #555;
                    line-height: 1.6;
                }}
                .btn {{
                    display: inline-block;
                    padding: 10px 20px;
                    text-align: center;
                    background-color: #007bff;
                    color: #fff;
                    text-decoration: none;
                    border-radius: 5px;
                }}
                .btn:hover {{
                    background-color: #0056b3;
                }}
                .footer {{
                    margin-top: 20px;
                    text-align: center;
                    color: #777;
                }}
                .conten {{
                    margin: 0px 20px;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <h2>Registro exitoso</h2>
                <div class="conten">
                    <p>¡Bienvenido a Libra Tech! Estamos emocionados de tenerte como parte de nuestra comunidad de amantes de la lectura. En Libra Manage, no solo encontrarás una plataforma para organizar tus libros, sino también un espacio dedicado a descubrir nuevas historias y conectar con otros apasionados por la lectura.</p>
                    <p>Tu viaje con nosotros acaba de comenzar, y estamos aquí para hacer que cada página cuente.</p>
                    <p>No dudes en ponerte en contacto con nosotros si tienes alguna pregunta o si hay algo en lo que podamos ayudarte. Estamos aquí para hacer que tu experiencia con Libra Manage sea excepcional.</p>      
                    <p>¡Disfruta explorando el mundo de los libros con Libra Manage!</p>
                </div>
            </div>
            <div class="footer">
                <p>© 2023 Biblioteca Virtual | Todos los derechos reservados</p>
            </div>
        </body>
        </html>
"""

    message = MessageSchema(
        subject=f"Hola {username}, Bienvenido a Libra Manage",
        recipients=[email],
        body=template,
        subtype="html",
    )
    # Enviar mensaje
    fm = FastMail(conf)
    try:
        await fm.send_message(message=message)
        return JSONResponse(status_code=200, content={"message": "email has been sent"})
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error al enviar el correo electrónico: {str(e)}"
        )
