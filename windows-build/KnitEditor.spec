# -*- mode: python -*-
from kivy.deps import sdl2, glew
import sys
site_packages = [path for path in sys.path if path.rstrip("/\\").endswith('site-packages')]
print(site_packages)
block_cipher = None

added_files = [(site_packages_, ".") for site_packages_ in site_packages]


a = Analysis(['KnitEditor.py'],
             pathex=['.'] + sys.path,
             binaries=None,
             datas=added_files,
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='KnitEditor',
          debug=False,
          strip=False,
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               *[Tree(p) for p in (sdl2.dep_bins + glew.dep_bins)],
               strip=False,
               upx=True,
               name='KnitEditor')
