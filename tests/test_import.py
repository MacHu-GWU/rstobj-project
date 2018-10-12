#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
from pytest import raises, approx


def test():
    import rstobj
    rstobj.markup.URI
    rstobj.markup.URL
    rstobj.markup.Header
    rstobj.markup.Header7
    rstobj.directives.Image
    rstobj.directives.ListTable


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
