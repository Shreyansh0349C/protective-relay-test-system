# -*- mode: python ; coding: utf-8 -*-

import sys
from PyInstaller.utils.hooks import collect_submodules, collect_data_files

block_cipher = None

hidden_imports = []
hidden_imports.extend(collect_submodules('pyqtgraph'))
hidden_imports.extend(collect_submodules('PySide6'))
hidden_imports.extend(collect_submodules('numpy'))
hidden_imports.extend(collect_submodules('serial'))

datas = []
datas.extend(collect_data_files('pyqtgraph'))

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=hidden_imports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['tkinter', 'unittest', 'matplotlib', 'pydoc'],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='RELAYLAB-X',
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
    name='RELAYLAB-X',
)

if sys.platform == 'darwin':
    app = BUNDLE(
        coll,
        name='RELAYLAB X.app',
        icon=None,
        bundle_identifier='com.relaylab.x',
        info_plist={
            'NSHighResolutionCapable': 'True',
            'CFBundleDisplayName': 'RELAYLAB X',
            'CFBundleName': 'RELAYLAB X',
            'CFBundleVersion': '0.1.0',
            'CFBundleShortVersionString': '0.1.0',
        },
    )
