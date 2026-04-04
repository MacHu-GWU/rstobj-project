# -*- coding: utf-8 -*-

"""
image related directives.
"""

from __future__ import annotations

import typing as T
from dataclasses import dataclass, field
from .base import Directive


@dataclass(kw_only=True)
class Image(Directive):
    """
    The ``.. image::`` directive.

    parameter definition see here: http://docutils.sourceforge.net/docs/ref/rst/directives.html#image

    :param uri: required.
    :param height: optional.
    :param width: optional.
    :param scale: optional.
    :param alt_text: optional.
    :param align: optional. one of :class:`Image.AlignOptions`.

    Example::

        img = Image(
            uri="https://www.python.org/static/img/python-logo.png",
            height=320,
            width=320,
            alt_text="Image Not Found",
            align=Image.AlignOptions.center,
        )
        img.render()

    Output::

        .. image:: https://www.python.org/static/img/python-logo.png
            :height: 320px
            :width: 320px
            :alt: Image Not Found
            :align: center
    """

    uri: str
    height: int | None = field(default=None)
    width: int | None = field(default=None)
    scale: int | None = field(default=None)
    alt_text: str | None = field(default=None)
    align: str | None = field(default=None)

    meta_directive_keyword: T.ClassVar[str] = "image"

    class AlignOptions:
        """
        ``align`` argument choices.

        - ``Image.AlignOptions.left``: ``"left"``
        - ``Image.AlignOptions.center``: ``"center"``
        - ``Image.AlignOptions.right``: ``"right"``
        - ``Image.AlignOptions.top``: ``"top"``
        - ``Image.AlignOptions.middle``: ``"middle"``
        - ``Image.AlignOptions.bottom``: ``"bottom"``
        """

        left = "left"
        center = "center"
        right = "right"
        top = "top"
        middle = "middle"
        bottom = "bottom"

    def __post_init__(self):
        if self.align not in [None, "left", "center", "right", "top", "middle", "bottom"]:  # pragma: no cover
            raise ValueError(
                "Image.align has to be one of 'left', 'center', 'right', 'top', 'middle', 'bottom'!"
            )

    @property
    def arg(self) -> str:
        return self.uri
