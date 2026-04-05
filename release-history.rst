.. _release-history:

Release and Version History
==============================================================================


2.0.0 (2026-04-04)
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
