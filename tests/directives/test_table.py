# -*- coding: utf-8 -*-

import pytest
from rstobj.tests import compare_with
from rstobj.directives.table import ListTable
from rstobj.directives.codeblock import Code, CodeBlock


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

    def test_with_widths(self):
        ltable = ListTable(
            data=[
                ["2015-01-01", "this is very long sentence"],
                ["2015-01-02", "this is very long sentence"],
                ["2015-01-03", "this is very long sentence"],
            ],
            title="Daily Message",
            widths=[20, 80],
        )
        rst = ltable.render()
        compare_with(rst, "rstobj.directives.table.ListTable.with-widths.rst")

    def test_with_codeblock(self):
        ltable = ListTable(
            data=[
                [
                    "lang",
                    "example"
                ],
                [
                    "python2",
                    CodeBlock(
                        code=Code("from __future__ import print_function\n\nprint('Hello World!')")
                    )
                ],
                [
                    "python3",
                    CodeBlock(
                        code=Code("from __future__ import print_function\n\nprint('Hello World!')")
                    )
                ]
            ],
            title="Hello World Examples",
            index=False,
            header=True,
        )
        rst = ltable.render()
        compare_with(rst, "rstobj.directives.table.ListTable.with-codeblock.rst")

        rst = ltable.render(indent=1)
        compare_with(rst, "rstobj.directives.table.ListTable.with-codeblock-indent.rst")


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
