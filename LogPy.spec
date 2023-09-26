# -*- mode: python ; coding: utf-8 -*-


logpy = Analysis(
    ['logpy\\main.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
logpy_pyz = PYZ(logpy.pure)

logpy_exe = EXE(
    logpy_pyz,
    logpy.scripts,
    [],
    exclude_binaries=True,
    name='LogPy',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)


gui = Analysis(
    ['logpy\\gui.py'],
    pathex=[],
    binaries=[],
    datas=[('README.md', '.'), ('logpy/guiutils/results-icon.ico', 'icons'), ('logpy/guiutils/analysis-icon.ico', 'icons')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
gui_pyz = PYZ(gui.pure)

gui_exe = EXE(
    gui_pyz,
    gui.scripts,
    [],
    exclude_binaries=True,
    name='LogPy-Gui',
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
    icon=['logpy\\guiutils\\results-icon.ico'],
)

coll = COLLECT(
    logpy_exe,
    logpy.binaries,
    logpy.datas,

    gui_exe,
    gui.binaries,
    gui.datas,

    strip=False,
    upx=True,
    upx_exclude=[],
    name='LogPy',
)
