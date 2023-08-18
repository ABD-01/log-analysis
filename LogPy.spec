# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


logpy = Analysis(['logpy\\main.py'], pathex=[], binaries=[], datas=[], hiddenimports=[], hookspath=[], hooksconfig={}, runtime_hooks=[], excludes=[], win_no_prefer_redirects=False, win_private_assemblies=False, cipher=block_cipher, noarchive=False,)
logpy_pyz = PYZ(logpy.pure, logpy.zipped_data, cipher=block_cipher)

logpy_exe = EXE(logpy_pyz, logpy.scripts, [], exclude_binaries=True, name='LogPy', debug=False, bootloader_ignore_signals=False, strip=False, upx=True, console=True, disable_windowed_tr =False, argv_emulation=False, target_arch=None, codesign_identity=None, entitlements_file=None,)


gui = Analysis(['logpy\\gui.py'], pathex=[], binaries=[], datas=[('README.md', '.'), ('logpy/guiutils/results-icon.ico', 'icons')], hiddenimports=[], hookspath=[], hooksconfig={}, runtime_hooks=[], excludes=[], win_no_prefer_redirects=False, win_private_assemblies=False, cipher=block_cipher, noarchive=False,)
gui_pyz = PYZ(gui.pure, gui.zipped_data, cipher=block_cipher)

gui_exe = EXE(gui_pyz, gui.scripts, [], exclude_binaries=True, name='LogPy-Gui', debug=False, bootloader_ignore_signals=False, strip=False, upx=True, console=False, disable_windowed_traceback=False, argv_emulation=False, target_arch=None, codesign_identity=None, entitlements_file=None, icon=['logpy\\guiutils\\results-icon.ico'],)


gui2 = Analysis(['logpy\\gui_devel.py'], pathex=[], binaries=[], datas=[('README.md', '.'), ('logpy/guiutils/results-icon.ico', 'icons')], hiddenimports=[], hookspath=[], hooksconfig={}, runtime_hooks=[], excludes=[], win_no_prefer_redirects=False, win_private_assemblies=False, cipher=block_cipher, noarchive=False,)
gui2_pyz = PYZ(gui2.pure, gui2.zipped_data, cipher=block_cipher)

gui2_exe = EXE(gui2_pyz, gui2.scripts, [], exclude_binaries=True, name='LogPy-Gui2', debug=False, bootloader_ignore_signals=False, strip=False, upx=True, console=False, disable_windowed_traceback=False, argv_emulation=False, target_arch=None, codesign_identity=None, entitlements_file=None, icon=['logpy\\guiutils\\results-icon.ico'],)

coll = COLLECT(
    logpy_exe,
    logpy.binaries,
    logpy.zipfiles,
    logpy.datas,

    gui_exe,
    gui.binaries,
    gui.zipfiles,
    gui.datas,

    gui2_exe,
    gui2.binaries,
    gui2.zipfiles,
    gui2.datas,

    strip=False,
    upx=True,
    upx_exclude=[],
    name='LogPy',
)
