# -*- coding: utf-8 -*-

"""
table of content directive.
"""

from __future__ import annotations

import typing as T
from dataclasses import dataclass, field
from .base import Directive


@dataclass(kw_only=True)
class TableOfContent(Directive):
    """
    ``.. contents::`` directive.

    parameter definition see here: http://docutils.sourceforge.net/docs/ref/rst/directives.html#table-of-contents

    :param title: str, required.
    :param depth: int, optional.
    :param local: bool, optional.

    :type backlinks: str
    :param backlinks: optional. one of
        :attr:`TableOfContent.BacklinksOptions`.

    Example::

        toc = TableOfContent(title="Table of Contents", depth=2)
        toc.render()

    Output::

        .. contents:: Table of Contents
            :depth: 2
    """

    title: str | None = field(default=None)
    depth: int | None = field(default=None)
    local: bool = field(default=False)
    backlinks: str | None = field(default=None)

    meta_directive_keyword: T.ClassVar[str] = "contents"

    class BacklinksOptions:
        """
        ``backlinks`` argument choices.

        - ``TableOfContent.BacklinksOptions.entry``: ``"entry"``
        - ``TableOfContent.BacklinksOptions.top``: ``"top"``
        - ``TableOfContent.BacklinksOptions.none``: ``"none"``
        """

        entry = "entry"
        top = "top"
        none = "none"

    def __post_init__(self):
        if self.backlinks not in [None, "entry", "top", "none"]:  # pragma: no cover
            raise ValueError(
                "TableOfContent.backlinks has to be one of 'entry', 'top', 'none'!"
            )

    @property
    def arg(self) -> str:
        if self.title is None:
            return ""
        else:
            return self.title
