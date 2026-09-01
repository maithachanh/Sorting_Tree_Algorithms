# -*- mode: python ; coding: utf-8 -*-
import sys
import os

block_cipher = None
base_dir = os.path.abspath(os.getcwd())

datas = [
    (os.path.join(base_dir, 'assets'), 'assets'),
    (os.path.join(base_dir, 'config.py'), '.'),
    (os.path.join(base_dir, 'Algorithms'), 'Algorithms'),
    (os.path.join(base_dir, 'gui'), 'gui'),
    (os.path.join(base_dir, 'utils'), 'utils'),
]

a = Analysis(
    ['main.py'],
    pathex=[base_dir],
    binaries=[],
    datas=datas,
    hiddenimports=[
        'PyQt5',
        'PyQt5.QtCore',
        'PyQt5.QtGui',
        'PyQt5.QtWidgets',
        'pygments',
        'pygments.lexers',
        'pygments.formatters',
        'pygments.styles',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['tkinter', 'unittest', 'email', 'http', 'xml', 'pydoc'],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='Visual_AlgoStudio',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,                  # Tắt màn hình console đen khi mở app
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=os.path.join(base_dir, 'assets', 'app_icon.ico'),
)