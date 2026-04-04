# -*- coding: utf-8 -*-

from __future__ import annotations

from dataclasses import dataclass
from ..base import RstObj


@dataclass(kw_only=True)
class URI(RstObj):
    """
    Example::

        uri = URI(title="Hello World", link="https://www.google.com")
        uri.render()

    Output::

        `Hello World <https://www.google.com>`_
    """

    title: str
    link: str


URL = URI


@dataclass(kw_only=True)
class Reference(RstObj):
    """
    Example::

        ref = Reference(title="Hello World", label="hello-world")
        ref.render()

    Output::

        :ref:`Hello World <hello-world>`
    """

    title: str
    label: str


Ref = Reference
