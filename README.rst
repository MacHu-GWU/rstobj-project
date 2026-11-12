
.. image:: https://readthedocs.org/projects/rstobj/badge/?version=latest
    :target: https://rstobj.readthedocs.io/en/latest/
    :alt: Documentation Status

.. image:: https://github.com/MacHu-GWU/rstobj-project/actions/workflows/main.yml/badge.svg
    :target: https://github.com/MacHu-GWU/rstobj-project/actions?query=workflow:CI

.. image:: https://codecov.io/gh/MacHu-GWU/rstobj-project/branch/main/graph/badge.svg
    :target: https://codecov.io/gh/MacHu-GWU/rstobj-project

.. image:: https://img.shields.io/pypi/v/rstobj.svg
    :target: https://pypi.python.org/pypi/rstobj

.. image:: https://img.shields.io/pypi/l/rstobj.svg
    :target: https://pypi.python.org/pypi/rstobj

.. image:: https://img.shields.io/pypi/pyversions/rstobj.svg
    :target: https://pypi.python.org/pypi/rstobj

.. image:: https://img.shields.io/badge/✍️_Release_History!--None.svg?style=social&logo=github
    :target: https://github.com/MacHu-GWU/rstobj-project/blob/main/release-history.rst

.. image:: https://img.shields.io/badge/⭐_Star_me_on_GitHub!--None.svg?style=social&logo=github
    :target: https://github.com/MacHu-GWU/rstobj-project

------

.. image:: https://img.shields.io/badge/Link-API-blue.svg
    :target: https://rstobj.readthedocs.io/en/latest/py-modindex.html

.. image:: https://img.shields.io/badge/Link-Install-blue.svg
    :target: `install`_

.. image:: https://img.shields.io/badge/Link-GitHub-blue.svg
    :target: https://github.com/MacHu-GWU/rstobj-project

.. image:: https://img.shields.io/badge/Link-Submit_Issue-blue.svg
    :target: https://github.com/MacHu-GWU/rstobj-project/issues

.. image:: https://img.shields.io/badge/Link-Request_Feature-blue.svg
    :target: https://github.com/MacHu-GWU/rstobj-project/issues

.. image:: https://img.shields.io/badge/Link-Download-blue.svg
    :target: https://pypi.org/pypi/rstobj#files


Welcome to ``rstobj`` Documentation
==============================================================================
.. image:: https://rstobj.readthedocs.io/en/latest/_static/rstobj-logo.png
    :target: https://rstobj.readthedocs.io/en/latest/

``rstobj`` is a library that construct Restructured Text markup or directives from Python Code. ``rstobj`` is based on ``jinja2``.

**The idea behind rstobj**:

RestructuredText is super powerful, way more powerful than markdown. But have you ever think of **customize YOUR OWN markup or directive and do some magic?**

Have you think of automatically generate customized document from your code or tabulate data?

`Sphinx Doc <http://www.sphinx-doc.org/en/master/>`_ is the ultimate doc build tool. With ``rstobj``, you can **easily create your own markup / directive, and hide complex workflow behind a single markup / directive**, then use it when you need it. Here's some ideas:

1. Use ``.. include-all-image::`` to automatically scan image file under a directory, create ``.. image::`` directive and organize everything in a table.
2. Separate comment and value of the config file, automatically create an document for a config file.
3. ...

I have a `Blog Post <https://github.com/MacHu-GWU/Tech-Blog/issues/6>`_ to share how to create a sphinx doc extension in 50 lines and customize your own directive (Sorry, its written in Chinese).


**Example**:

.. code-block:: python

    import rstobj.api as rstobj

    header = rstobj.markup.Header(title="Section1", header_level=1, auto_label=True)
    print(header.render())

    ltable = rstobj.directives.ListTable(
        data=[["id", "name"], [1, "Alice"], [2, "Bob"]],
        title="Users",
        header=True,
    )
    print(ltable.render())

Output::

    .. _Section1:

    Section1
    ========

    .. list-table:: Users
        :header-rows: 1
        :stub-columns: 0

        * - id
          - name
        * - 1
          - Alice
        * - 2
          - Bob

See the `Rendering Gallery <https://rstobj.readthedocs.io/en/latest/01-Rendering-Gallery/index.html>`_ for every supported markup and directive, with its Python code, its output, and how it renders.

I recommend to use this in your jinja2 template, content of ``output.rst``::

    {{ header.render() }}
    {{ ltable.render() }}

And use ``rstobj`` with ``sphinx-jinja`` library https://pypi.org/project/sphinx-jinja/ in sphinx doc project.

**Supported directives**:

- ``.. image::``
- ``.. list-table::``
- ``.. contents::``
- ``.. code-block::``
- ``.. include::``

**Supported markup**:

- ``Header``::

    .. _ref-label:

    Title
    =====

- ``URL``: ```Text <Target>`_``
- ``Reference``: ``:ref:`Text <Target>```


**If you need more features, please submit an issue to** https://github.com/MacHu-GWU/rstobj-project/issues


.. _install:

Install
------------------------------------------------------------------------------

``rstobj`` is released on PyPI, so all you need is:

.. code-block:: console

    $ pip install rstobj

To upgrade to latest version:

.. code-block:: console

    $ pip install --upgrade rstobj

.. _use-with-ai-coding-agents:

Use with AI Coding Agents
------------------------------------------------------------------------------

This repo ships an `Agent Skill <https://code.claude.com/docs/en/skills>`_ that documents the public API of ``rstobj``, so an AI coding agent such as Claude Code can use the library without reading its source. It lives in `.claude/skills/pypi-rstobj <https://github.com/MacHu-GWU/rstobj-project/tree/main/.claude/skills/pypi-rstobj>`_. To use it in your project, copy it into your project's ``.claude/skills/`` folder. Run this from your project's root:

.. code-block:: console

    $ git clone --depth 1 https://github.com/MacHu-GWU/rstobj-project.git /tmp/rstobj-project
    $ mkdir -p .claude/skills
    $ cp -R /tmp/rstobj-project/.claude/skills/pypi-rstobj .claude/skills/
