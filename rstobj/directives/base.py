# -*- coding: utf-8 -*-

from __future__ import annotations

import typing as T
from dataclasses import dataclass
from dataclasses import field
from ..base import RstObj


@dataclass(kw_only=True)
class Directive(RstObj):
    class_: str | None = field(default=None)
    name: str | None = field(default=None)

    meta_directive_keyword: T.ClassVar[str | None] = None
    #: False for a directive that has no ``:name:`` option, such as ``contents``.
    meta_supports_name: T.ClassVar[bool] = True

    @property
    def arg(self):  # pragma: no cover
        raise NotImplementedError
