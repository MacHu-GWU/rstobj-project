#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
from pytest import raises, approx
from rstobj.tests import compare_with
from rstobj.directives.table import ListTable


class TestListTable(object):
    def test_with_header(self):
        ltable = ListTable(
            data=[["id", "name"], [1, "Alice"], [2, "Bob"]],
            title="Users",
            header=True,
        )
        rst = ltable.render()
        compare_with(rst, "rstobj.directives.table.ListTable.with-header.rst")

    def test_with_index(self):
        ltable = ListTable(
            data=[["2015-01-01", 100], ["2015-01-02", 105], ["2015-01-03", 97]],
            title="Price",
            index=True,
            header=False,
        )
        rst = ltable.render()
        compare_with(rst, "rstobj.directives.table.ListTable.with-index.rst")


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
