import smtplib
from email.message import EmailMessage
from email.utils import formataddr
from app import config

def send_html_email(to_name: str, to_email: str, subject: str, html: str):
    if not config.SMTP_USER or not config.SMTP_PASSWORD:
        raise RuntimeError("Не настроены SMTP_USER и SMTP_PASSWORD в файле .env.")

    message = EmailMessage()
    message["Subject"] = subject
    message["From"] = formataddr((config.FROM_NAME, config.FROM_EMAIL))
    message["To"] = formataddr((to_name, to_email))
    message.set_content(
        f"{to_name}, доступ к обучению активирован. "
        "Откройте письмо в HTML-формате или перейдите на сайт InGenium Life."
    )
    message.add_alternative(html, subtype="html")

    with smtplib.SMTP_SSL(config.SMTP_HOST, config.SMTP_PORT, timeout=30) as server:
        server.login(config.SMTP_USER, config.SMTP_PASSWORD)
        server.send_message(message)
