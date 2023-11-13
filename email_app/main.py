from .send_email import send_email

to = "enter the email address here"
subject = "enter the message subject here"
content = "enter the message content to send here"


if __name__ == "__main__":
    send_email(to=to, subject=subject, content=content)
