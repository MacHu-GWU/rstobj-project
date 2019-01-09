# -*- coding: utf-8 -*-

import pytest
from rstobj.tests import compare_with
from rstobj.directives.toc import TableOfContent


class TestTableOfContent(object):
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
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
