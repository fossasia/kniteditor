windows-build
=============

This directory contains the files to build the windows executable and
installer.

You can read the `kivy documentation 
<https://kivy.org/docs/guide/packaging-windows.html>`__
on how this build came to be.

We use `pyinstaller <https://pyinstaller.readthedocs.io/>`__ to create the
binaries.
`Inno Setup 5 <http://www.jrsoftware.org/isinfo.php>`__ is used to build the
installer. Note that Inno Setup 5 has its worn license attached.

Appveyor executes the windows build when a new release is drafted.