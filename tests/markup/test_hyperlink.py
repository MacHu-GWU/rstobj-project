# -*- coding: utf-8 -*-

import pytest
from rstobj.markup.hyperlink import URI, Reference


class TestURI:
    def test(self):
        obj = URI(title="Python Homepage", link="https://www.python.org")
        rst = obj.render()
        assert rst == "`Python Homepage <https://www.python.org>`_"


class TestReference:
    def test(self):
        obj = Reference(title="Section1", label="section1")
        rst = obj.render()
        assert rst == ":ref:`Section1 <section1>`"


if __name__ == "__main__":
    from rstobj.tests import run_cov_test

    run_cov_test(
        __file__,
        "rstobj.markup.hyperlink",
        preview=False,
    )
