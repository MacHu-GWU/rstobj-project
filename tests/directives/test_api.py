# -*- coding: utf-8 -*-

from rstobj.directives import api


def test():
    _ = api
    _ = api.Image
    _ = api.ListTable
    _ = api.Code
    _ = api.CodeBlockEmpty
    _ = api.CodeBlockBase
    _ = api.CodeBlock
    _ = api.CodeBlockPython
    _ = api.CodeBlockRuby
    _ = api.CodeBlockR
    _ = api.CodeBlockPerl
    _ = api.CodeBlockC
    _ = api.CodeBlockCPP
    _ = api.CodeBlockHTML
    _ = api.CodeBlockCSS
    _ = api.CodeBlockJavaScript
    _ = api.CodeBlockSQL
    _ = api.CodeBlockScala
    _ = api.CodeBlockMake
    _ = api.CodeBlockBash
    _ = api.CodeBlockLua
    _ = api.CodeBlockRst
    _ = api.CodeBlockMarkdown
    _ = api.TableOfContent
    _ = api.Include


if __name__ == "__main__":
    from rstobj.tests import run_cov_test

    run_cov_test(
        __file__,
        "rstobj.directives.api",
        preview=False,
    )
