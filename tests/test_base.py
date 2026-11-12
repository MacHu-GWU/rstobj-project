# -*- coding: utf-8 -*-

from rstobj.base import RstObj
from rstobj.base import _indent_line
from rstobj.base import _indent_continuation

import pytest

from jinja2.exceptions import UndefinedError

from rstobj.directives.codeblock import Code
from rstobj.markup.bullet_list import BulletList
from rstobj.templates import env


class TestRender:
    def test_no_indent_returns_template_output(self):
        assert Code(text="a  \n\nb").render() == "a  \n\nb"

    def test_indent(self):
        assert Code(text="a\nb").render(indent=1) == "    a\n    b"

    def test_indent_keeps_blank_lines_empty(self):
        assert Code(text="a\n\nb").render(indent=2) == "        a\n\n        b"

    def test_first_line_indent(self):
        rst = Code(text="a\nb").render(indent=2, first_line_indent=0)
        assert rst == "a\n        b"

    def test_first_line_indent_without_indent(self):
        assert Code(text="a\nb").render(first_line_indent=1) == "    a\nb"

    def test_negative_first_line_indent(self):
        with pytest.raises(TypeError):
            Code(text="a").render(indent=1, first_line_indent=-1)


def test_str_or_render():
    assert RstObj.str_or_render("a") == "a"
    assert RstObj.str_or_render(1) == "1"
    assert RstObj.str_or_render(Code(text="a"), indent=1) == "    a"


class TestRenderNested:
    def test_string(self):
        assert RstObj._render_nested("a\nb", width=2) == "a\n  b"

    def test_string_already_indented(self):
        assert RstObj._render_nested("a\n    b", width=2) == "a\n    b"

    def test_rst_obj_drops_outer_blank_lines(self):
        rst = RstObj._render_nested(BulletList(items=["x", "y"]), width=2)
        assert rst == "- x\n  - y"


def test_indent_line():
    assert _indent_line("a  ", "  ") == "  a"
    assert _indent_line("   ", "  ") == ""


def test_indent_continuation():
    assert _indent_continuation("a", 4, force=True) == "a"
    assert _indent_continuation("a\n\nb", 2, force=False) == "a\n\n  b"
    assert _indent_continuation("a\n  b", 2, force=False) == "a\n  b"
    assert _indent_continuation("a\n  b", 2, force=True) == "a\n    b"


def test_template_typo_raises():
    """
    The jinja2 environment uses StrictUndefined, so a typo in a template
    fails loudly instead of rendering an empty string.
    """
    template = env.from_string("{{ obj.no_such_attribute }}")
    with pytest.raises(UndefinedError):
        template.render(obj=Code(text="a"))


if __name__ == "__main__":
    from rstobj.tests import run_cov_test

    run_cov_test(
        __file__,
        "rstobj.base",
        preview=False,
    )
