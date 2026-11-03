#!/bin/bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT_DIR"

source .venv/bin/activate

VERSION="$(python -c 'from version import __version__; print(__version__)')"
APP_NAME="InGenium Mailer"
IDENTIFIER="dev.andriiweb.ingeniummailer"

python -m pip install --upgrade pip
python -m pip install -r requirements.txt

rm -rf build dist package-root
python -m PyInstaller --clean --noconfirm "InGenium-Mailer.spec"

mkdir -p "package-root/Applications"
ditto "dist/${APP_NAME}.app" "package-root/Applications/${APP_NAME}.app"

# No postinstall script: the app creates Application Support/.env/database
# under the logged-in user's account on its first launch.
pkgbuild \
  --root "package-root" \
  --identifier "$IDENTIFIER" \
  --version "$VERSION" \
  --install-location "/" \
  "dist/InGenium-Mailer-${VERSION}-macOS.pkg"

echo
echo "Готово:"
echo "  Приложение: dist/${APP_NAME}.app"
echo "  Установщик: dist/InGenium-Mailer-${VERSION}-macOS.pkg"
