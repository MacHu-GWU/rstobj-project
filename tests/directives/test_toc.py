# -*- coding: utf-8 -*-

import pytest
from rstobj.tests import compare_with
from rstobj.directives.toc import TableOfContent


class TestTableOfContent:
    def test(self):
        toc = TableOfContent()
        rst = toc.render()
        compare_with(rst, "rstobj.directives.toc.TableOfContent.basic.rst")

        toc = TableOfContent(
            title="Table of Content",
            depth=1,
            backlinks=TableOfContent.BacklinksOptions.top,
            local=True,
        )
        rst = toc.render()
        compare_with(
            rst, "rstobj.directives.toc.TableOfContent.rich-options.rst")


if __name__ == "__main__":
    from rstobj.tests import run_cov_test

    run_cov_test(
        __file__,
        "rstobj.directives.toc",
        preview=False,
    )
