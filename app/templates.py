from html import escape
from pathlib import Path
from app.config import TEMPLATE_PATH

def build_training_activated_email(name: str, title: str, course_url: str, reviews_url: str):
    template = Path(TEMPLATE_PATH).read_text(encoding="utf-8")
    values = {
        "name": escape(name.strip() or "дорогой друг"),
        "title": escape(title.strip()),
        "course_url": escape(course_url.strip(), quote=True),
        "reviews_url": escape(reviews_url.strip(), quote=True),
    }
    for key, value in values.items():
        template = template.replace("{{" + key + "}}", value)
    subject = f"Доступ открыт! Тренинг «{title.strip()}» — InGenium Life"
    return subject, template
