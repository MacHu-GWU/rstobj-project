# -*- coding: utf-8 -*-

"""
RestructuredText Object abstraction.
"""

from __future__ import annotations

import typing as T
from dataclasses import dataclass

if T.TYPE_CHECKING:  # pragma: no cover
    from jinja2 import Template

from .templates import env
from .option import Options


def _indent_line(line: str, prefix: str) -> str:
    """
    Prefix a line and strip its trailing whitespace. A blank line stays empty,
    so indenting never leaves whitespace-only lines.
    """
    line = line.rstrip()
    if line:
        return prefix + line
    else:
        return ""


def _indent_continuation(text: str, width: int, force: bool) -> str:
    """
    Indent every line after the first by ``width`` spaces, so a multi-line
    text stays inside the list item or table cell it starts in.

    :param force: if False, text whose continuation lines are all indented by
        at least ``width`` already is returned unchanged, so callers that
        indented their strings by hand keep the same output.
    """
    lines = text.split("\n")
    rest = lines[1:]
    if not force:
        is_indented = all(
            (not line.strip()) or (len(line) - len(line.lstrip(" ")) >= width)
            for line in rest
        )
        if is_indented:
            return text
    prefix = " " * width
    return "\n".join([lines[0]] + [_indent_line(line, prefix) for line in rest])


@dataclass(kw_only=True)
class RstObj:
    """
    The base restructured text object.
    """

    @property
    def template_name(self) -> str:
        """
        Find template file.
        """
        return "{}.{}.rst".format(self.__module__, self.__class__.__name__)

    @property
    def template(self) -> Template:
        """
        Return ``jinja2.Template`` instance.
        """
        return env.get_template(self.template_name)

    def render(
        self,
        indent: int | None = None,
        first_line_indent: int | None = None,
        **kwargs,
    ) -> str:
        """
        Render this object into text.

        :param indent: global indent. Indent length can be changed in
            :attr:`rstobj.option.Options.tab`.

        :param first_line_indent: sometimes we only need to indent
            first line, this option will overwrite the ``indent`` argument.

        :param kwargs: other optional arguments.
        """
        out = self.template.render(obj=self, tab=Options.tab)
        if indent or first_line_indent:
            origin_lines = out.split("\n")
            target_lines = [
                _indent_line(line, Options.tab * (indent or 0)) for line in origin_lines
            ]
            if first_line_indent is not None:
                if first_line_indent >= 0:
                    target_lines[0] = _indent_line(
                        origin_lines[0],
                        Options.tab * first_line_indent,
                    )
                else:  # pragma: no cover
                    raise TypeError
            out = "\n".join(target_lines)
        return out

    @staticmethod
    def str_or_render(
        value: str | RstObj,
        **kwargs,
    ) -> str:
        """
        If it is a string type, then just return. If it is a RstObj type,
        then return the rendered string.
        """
        if isinstance(value, RstObj):
            return value.render(**kwargs)
        else:
            return str(value)

    @staticmethod
    def _render_nested(
        value: str | RstObj,
        width: int,
    ) -> str:
        """
        Render a list item or table cell whose text starts after a marker
        ``width`` characters wide, such as ``"- "`` or ``"    * - "``.

        A :class:`RstObj` is rendered without its leading and trailing blank
        lines, and all its continuation lines are indented. A string is taken
        as reStructuredText; its continuation lines are indented unless they
        already are.
        """
        if isinstance(value, RstObj):
            text = value.render().strip("\n")
            return _indent_continuation(text, width, force=True)
        else:
            return _indent_continuation(str(value), width, force=False)
