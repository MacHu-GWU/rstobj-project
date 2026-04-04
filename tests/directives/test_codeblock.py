# -*- coding: utf-8 -*-

from rstobj.tests import compare_with
from rstobj.directives.codeblock import (
    Code,
    CodeBlockEmpty,
    CodeBlock,
    CodeBlockPython,
)

cb_user_class = """
class User(object):
    def __init__(self, id, name):
        self.id = id
        self.name = name
""".strip()


class TestCode:
    def test_render_indent(self):
        code = Code(text=cb_user_class)
        rst = code.render(indent=1)
        compare_with(rst, "rstobj.directives.codeblock.Code.render-indent.rst")


class TestCodeBlockEmpty:
    def test_render(self):
        cb = CodeBlockEmpty(code=Code(text=cb_user_class))
        rst = cb.render()
        compare_with(rst, "rstobj.directives.codeblock.CodeBlockEmpty.render.rst")

        rst = cb.render(indent=1)
        compare_with(
            rst, "rstobj.directives.codeblock.CodeBlockEmpty.render-indent.rst"
        )


class TestCodeBlock:
    def test_render(self):
        cb = CodeBlock(code=Code(text=cb_user_class))
        rst = cb.render()
        compare_with(rst, "rstobj.directives.codeblock.CodeBlock.render.rst")


class TestCodeBlockPython:
    def test_render(self):
        cb = CodeBlockPython.from_string(cb_user_class)
        rst = cb.render()
        compare_with(rst, "rstobj.directives.codeblock.CodeBlockPython.render.rst")


if __name__ == "__main__":
    from rstobj.tests import run_cov_test

    run_cov_test(
        __file__,
        "rstobj.directives.codeblock",
        preview=False,
    )
