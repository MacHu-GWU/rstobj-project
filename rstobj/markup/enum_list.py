# -*- coding: utf-8 -*-

"""
Enumerate list.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from ..base import RstObj


@dataclass(kw_only=True)
class EnumList(RstObj):
    """
    Enumerate list class.

    Example::

        blist = Enumerate(items=["a", "b", "c"], start_num=3)
        blist.render()

    Output::

        3. a
        4. b
        5. c

    More example: http://docutils.sourceforge.net/docs/user/rst/quickref.html#enumerated-lists
    """

    items: list
    start_num: int = field(default=1)
