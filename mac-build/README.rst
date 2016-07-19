mac-build
=========

This installer is based on `the kivy documentation
<https://kivy.org/docs/guide/packaging-osx.html>`__.
Tihs build is automatically triggered by travis. When a tag is pushed, the outcome is uplaoded to the github releases.

Preconditions
-------------

``brew`` should be installed already. You can install it manually before you execute ``ìnstall.sh`` with this command (`source <http://brew.sh/>`__):

.. code:: bash

    /usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"

Installation
------------

If you are on a Mac computer, you can run the following in the Terminal

.. code:: bash

    ./install.sh --user

to create the dmg file. The build step is included.

Build
-----

If you have run the ``install.sh`` file already, you can run

.. code:: bash

     ./build.sh --user

to skip the obsolete installation steps.

Uninstall
---------

If you really want to uninstall everything that was installed, you can run:

.. code:: bash

    ./uninstall.sh

Note that you may want to read what it does, before. It might be that you do not want to set your computer back so much.

