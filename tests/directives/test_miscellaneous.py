# -*- coding: utf-8 -*-

import pytest
from rstobj.tests import compare_with
from rstobj.directives.miscellaneous import Include


class TestInclude:
    def test(self):
        include = Include(
            path="README.rst",
        )
        rst = include.render()
        compare_with(rst, "rstobj.directives.miscellaneous.Include.render.rst")


if __name__ == "__main__":
    from rstobj.tests import run_cov_test

    run_cov_test(
        __file__,
        "rstobj.directives.miscellaneous",
        preview=False,
    )
