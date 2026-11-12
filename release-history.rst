.. _release_history:

Release and Version History
==============================================================================


2.0.1 (2026-11-11)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Breaking Changes**

- Drop Python 3.10, which reached end of life in October 2026; this release requires Python 3.11+. Users on Python 3.10 keep getting 2.0.0.

**Bugfixes**

- Ship the jinja2 templates (``rstobj/templates/*.rst``) in the wheel. The 2.0.0 wheel left them out, so any ``render()`` call raised ``jinja2.exceptions.TemplateNotFound`` after ``pip install rstobj``.

The fixes below only change output that was invalid reStructuredText or plainly wrong; every output that was valid before is unchanged, apart from trailing whitespace.

- ``Include``: render the options with their real hyphenated names (``:start-line:``, ``:end-line:``, ``:start-after:``, ``:end-before:``, ``:number-lines:``, ``:tab-width:``). The underscore names made docutils reject the directive.
- ``Include(literal=False)`` no longer renders ``:literal:``.
- ``BulletList`` and ``EnumList``: render an item that is an rstobj object, such as a nested list or a code block, instead of its Python repr.
- ``BulletList``, ``EnumList`` and ``ListTable``: indent the continuation lines of multi-line string items and cells, so they stay inside their item or cell. Strings whose continuation lines are already indented are left unchanged.
- ``Header``: count wide characters (CJK, emoji) as two columns when sizing the underline, so a non-ASCII title no longer gets an underline that is too short.
- ``Header``: an empty ``ref_label`` (for example from ``auto_label`` on a title made only of punctuation) no longer renders the invalid target ``.. _:``.
- ``CodeBlock`` and its language subclasses: render ``class_`` and ``name`` as ``:class:`` and ``:name:``; they were silently dropped.
- ``Image``: render ``scale`` as ``:scale: <n>%``; it was silently dropped.
- ``TableOfContent``: no longer render ``:name:``, which the ``contents`` directive does not accept.
- ``ListTable(widths=[])`` no longer renders an empty ``:widths:`` option.
- Changing ``rstobj.option.Options.tab`` now changes every indent, including directive options, so a table with a code block in a cell stays valid.
- No trailing whitespace: blank lines in indented output stay empty, and a directive with no argument renders ``.. code-block::`` with no space after it.

**Miscellaneous**

- New docs page, "Rendering Gallery": every example shows its Python code, the exact reStructuredText it produces, and how Sphinx renders it.
- Rewrite the tests around one list of cases (``rstobj/tests/cases.py``) shared with the gallery. Each case's output is compared byte for byte with a snapshot file, and checked to parse in docutils without a warning.
- The docs build now fails on any warning, locally and on Read the Docs.
- Fix the README example, which used imports removed in 2.0.0.
- CI builds the wheel, installs it in an isolated environment, and renders a header, so a wheel with missing files fails CI.
- Upgrade the locked ``anyio`` (a dev dependency through ``httpx2``) to 4.16.0, which removes a pytest 10 deprecation warning from the test run.
- Move to the new project template: ``uv``, ``mise`` tasks, ruff, and an updated CI.


2.0.0 (2026-04-05)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Breaking Changes**

- Drop support for Python < 3.10, now requires Python 3.10+.
- Replace ``attrs`` / ``attrs_mate`` dependency with standard library ``dataclasses``. All RST object classes are now plain ``@dataclass(kw_only=True)`` subclasses — no more ``@attr.s`` decorators.
- All dataclass fields are now keyword-only. Positional construction (e.g. ``Code("text")``) is no longer supported; use ``Code(text="text")`` instead.
- Remove ``meta_not_none_fields`` mechanism. Required fields are now expressed directly as fields without a default value; passing ``None`` will raise a ``TypeError`` at construction time.
- Remove ``__attrs_post_init__``; field validation logic moved to standard ``__post_init__``.

**Features and Improvements**

- Adopt ``|`` union syntax for all type hints (e.g. ``str | None`` instead of ``Optional[str]``).
- Add ``from __future__ import annotations`` to all modules for consistent lazy annotation evaluation.
- ``meta_directive_keyword`` and ``meta_lang`` class variables are now properly annotated with ``typing.ClassVar`` so dataclass does not treat them as fields.
- ``demo.py``: replace non-standard ``Path.select_image()`` call with standard ``Path.iterdir()`` filtered by extension; replace hardcoded absolute path in ``__main__`` block with ``Path(__file__)``-relative path.

**Miscellaneous**

- All test classes drop the obsolete ``(object)`` base class.
- All test ``if __name__ == "__main__":`` blocks now use ``run_cov_test`` instead of bare ``pytest.main``.
- Add ``__init__.py``-free duplicate-name test file support via ``importmode = "importlib"`` in pytest config.
- ``directives/__init__.py`` and ``markup/__init__.py``: replace ``from .module import *`` with explicit one-per-line imports.
- Add ``rstobj/directives/api.py`` and ``rstobj/markup/api.py`` as explicit public API surfaces.


1.2.1 (2022-09-17)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Features and Improvements**

- add ``widths`` option for ``ListTable``


1.1.1 (2022-09-11)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Miscellaneous**

- embrace type hint

**Breaking Changes**

- drop support for python2.7, 3.4, 3.5, only support for 3.6 +


0.0.7 (2019-05-25)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Minor Improvements**

Introduce type hint


0.0.6 (2019-01-09)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Features and Improvements**

add bullet list and enumerate list.

**Minor Improvements**

add usage example for all markup and directive.


0.0.5 (2018-12-02)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Features and Improvements**

- add ``.. include:: filepath`` directive
- add ``auto_label`` arg for ``Header`` markup.


0.0.4 (2018-11-23)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Bugfixes**

- fix ``.. image::`` directive align option bug


0.0.3 (2018-11-13)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Features and Improvements**

- add support for ``.. contents::`` directive.

**Bugfixes**

- fix codeblock lang error


0.0.2 (2018-10-28)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Features and Improvements**

- add support for ``.. code-block::`` directive.
- allow ``.. code-block::`` in ``ListTable``.
- support cross reference ``:ref``

**Minor Improvements**

- adapt pygitrepo >= 0.0.25


0.0.1 (2018-10-11)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- First release
