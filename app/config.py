import os
import sys
from pathlib import Path
from dotenv import load_dotenv

from version import __version__

APP_NAME = "InGenium Mailer"
APP_VERSION = __version__

# PyInstaller stores bundled read-only resources in _MEIPASS.
if getattr(sys, "frozen", False):
    RESOURCE_ROOT = Path(sys._MEIPASS)
    APP_SUPPORT_DIR = Path.home() / "Library" / "Application Support" / APP_NAME
    APP_SUPPORT_DIR.mkdir(parents=True, exist_ok=True)
    ENV_PATH = APP_SUPPORT_DIR / ".env"
else:
    RESOURCE_ROOT = Path(__file__).resolve().parent.parent
    APP_SUPPORT_DIR = RESOURCE_ROOT / "data"
    APP_SUPPORT_DIR.mkdir(parents=True, exist_ok=True)
    ENV_PATH = RESOURCE_ROOT / ".env"

load_dotenv(ENV_PATH)

SMTP_HOST = os.getenv("SMTP_HOST", "smtppro.zoho.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "465"))
SMTP_USER = os.getenv("SMTP_USER", "")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")
FROM_NAME = os.getenv("FROM_NAME", "InGenium Life")
FROM_EMAIL = os.getenv("FROM_EMAIL", SMTP_USER)
DEFAULT_COURSE_URL = os.getenv("DEFAULT_COURSE_URL", "https://ingenium-life.com")
DEFAULT_REVIEWS_URL = os.getenv("DEFAULT_REVIEWS_URL", "https://ingenium-life.com/reviews")

DB_PATH = APP_SUPPORT_DIR / "mail_history.db"
PREVIEW_PATH = APP_SUPPORT_DIR / "email_preview.html"
TEMPLATE_PATH = RESOURCE_ROOT / "templates" / "training_activated.html"
