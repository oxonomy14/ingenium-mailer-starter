import smtplib
from email.message import EmailMessage
from email.utils import formataddr
from app import config


def test_smtp_connection(settings):
    """Verify SMTP SSL connection and authentication without sending an email."""
    host = settings["smtp_host"].strip()
    port = int(settings["smtp_port"])
    username = settings["smtp_user"].strip()
    password = settings["smtp_password"]

    if not username or not password:
        raise RuntimeError("Укажите SMTP_USER и SMTP_PASSWORD.")

    with smtplib.SMTP_SSL(host, port, timeout=20) as server:
        server.ehlo()
        server.login(username, password)


def send_html_email(to_name: str, to_email: str, subject: str, html: str):
    # Read refreshed settings each time, so changes made in Settings take effect immediately.
    config.load_settings()

    if not config.SMTP_USER or not config.SMTP_PASSWORD:
        raise RuntimeError("Не настроены SMTP_USER и SMTP_PASSWORD. Откройте Настройки SMTP.")

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
