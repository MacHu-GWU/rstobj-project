# -*- coding: utf-8 -*-

"""
Bullet list.
"""

from __future__ import annotations

from dataclasses import dataclass
from ..base import RstObj


@dataclass(kw_only=True)
class BulletList(RstObj):
    """
    Bullet list class.

    Example::

        blist = BulletList(items=["a", "b", "c"])
        blist.render()

    Output::

        - a
        - b
        - c

    More example: http://docutils.sourceforge.net/docs/user/rst/quickref.html#bullet-lists
    """

    items: list
