# InGenium Mailer

Текущая версия: **0.2.0**. Версия хранится в `version.py`.

Небольшое desktop-приложение на Python для отправки клиентских писем InGenium Life.

## Возможности первой версии

- Ввод имени, email и названия тренинга.
- Ссылки на обучение и отзывы.
- HTML-письмо в фирменном стиле InGenium Life.
- Предпросмотр в браузере.
- Отправка через SMTP SSL.
- Локальная история отправок в SQLite.
- Отчёт об отправке в окне приложения: результат, дата, получатель, тема и тренинг.
- Просмотр последних 20 отправок при запуске.
- Подготовка к сборке в macOS `.app` через PyInstaller.

## Управление версиями

При выпуске новой версии измени только значение `__version__` в `version.py`, например `0.2.0` → `0.3.0`. Программа автоматически покажет эту версию в заголовке окна. При сборке PyInstaller используй то же значение для имени релиза.

## 1. Подготовка

Рекомендуется Python 3.11 или 3.12.

```bash
python3 --version
```

Создай виртуальное окружение и установи зависимости:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## 2. Настройка SMTP

Скопируй пример настроек:

```bash
cp .env.example .env
```

Открой `.env` и укажи SMTP-логин и пароль приложения Zoho.

Не добавляй `.env` в Git и никому не отправляй его содержимое.

## 3. Запуск

Из корня проекта:

```bash
python main.py
```

## 4. Сборка macOS `.app`

Сборку нужно выполнять на том Mac, для которого предназначена версия приложения. PyInstaller не является кросс-компилятором.

```bash
pyinstaller \
  --noconfirm \
  --clean \
  --windowed \
  --name "InGenium Mailer" \
  --add-data "templates:templates" \
  main.py
```

Готовое приложение появится здесь:

```text
dist/InGenium Mailer.app
```

Для Apple Silicon (M1/M2/M3/...) запускай сборку на Apple Silicon Mac с соответствующим Python.
Для Intel-сборки запускай её на Intel Mac с соответствующим Python.

## Где хранятся настройки и история

- При запуске из исходников файл `.env` находится в корне проекта, база — в `data/`.
- В собранном macOS `.app` файл `.env`, база SQLite и предпросмотр находятся в `~/Library/Application Support/InGenium Mailer/`.
- Шаблон HTML включается внутрь приложения как ресурс.

Для настройки собранного `.app` создай файл `.env` в `~/Library/Application Support/InGenium Mailer/` по образцу `.env.example`. Пароль SMTP не вшивается в приложение. На следующем этапе заменим хранение пароля в `.env` на macOS Keychain.
