# -*- mode: python ; coding: utf-8 -*-
from version import __version__

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('templates/training_activated.html', 'templates'),
        ('.env.example', '.'),
    ],
    hiddenimports=['dotenv'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='InGenium Mailer',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='InGenium Mailer',
)

app = BUNDLE(
    coll,
    name='InGenium Mailer.app',
    icon='assets/InGenium-Mailer.icns',
    bundle_identifier='dev.andriiweb.ingeniummailer',
    info_plist={
        'CFBundleName': 'InGenium Mailer',
        'CFBundleDisplayName': 'InGenium Mailer',
        'CFBundleShortVersionString': __version__,
        'CFBundleVersion': __version__,
        'LSMinimumSystemVersion': '10.15',
    },
)
