import re

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

def validate_form(name: str, email: str, title: str, course_url: str, reviews_url: str):
    if not name.strip():
        return "Введите имя клиента."
    if not EMAIL_RE.match(email.strip()):
        return "Проверьте адрес электронной почты."
    if not title.strip():
        return "Введите название тренинга."
    if not course_url.strip().startswith(("https://", "http://")):
        return "Ссылка на обучение должна начинаться с http:// или https://."
    if not reviews_url.strip().startswith(("https://", "http://")):
        return "Ссылка на отзывы должна начинаться с http:// или https://."
    return None
