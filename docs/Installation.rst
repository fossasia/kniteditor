.. _installation:

kniteditor Installation Instructions
====================================

Kivy Installation
-----------------

.. warning:: Kivy as of today, 2016/07/04, works for Python 3.4. If you intend to use an other version,
  be aware that it might take a lot of time.

Windows
~~~~~~~

1. If kivy does not work, uninstall kivy.

  .. code:: bash
  
      py -3.4 -m pip uninstall kivy

2. Uninstall Python 3.4. Unless you want to install Visual Studio and configure how to compile Python modules with the right compiler at the right location, you uninstall Python 3.4. All the installed packages wil be left untouched. This is why we uninstalled kivy before.

3. Use the `kivy installer <https://github.com/KeyWeeUsr/KivyInstaller>`__ to install kivy. [`Thanks <https://github.com/kivy/kivy/issues/4287#issuecomment-229910592>`__]

Ubuntu
~~~~~~

See the `kivy installation instructions <https://kivy.org/docs/installation/installation.html>`__.

Package installation from Pypi
------------------------------

The kniteditor library requires `Python 3 <https://www.python.org/>`__.
It can be installed form the `Python Package Index
<https://pypi.python.org/pypi/kniteditor>`__.

Windows
~~~~~~~

Install it with a specific python version under windows:

.. code:: bash

    py -3 -m pip --no-cache-dir install --upgrade kniteditor

Test the installed version:

.. code:: bash

    py -3 -m pytest --pyargs kniteditor

Linux
~~~~~ 

To install the version from the python package index, you can use your terminal and execute this under Linux:

.. code:: shell
  
  sudo python3 -m pip --no-cache-dir install --upgrade kniteditor

test the installed version:

.. code:: shell
  
  python3 -m pytest --pyargs kniteditor

.. _installation-repository:

Installation from Repository
----------------------------

You can setup the development version under Windows and Linux.

.. _installation-repository-linux:

Linux
~~~~~

If you wish to get latest source version running, you can check out the repository and install it manually.

.. code:: bash

  git clone https://github.com/AllYarnsAreBeautiful/kniteditor.git
  cd kniteditor
  sudo python3 -m pip install --upgrade pip
  sudo python3 -m pip install -r requirements.txt
  sudo python3 -m pip install -r test-requirements.txt
  py.test

To also make it importable for other libraries, you can link it into the site-packages folder this way:

.. code:: bash

  sudo python3 setup.py link

.. _installation-repository-windows:

Windows
~~~~~~~

Same as under :ref:`installation-repository-linux` but you need to replace
``sudo python3`` with ``py -3``. This also counts for the following
documentation.
