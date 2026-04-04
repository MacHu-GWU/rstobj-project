# -*- coding: utf-8 -*-

"""
Other directives.
"""

from __future__ import annotations

import typing as T
from dataclasses import dataclass, field
from .base import Directive


@dataclass(kw_only=True)
class Include(Directive):
    """
    ``.. include::`` directive. Include an external document fragment.

    Example::

        inc = Include(path="README.rst")
        inc.render()

    Output::

        .. include:: README.rst

    Parameters definition see here http://docutils.sourceforge.net/docs/ref/rst/directives.html#including-an-external-document-fragment.
    """

    path: str
    start_line: int | None = field(default=None)
    end_line: int | None = field(default=None)
    start_after: str | None = field(default=None)
    end_before: str | None = field(default=None)
    literal: bool | None = field(default=None)
    code: str | None = field(default=None)
    number_lines: int | None = field(default=None)
    encoding: str | None = field(default=None)
    tab_width: int | None = field(default=None)

    meta_directive_keyword: T.ClassVar[str] = "include"

    @property
    def arg(self) -> str:
        return self.path
