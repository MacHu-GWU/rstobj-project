#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
from rstobj.tests import compare_with
from rstobj.directives.miscellaneous import Include


class TestInclude(object):
    def test(self):
        include = Include(
            path="README.rst",
        )
        rst = include.render()
        compare_with(rst, "rstobj.directives.miscellaneous.Include.render.rst")


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
