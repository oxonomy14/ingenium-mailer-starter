# InGenium Mailer

Текущая версия: **0.3.0**. Единственный источник версии — `version.py`.

Desktop-приложение для отправки клиентских писем InGenium Life.

## Возможности

- Форма клиента и тренинга.
- HTML-шаблон активации тренинга.
- Предпросмотр письма в браузере.
- Отправка через Zoho SMTP SSL.
- История отправок и отчёт в SQLite.
- Сборка macOS `.app` и установщика `.pkg`.

## Системные требования

- macOS.
- Python 3.11 или 3.12 для сборки.
- Сборку выполняй на Mac с той архитектурой, для которой нужен установщик (Intel или Apple Silicon).

## Локальная разработка

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
python main.py
```

При запуске из исходников настройки и база находятся в `data/`.

## Создание установщика macOS

1. Убедись, что SMTP-секреты не находятся в `.env.example`. В нём должны быть только пустые/примерные значения.
2. Сделай скрипт исполняемым, если нужно:

```bash
chmod +x build_installer.sh
```

3. Запусти сборку:

```bash
./build_installer.sh
```

Скрипт:
- устанавливает зависимости в `.venv`;
- собирает приложение по `InGenium-Mailer.spec`;
- создаёт `dist/InGenium Mailer.app`;
- создаёт установщик `dist/InGenium-Mailer-0.3.0-macOS.pkg`.

Открой `.pkg` двойным щелчком и пройди стандартную установку macOS. Приложение установится в `/Applications`.

## Что создаётся при установке

Установщик запускает `installer/scripts/postinstall`. Для текущего вошедшего в macOS пользователя он создаёт:

```text
~/Library/Application Support/InGenium Mailer/
    .env
```

В `.env` будет шаблон настроек без пароля. При первом запуске приложения SQLite автоматически создаст:

```text
mail_history.db
```

После предпросмотра письма появится:

```text
email_preview.html
```

Приложение не перезаписывает существующий `.env` и не удаляет базу при обновлении. Поэтому настройки SMTP и история отправок сохраняются.

Если установка выполнялась без активной пользовательской сессии, папка Application Support будет создана при первом запуске приложения, а `.env` будет скопирован из ресурсов приложения.

## Настройка SMTP после установки

Открой файл:

```text
~/Library/Application Support/InGenium Mailer/.env
```

Укажи SMTP-логин и пароль приложения Zoho. Не сохраняй реальные секреты в Git и не передавай `.env` другим людям.

## Где находятся файлы

- Приложение: `/Applications/InGenium Mailer.app`
- Настройки и история: `~/Library/Application Support/InGenium Mailer/`
- База: `~/Library/Application Support/InGenium Mailer/mail_history.db`

## Обновление приложения

При установке новой версии поверх старой папка Application Support не удаляется. История SQLite и пользовательский `.env` сохраняются.

Версию релиза меняй в `version.py`. При изменении версии также обновляй `CFBundleShortVersionString` и `CFBundleVersion` в `InGenium-Mailer.spec`, а также версию в документации/имени установщика, если она указана явно.


## Настройки SMTP в интерфейсе (v0.4.0)

В главном окне приложения нажми **«Настройки SMTP»**. Там можно изменить:
- SMTP-сервер и порт;
- логин и пароль приложения;
- имя и email отправителя;
- ссылки на обучение и отзывы.

Кнопка **«Проверить подключение»** проверяет SSL-соединение и авторизацию, но не отправляет письмо. Кнопка **«Сохранить»** записывает настройки в `~/Library/Application Support/InGenium Mailer/.env`. Существующий файл не перезаписывается установщиком.

Пароль сейчас хранится в локальном `.env` с правами доступа `600`; это не эквивалентно Keychain. Интеграцию с macOS Keychain можно добавить отдельно.


## Іконка macOS

Іконка програми зберігається в `assets/InGenium-Mailer.icns`; вихідне PNG — `assets/InGenium-Mailer-Icon.png`.
PyInstaller підключає ICNS через параметр `icon` у `InGenium-Mailer.spec`. Після перескладання `.app` і `.pkg` Finder та Dock мають показувати фірмову іконку InGenium Mailer.


## v0.4.1 — виправлення встановлення macOS

Установчий пакет більше не запускає `postinstall`. Це усуває помилку виконання скрипта в ізольованому середовищі macOS Installer.

Папка `~/Library/Application Support/InGenium Mailer/`, файл `.env` та SQLite-база створюються самим застосунком під час першого запуску. У `app/config.py` шаблон `.env.example` уже включено до ресурсів PyInstaller. Наявний `.env` не перезаписується.
