# -*- coding: utf-8 -*-

from rstobj import api


def test():
    _ = api
    _ = api.markup.URI
    _ = api.markup.URL
    _ = api.markup.Header
    _ = api.markup.Header7
    _ = api.markup.BulletList
    _ = api.markup.EnumList
    _ = api.directives.Image
    _ = api.directives.ListTable
    _ = api.directives.CodeBlock
    _ = api.directives.CodeBlockEmpty
    _ = api.directives.CodeBlockPython


if __name__ == "__main__":
    from rstobj.tests import run_cov_test

    run_cov_test(
        __file__,
        "rstobj.api",
        preview=False,
    )
