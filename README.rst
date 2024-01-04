Introduction
============

.. image:: https://ensmarten-ing-assets.s3.amazonaws.com/minihass_social.png
    :alt: Minihass Banner
|
.. image:: https://github.com/ensmartening/CircuitPython_minihass/actions/workflows/build.yml/badge.svg
    :target: https://github.com/ensmartening/CircuitPython_minihass/actions/workflows/build.yml
    :alt: Build Status

.. image:: https://codecov.io/gh/ensmartening/CircuitPython_minihass/graph/badge.svg?token=9H0KNZC0PO
    :target: https://codecov.io/gh/ensmartening/CircuitPython_minihass
    :alt: Codecov Status

.. image:: https://github.com/ensmartening/CircuitPython_minihass/actions/workflows/sphinx.yml/badge.svg
    :target: https://CircuitPython_minihass.ensmarten.ing
    :alt: Docs Status

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/psf/black
    :alt: Code Style: Black

A lightweight Python package to interact with Home Assistant over MQTT, intended for use with CircuitPython and the Adafruit MiniMQTT library.


Dependencies
=============
This driver depends on:

* `Adafruit CircuitPython <https://github.com/adafruit/circuitpython>`_

Please ensure all dependencies are available on the CircuitPython filesystem.
This is easily achieved by downloading
`the Adafruit library and driver bundle <https://circuitpython.org/libraries>`_
or individual libraries can be installed using
`circup <https://github.com/adafruit/circup>`_.

..
    Installing from PyPI
    =====================
    .. note:: This library is not available on PyPI yet. Install documentation is included
    as a standard element. Stay tuned for PyPI availability!

    Todo: Remove the above note if PyPI version is/will be available at time of release.

    On supported GNU/Linux systems like the Raspberry Pi, you can install the driver locally `from
    PyPI <https://pypi.org/project/cybershoe-circuitpython-minihass/>`_.
    To install for current user:

    .. code-block:: shell

        pip3 install cybershoe-circuitpython-minihass

    To install system-wide (this may be required in some cases):

    .. code-block:: shell

        sudo pip3 install cybershoe-circuitpython-minihass

    To install in a virtual environment in your current project:

    .. code-block:: shell

        mkdir project-name && cd project-name
        python3 -m venv .venv
        source .env/bin/activate
        pip3 install cybershoe-circuitpython-minihass

    Installing to a Connected CircuitPython Device with Circup
    ==========================================================

    Make sure that you have ``circup`` installed in your Python environment.
    Install it with the following command if necessary:

    .. code-block:: shell

        pip3 install circup

    With ``circup`` installed and your CircuitPython device connected use the
    following command to install:

    .. code-block:: shell

        circup install cybershoe_minihass

    Or the following command to update an existing version:

    .. code-block:: shell

        circup update

    Usage Example
    =============

    Todo: Add a quick, simple example. It and other examples should live in the
    examples folder and be included in docs/examples.rst.

Documentation
=============
API documentation for this library can be found on `ensmarten.ing <https://circuitpython-minihass.ensmarten.ing/>`_.

Contributing
============

Contributions are welcome! Please read our `Code of Conduct
<https://github.com/ensmartening/CircuitPython_minihass/blob/HEAD/CODE_OF_CONDUCT.md>`_
before contributing to help this project stay welcoming.
