# -*- coding: utf-8 -*-

from __future__ import annotations

from dataclasses import dataclass, field
from typing import ClassVar
from ..base import RstObj


@dataclass(kw_only=True)
class Directive(RstObj):
    class_: str | None = field(default=None)
    name: str | None = field(default=None)

    meta_directive_keyword: ClassVar[str | None] = None

    @property
    def arg(self):  # pragma: no cover
        raise NotImplementedError
