# -*- coding: utf-8 -*-

import pytest
from pytest import raises, approx


def test():
    import rstobj

    _ = rstobj.markup.URI
    _ = rstobj.markup.URL
    _ = rstobj.markup.Header
    _ = rstobj.markup.Header7
    _ = rstobj.markup.BulletList
    _ = rstobj.markup.EnumList
    _ = rstobj.directives.Image
    _ = rstobj.directives.ListTable
    _ = rstobj.directives.CodeBlock
    _ = rstobj.directives.CodeBlockEmpty
    _ = rstobj.directives.CodeBlockPython


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
