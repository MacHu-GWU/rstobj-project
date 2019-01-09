# -*- coding: utf-8 -*-

import pytest
from rstobj.markup.hyperlink import URI, Reference


class TestURI(object):
    def test(self):
        obj = URI(title="Python Homepage", link="https://www.python.org")
        rst = obj.render()
        assert rst == "`Python Homepage <https://www.python.org>`_"


class TestReference(object):
    def test(self):
        obj = Reference(title="Section1", label="section1")
        rst = obj.render()
        assert rst == ":ref:`Section1 <section1>`"


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
