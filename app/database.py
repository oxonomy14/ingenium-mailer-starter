import sqlite3
from datetime import datetime, timezone
from app.config import DB_PATH

def initialize_database():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS email_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                created_at TEXT NOT NULL,
                recipient_name TEXT NOT NULL,
                recipient_email TEXT NOT NULL,
                subject TEXT NOT NULL,
                training_title TEXT NOT NULL,
                status TEXT NOT NULL,
                error TEXT
            )
        """)

def log_email(name, email, subject, title, status, error=None):
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            INSERT INTO email_log
            (created_at, recipient_name, recipient_email, subject, training_title, status, error)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            datetime.now(timezone.utc).isoformat(),
            name, email, subject, title, status, error
        ))


def get_recent_logs(limit=20):
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        rows = conn.execute("""
            SELECT created_at, recipient_name, recipient_email,
                   subject, training_title, status, error
            FROM email_log
            ORDER BY id DESC
            LIMIT ?
        """, (limit,)).fetchall()
        return [dict(row) for row in rows]
