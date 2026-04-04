# -*- coding: utf-8 -*-

"""
table related directives.
"""

from __future__ import annotations

import typing as T
from dataclasses import dataclass, field
from .base import Directive


@dataclass(kw_only=True)
class ListTable(Directive):
    """
    List Tabulate Table.

    parameter definition see here http://docutils.sourceforge.net/docs/ref/rst/directives.html#list-table.

    :param data: list of list.
    :param title: str, optional.
    :param index: bool, use first column as index. default False.
    :param header: bool, use first row as header. default True.
    :param widths: list of int
    :param align:

    Example::

        ltable = rstobj.directives.ListTable(
            data=[["id", "name"], [1, "Alice"], [2, "Bob"]],
            title="Users",
            header=True,
        )
        ltable.render()

    Output::

        .. list-table:: Title of the table
            :widths: 10 10 10
            :header-rows: 1

            * - Header1
              - Header2
              - Header3
            * - Value1
              - Value2
              - Value3
    """

    data: list
    title: str = field(default="")
    index: bool = field(default=False)
    header: bool = field(default=True)
    widths: list[int] | None = field(default=None)
    align: str | None = field(default=None)

    meta_directive_keyword: T.ClassVar[str] = "list-table"

    class AlignOptions:
        """
        ``align`` parameter choices.
        """

        left = "left"
        center = "center"
        right = "right"

    def __post_init__(self):
        if self.align not in [None, "left", "center", "right"]:  # pragma: no cover
            raise ValueError(
                "ListTable.align has to be one of 'left', 'center', 'right'!"
            )

    @property
    def widths_arg(self) -> str:
        return " ".join([str(i) for i in self.widths])

    @property
    def arg(self) -> str:
        return self.title
