# -*- coding: utf-8 -*-

import pytest
from rstobj.tests import compare_with
from rstobj.directives.image import Image


class TestImage:
    def test(self):
        image = Image(
            uri="https://www.python.org/static/img/python-logo.png",
            width=320,
            height=320,
            alt_text="Image Not Found",
            align=Image.AlignOptions.center,
        )
        rst = image.render()
        compare_with(rst, "rstobj.directives.image.Image.with-everything.rst")

        image = Image(
            uri="https://www.python.org/static/img/python-logo.png",
        )
        rst = image.render()
        compare_with(rst, "rstobj.directives.image.Image.uri-only.rst")

    def test_render_indent(self):
        image = Image(
            uri="https://www.python.org/static/img/python-logo.png",
        )
        rst = image.render(indent=1)
        compare_with(rst, "rstobj.directives.image.Image.render-indent.rst")


if __name__ == "__main__":
    from rstobj.tests import run_cov_test

    run_cov_test(
        __file__,
        "rstobj.directives.image",
        preview=False,
    )
