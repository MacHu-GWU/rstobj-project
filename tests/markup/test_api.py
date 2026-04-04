# -*- coding: utf-8 -*-

from rstobj.markup import api


def test():
    _ = api
    _ = api.Header
    _ = api.Header1
    _ = api.Header2
    _ = api.Header3
    _ = api.Header4
    _ = api.Header5
    _ = api.Header6
    _ = api.Header7
    _ = api.URI
    _ = api.URL
    _ = api.Reference
    _ = api.Ref
    _ = api.BulletList
    _ = api.EnumList


if __name__ == "__main__":
    from rstobj.tests import run_cov_test

    run_cov_test(
        __file__,
        "rstobj.markup.api",
        preview=False,
    )
