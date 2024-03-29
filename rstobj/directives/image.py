# -*- coding: utf-8 -*-

"""
image related directives.
"""

import attr
from .base import Directive


@attr.s
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
    uri: str = attr.ib(default=None)
    height: int = attr.ib(
        default=None,
        validator=attr.validators.optional(attr.validators.instance_of(int)),
    )
    width: int = attr.ib(
        default=None,
        validator=attr.validators.optional(attr.validators.instance_of(int)),
    )
    scale: int = attr.ib(
        default=None,
        validator=attr.validators.optional(attr.validators.instance_of(int)),
    )
    alt_text: str = attr.ib(default=None)
    align: str = attr.ib(default=None)

    meta_directive_keyword: str = "image"
    meta_not_none_fields: tuple = ("uri",)

    class AlignOptions(object):
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

    @align.validator
    def check_align(self, attribute, value):  # pragma: no cover
        if value not in [None, "left", "center", "right", "top", "middle", "bottom"]:
            raise ValueError(
                "ListTable.align has to be one of 'left', 'center', 'right', 'top', 'middle', 'bottom'!"
            )

    @property
    def arg(self):
        """
        :rtype:
        """
        return self.uri
