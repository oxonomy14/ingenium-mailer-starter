import os
import sys
import shutil
from pathlib import Path
from dotenv import load_dotenv, set_key

from version import __version__

APP_NAME = "InGenium Mailer"
APP_VERSION = __version__

if getattr(sys, "frozen", False):
    RESOURCE_ROOT = Path(sys._MEIPASS)
    APP_SUPPORT_DIR = Path.home() / "Library" / "Application Support" / APP_NAME
else:
    RESOURCE_ROOT = Path(__file__).resolve().parent.parent
    APP_SUPPORT_DIR = RESOURCE_ROOT / "data"

APP_SUPPORT_DIR.mkdir(parents=True, exist_ok=True)

ENV_PATH = APP_SUPPORT_DIR / ".env"
ENV_EXAMPLE_PATH = RESOURCE_ROOT / ".env.example"

# Create starter settings on first launch; never overwrite existing user settings.
if not ENV_PATH.exists() and ENV_EXAMPLE_PATH.exists():
    shutil.copy2(ENV_EXAMPLE_PATH, ENV_PATH)

DB_PATH = APP_SUPPORT_DIR / "mail_history.db"
PREVIEW_PATH = APP_SUPPORT_DIR / "email_preview.html"
TEMPLATE_PATH = RESOURCE_ROOT / "templates" / "training_activated.html"


def load_settings():
    """Load settings from the user's .env file and refresh module values."""
    global SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASSWORD
    global FROM_NAME, FROM_EMAIL, DEFAULT_COURSE_URL, DEFAULT_REVIEWS_URL

    load_dotenv(ENV_PATH, override=True)

    SMTP_HOST = os.getenv("SMTP_HOST") or "smtppro.zoho.com"
    try:
        SMTP_PORT = int(os.getenv("SMTP_PORT") or "465")
    except ValueError:
        SMTP_PORT = 465

    SMTP_USER = os.getenv("SMTP_USER") or ""
    SMTP_PASSWORD = os.getenv("SMTP_PASSWORD") or ""
    FROM_NAME = os.getenv("FROM_NAME") or "InGenium Life"
    FROM_EMAIL = os.getenv("FROM_EMAIL") or SMTP_USER
    DEFAULT_COURSE_URL = os.getenv("DEFAULT_COURSE_URL") or "https://ingenium-life.info"
    DEFAULT_REVIEWS_URL = os.getenv("DEFAULT_REVIEWS_URL") or "https://ingenium-life.com/reviews"

    return {
        "smtp_host": SMTP_HOST,
        "smtp_port": SMTP_PORT,
        "smtp_user": SMTP_USER,
        "smtp_password": SMTP_PASSWORD,
        "from_name": FROM_NAME,
        "from_email": FROM_EMAIL,
        "course_url": DEFAULT_COURSE_URL,
        "reviews_url": DEFAULT_REVIEWS_URL,
    }


def save_settings(settings):
    """Persist settings to .env and reload them for the current process."""
    ENV_PATH.parent.mkdir(parents=True, exist_ok=True)
    if not ENV_PATH.exists():
        ENV_PATH.touch()

    values = {
        "SMTP_HOST": settings["smtp_host"].strip(),
        "SMTP_PORT": str(settings["smtp_port"]).strip(),
        "SMTP_USER": settings["smtp_user"].strip(),
        "SMTP_PASSWORD": settings["smtp_password"],
        "FROM_NAME": settings["from_name"].strip(),
        "FROM_EMAIL": settings["from_email"].strip(),
        "DEFAULT_COURSE_URL": settings["course_url"].strip(),
        "DEFAULT_REVIEWS_URL": settings["reviews_url"].strip(),
    }

    for key, value in values.items():
        set_key(str(ENV_PATH), key, value, quote_mode="always")

    try:
        ENV_PATH.chmod(0o600)
    except OSError:
        pass

    load_settings()
    return ENV_PATH


load_settings()
