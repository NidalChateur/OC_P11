import smtplib
from email.message import EmailMessage

from decouple import config

# Charger la configuration depuis les variables d'environnement
EMAIL = config("EMAIL")
PASSWORD = config("PASSWORD")
SMTP_SERVER = config("SMTP_SERVER")
SMTP_PORT = config("SMTP_PORT")


def create_message(to: str, subject: str, content: str) -> EmailMessage:
    message = EmailMessage()
    message["To"] = to
    message["From"] = EMAIL
    message["Subject"] = subject
    message.set_content(content)

    return message


def send_email(to: str, subject: str, content: str):
    message = create_message(to, subject, content)

    with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as smtp:
        try:
            smtp.login(EMAIL, PASSWORD)
            print("Connecté au service de messagerie avec succès !")
            smtp.send_message(message)
            print("Email envoyé !")
        except Exception as e:
            print(f"Une erreur s'est produite : {e}")
