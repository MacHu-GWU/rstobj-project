# -*- coding: utf-8 -*-

from rstobj.directives.base import Directive

from rstobj.directives.image import Image
from rstobj.directives.toc import TableOfContent


def test_meta_supports_name():
    assert Directive.meta_supports_name is True
    assert Image.meta_supports_name is True
    assert TableOfContent.meta_supports_name is False


def test_class_and_name_options():
    rst = Image(uri="a.png", class_="my-class", name="my-name").render()
    assert rst == ".. image:: a.png\n    :class: my-class\n    :name: my-name\n"


if __name__ == "__main__":
    from rstobj.tests import run_cov_test

    run_cov_test(
        __file__,
        "rstobj.directives.base",
        preview=False,
    )
