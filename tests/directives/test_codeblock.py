#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
from rstobj.tests import compare_with
from rstobj.directives.codeblock import (
    Code, CodeBlockEmpty,
    CodeBlock, CodeBlockPython,
)

cb_user_class = """
class User(object):
    def __init__(self, id, name):
        self.id = id
        self.name = name
""".strip()


class TestCode(object):
    def test_render_indent(self):
        code = Code(cb_user_class)
        rst = code.render(indent=1)
        compare_with(rst, "rstobj.directives.codeblock.Code.render-indent.rst")


class TestCodeBlockEmpty(object):
    def test_render(self):
        cb = CodeBlockEmpty(code=Code(cb_user_class))
        rst = cb.render()
        compare_with(
            rst, "rstobj.directives.codeblock.CodeBlockEmpty.render.rst")

        rst = cb.render(indent=1)
        compare_with(
            rst, "rstobj.directives.codeblock.CodeBlockEmpty.render-indent.rst")


class TestCodeBlock(object):
    def test_render(self):
        cb = CodeBlock(code=Code(cb_user_class))
        rst = cb.render()
        compare_with(rst, "rstobj.directives.codeblock.CodeBlock.render.rst")


class TestCodeBlockPython(object):
    def test_render(self):
        cb = CodeBlockPython(code=Code(cb_user_class))
        rst = cb.render()
        compare_with(
            rst, "rstobj.directives.codeblock.CodeBlockPython.render.rst")


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
