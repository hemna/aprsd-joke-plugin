APRSD Joke Plugin
=================

|PyPI| |Status| |Python Version| |License|

|Read the Docs| |Tests| |Codecov|

|pre-commit|

.. |PyPI| image:: https://img.shields.io/pypi/v/aprsd-joke-plugin.svg
   :target: https://pypi.org/project/aprsd-joke-plugin/
   :alt: PyPI
.. |Status| image:: https://img.shields.io/pypi/status/aprsd-joke-plugin.svg
   :target: https://pypi.org/project/aprsd-joke-plugin/
   :alt: Status
.. |Python Version| image:: https://img.shields.io/pypi/pyversions/aprsd-joke-plugin
   :target: https://pypi.org/project/aprsd-joke-plugin
   :alt: Python Version
.. |License| image:: https://img.shields.io/pypi/l/aprsd-joke-plugin
   :target: https://opensource.org/licenses/MIT
   :alt: License
.. |Read the Docs| image:: https://img.shields.io/readthedocs/aprsd-joke-plugin/latest.svg?label=Read%20the%20Docs
   :target: https://aprsd-joke-plugin.readthedocs.io/
   :alt: Read the documentation at https://aprsd-joke-plugin.readthedocs.io/
.. |Tests| image:: https://github.com/hemna/aprsd-joke-plugin/workflows/Tests/badge.svg
   :target: https://github.com/hemna/aprsd-joke-plugin/actions?workflow=Tests
   :alt: Tests
.. |Codecov| image:: https://codecov.io/gh/hemna/aprsd-joke-plugin/branch/main/graph/badge.svg
   :target: https://codecov.io/gh/hemna/aprsd-joke-plugin
   :alt: Codecov
.. |pre-commit| image:: https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white
   :target: https://github.com/pre-commit/pre-commit
   :alt: pre-commit


Features
--------

* Get random jokes from the `v2.jokeapi.dev` API
* Support for multiple languages (English, German, Spanish, French, Portuguese)
* Multiple joke categories (Any, Misc, Programming, Dark, Pun, Spooky)
* Case-insensitive language and category parameters
* Automatic filtering of explicit content


Requirements
------------

* `aprsd >= 4.2.0`
* A running APRSD instance
* Internet connection to access the joke API


Installation
------------

You can install *APRSD Joke Plugin* via pip_ from PyPI_:

.. code:: console

   $ pip install aprsd-joke-plugin

Or using `uv`:

.. code:: console

   $ uv pip install aprsd-joke-plugin


Configuration
-------------

Before using the Joke plugin, you need to configure it in your APRSD configuration file.
Generate a sample configuration file if you haven't already:

.. code:: console

   $ aprsd sample-config

This will create a configuration file at `~/.config/aprsd/aprsd.conf` (or `aprsd.yml`).

Enable the Plugin
-----------------

To enable the plugin, add it to the ``enabled_plugins`` section of your APRSD configuration:

.. code:: ini

   [DEFAULT]
   enabled_plugins = aprsd_joke_plugin.aprsd_joke_plugin.JokeAPIPlugin

Plugin Configuration
--------------------

The plugin has an optional configuration section:

.. code:: ini

   [aprsd_joke_plugin]
   # Enable the plugin (default: False)
   enabled = True

**Note:** The plugin will automatically enable itself if it's listed in ``enabled_plugins``,
even if ``enabled = False`` in the plugin section. The ``enabled`` option in the plugin
section is primarily for disabling the plugin without removing it from ``enabled_plugins``.


Usage
-----

Once installed and configured, send a message to your APRSD instance starting with ``j`` or ``J``
to get a random joke.

Basic Usage
-----------

Send a message starting with ``j`` to get a random joke in English:

.. code::

   j

This will return a random joke from any category in English.

Specify Language
----------------

To get a joke in a specific language, use the ``l=<language>`` parameter:

.. code::

   j l=es

Supported languages:
   * ``de`` - German
   * ``en`` - English (default)
   * ``es`` - Spanish
   * ``fr`` - French
   * ``pt`` - Portuguese

Specify Category
----------------

To get a joke from a specific category, use the ``c=<category>`` parameter:

.. code::

   j c=pun

Supported categories:
   * ``any`` - Any category (default)
   * ``misc`` - Miscellaneous
   * ``prog`` - Programming jokes
   * ``dark`` - Dark jokes
   * ``pun`` - Pun jokes
   * ``sp`` - Spooky jokes

**Note:** Category names are case-insensitive. You can use the full names or abbreviations.

Combining Parameters
--------------------

You can combine language and category parameters:

.. code::

   j l=es c=pun

This will return a pun joke in Spanish.

Examples
--------

Get a random joke:
   ::

      j

Get a programming joke in English:
   ::

      j c=prog

Get a pun joke in Spanish:
   ::

      j l=es c=pun

Get a spooky joke in French:
   ::

      j l=fr c=sp

Example Interaction
-------------------

Here's an example of how a user would interact with the plugin via APRS messages:

**User sends:**
   ::

      j

**APRSD responds:**
   ::

      Why don't scientists trust atoms? Because they make up everything!

**User sends:**
   ::

      j c=prog

**APRSD responds:**
   ::

      Why do programmers prefer dark mode? Because light attracts bugs!

**User sends:**
   ::

      j l=es c=pun

**APRSD responds:**
   ::

      ¿Qué hace una abeja en el gimnasio? ¡Zum-ba!

**User sends:**
   ::

      j c=dark

**APRSD responds:**
   ::

      I was wondering why the frisbee was getting bigger, then it hit me.

Note: Responses are automatically wrapped to fit APRS message limits (67 characters per line),
so longer jokes may be split across multiple messages.

How It Works
------------

The plugin:
   1. Responds to messages starting with ``j`` or ``J``
   2. Parses optional language (``l=``) and category (``c=``) parameters
   3. Validates the language and category against allowed values
   4. Fetches a joke from the `v2.jokeapi.dev` API
   5. Returns the joke formatted for APRS message limits (67 characters per line)
   6. Automatically filters explicit content

The plugin uses the `v2.jokeapi.dev` API. You can find more information about the API
at https://v2.jokeapi.dev/

Verifying It's Working
----------------------

After starting APRSD, check the logs for messages like:

.. code::

   INFO: Registering Base plugin 'JokeAPIPlugin'(x.x.x)

Send a test message to your APRSD instance:

.. code::

   j

You should receive a joke in response.


Contributing
------------

Contributions are very welcome.
To learn more, see the `Contributor Guide`_.


License
-------

Distributed under the terms of the `MIT license`_,
*APRSD Joke Plugin* is free and open source software.


Issues
------

If you encounter any problems,
please `file an issue`_ along with a detailed description.


Credits
-------

This project was generated from `@hemna`_'s `APRSD Plugin Python Cookiecutter`_ template.

.. _@hemna: https://github.com/hemna
.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _MIT license: https://opensource.org/licenses/MIT
.. _PyPI: https://pypi.org/
.. _APRSD Plugin Python Cookiecutter: https://github.com/hemna/cookiecutter-aprsd-plugin
.. _file an issue: https://github.com/hemna/aprsd-joke-plugin/issues
.. _pip: https://pip.pypa.io/
.. github-only
.. _Contributor Guide: CONTRIBUTING.rst
.. _Usage: https://aprsd-joke-plugin.readthedocs.io/en/latest/usage.html
