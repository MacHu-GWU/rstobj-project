#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
from rstobj.markup.hyperlink import URI


class TestURI(object):
    def test(self):
        obj = URI(title="Python Homepage", link="https://www.python.org")
        rst = obj.render()
        assert rst == "`Python Homepage <https://www.python.org>`_"


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
