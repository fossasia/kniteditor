# -*- mode: python -*-

import sys
site_packages = [path for path in sys.path if path.rstrip("/\\").endswith('site-packages')]
print("site_packages:", site_packages)

from kivy.tools.packaging.pyinstaller_hooks import get_deps_all, hookspath, runtime_hooks

block_cipher = None

added_files = [(site_packages_, ".") for site_packages_ in site_packages]

kwargs = get_deps_all()
kwargs["datas"] = added_files
kwargs["hiddenimports"] += ['queue', 'unittest', 'unittest.mock']


a = Analysis(['_KnitEditor.py'],
             pathex=[],
             binaries=None,
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             hookspath=hookspath(),
             runtime_hooks=runtime_hooks(),
             **kwargs)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='KnitEditorX',
          debug=False,
          strip=False,
          upx=True,
          console=True )
coll = COLLECT(exe,
               Tree("/Applications/Kivy.app/Contents/Frameworks/SDL2_ttf.framework/Versions/A/Frameworks/FreeType.framework"),
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='KnitEditor')
app = BUNDLE(coll,
             name='KnitEditor.app',
             icon=None,
             bundle_identifier="com.ayab-knitting.KnitEditor")
