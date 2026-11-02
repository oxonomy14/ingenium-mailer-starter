import tkinter as tk
from tkinter import ttk, messagebox
import webbrowser
from datetime import datetime

from app import config
from app.database import initialize_database, log_email, get_recent_logs
from app.mailer import send_html_email
from app.templates import build_training_activated_email
from app.validators import validate_form


class MailerApp:
    def __init__(self):
        initialize_database()
        self.root = tk.Tk()
        self.root.title(f"{config.APP_NAME} v{config.APP_VERSION}")
        self.root.geometry("800x760")
        self.root.minsize(700, 650)
        self._build_ui()
        self._load_report_history()

    def _build_ui(self):
        style = ttk.Style()
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        outer = ttk.Frame(self.root, padding=24)
        outer.pack(fill="both", expand=True)

        ttk.Label(outer, text=f"InGenium Mailer v{config.APP_VERSION}", font=("Helvetica", 22, "bold")).pack(anchor="w")
        ttk.Label(outer, text="Уведомление об активации тренинга", foreground="#64748b").pack(anchor="w", pady=(4, 18))

        form = ttk.Frame(outer)
        form.pack(fill="x")
        self.fields = {}
        entries = [
            ("Имя клиента", "name", ""),
            ("Email клиента", "email", ""),
            ("Название тренинга", "title", ""),
            ("Ссылка на обучение", "course_url", config.DEFAULT_COURSE_URL),
            ("Ссылка на отзывы", "reviews_url", config.DEFAULT_REVIEWS_URL),
        ]
        for row, (label, key, default) in enumerate(entries):
            ttk.Label(form, text=label).grid(row=row, column=0, sticky="w", padx=(0, 14), pady=7)
            variable = tk.StringVar(value=default)
            ttk.Entry(form, textvariable=variable).grid(row=row, column=1, sticky="ew", pady=7)
            self.fields[key] = variable
        form.columnconfigure(1, weight=1)

        ttk.Separator(outer).pack(fill="x", pady=16)
        ttk.Label(outer, text="Шаблон письма", font=("Helvetica", 12, "bold")).pack(anchor="w")
        ttk.Label(outer, text="Предпросмотр откроется в браузере.", foreground="#64748b").pack(anchor="w", pady=(5, 12))

        actions = ttk.Frame(outer)
        actions.pack(fill="x")
        ttk.Button(actions, text="Предпросмотр письма", command=self.preview).pack(side="left")
        ttk.Button(actions, text="Отправить письмо", command=self.send).pack(side="right")

        ttk.Separator(outer).pack(fill="x", pady=18)
        report_header = ttk.Frame(outer)
        report_header.pack(fill="x")
        ttk.Label(report_header, text="Отчёт об отправке", font=("Helvetica", 13, "bold")).pack(side="left")
        ttk.Button(report_header, text="Обновить", command=self._load_report_history).pack(side="right")
        ttk.Label(outer, text="Результаты отправки и последние записи из локальной истории:", foreground="#64748b").pack(anchor="w", pady=(4, 8))

        report_frame = ttk.Frame(outer)
        report_frame.pack(fill="both", expand=True)
        self.report = tk.Text(report_frame, height=12, wrap="word", font=("Menlo", 11), relief="solid", borderwidth=1, padx=10, pady=8, state="disabled")
        scrollbar = ttk.Scrollbar(report_frame, orient="vertical", command=self.report.yview)
        self.report.configure(yscrollcommand=scrollbar.set)
        self.report.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.status = tk.StringVar(value="Готово к работе")
        ttk.Label(outer, textvariable=self.status, foreground="#475569").pack(anchor="w", pady=(10, 0))

    def _load_report_history(self):
        self.report.configure(state="normal")
        self.report.delete("1.0", "end")
        self.report.insert("end", "ПОСЛЕДНИЕ ОТПРАВКИ\n" + "—" * 42 + "\n\n")
        try:
            rows = get_recent_logs(20)
        except Exception as exc:
            rows = []
            self.report.insert("end", f"Не удалось прочитать историю: {exc}\n")
        if not rows:
            self.report.insert("end", "История пока пуста. После первой отправки здесь появится отчёт.\n")
        for row in rows:
            try:
                dt = datetime.fromisoformat(row["created_at"]).astimezone().strftime("%d.%m.%Y %H:%M:%S")
            except Exception:
                dt = row["created_at"]
            label = "УСПЕШНО" if row["status"] == "sent" else "ОШИБКА"
            self.report.insert("end", f"[{label}] {dt}\nКому: {row['recipient_name']} <{row['recipient_email']}>\nТренинг: {row['training_title']}\nТема: {row['subject']}\n")
            if row["error"]:
                self.report.insert("end", f"Причина: {row['error']}\n")
            self.report.insert("end", "\n" + "—" * 42 + "\n\n")
        self.report.configure(state="disabled")

    def _get_data(self):
        return {key: variable.get().strip() for key, variable in self.fields.items()}

    def _build_message(self):
        data = self._get_data()
        error = validate_form(data["name"], data["email"], data["title"], data["course_url"], data["reviews_url"])
        if error:
            raise ValueError(error)
        subject, html = build_training_activated_email(data["name"], data["title"], data["course_url"], data["reviews_url"])
        return data, subject, html

    def preview(self):
        try:
            data, subject, html = self._build_message()
        except ValueError as exc:
            messagebox.showwarning("Проверьте данные", str(exc))
            return
        preview_path = config.PREVIEW_PATH
        preview_path.parent.mkdir(parents=True, exist_ok=True)
        preview_path.write_text(f"<!doctype html><html lang='ru'><head><meta charset='utf-8'><title>{subject}</title></head><body>{html}</body></html>", encoding="utf-8")
        webbrowser.open(preview_path.as_uri())
        self.status.set("Предпросмотр открыт в браузере")

    def send(self):
        try:
            data, subject, html = self._build_message()
        except ValueError as exc:
            messagebox.showwarning("Проверьте данные", str(exc))
            return
        if not messagebox.askyesno("Подтверждение отправки", f"Отправить письмо на адрес:\n{data['email']}\n\nТренинг: {data['title']}\n\nПродолжить?"):
            return

        self.status.set("Отправка письма...")
        self.root.update_idletasks()
        sent_at = datetime.now().astimezone().strftime("%d.%m.%Y %H:%M:%S")
        try:
            send_html_email(data["name"], data["email"], subject, html)
            log_email(data["name"], data["email"], subject, data["title"], "sent")
            self.status.set(f"Успешно отправлено: {data['email']}")
            messagebox.showinfo("Письмо отправлено", f"SMTP-сервер принял письмо к отправке.\n\nПолучатель: {data['email']}\nВремя: {sent_at}")
        except Exception as exc:
            error_text = str(exc)
            log_email(data["name"], data["email"], subject, data["title"], "error", error_text)
            self.status.set("Ошибка отправки")
            messagebox.showerror("Не удалось отправить письмо", error_text)
        finally:
            self._load_report_history()

    def run(self):
        self.root.mainloop()
