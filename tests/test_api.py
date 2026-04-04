# -*- coding: utf-8 -*-

from rstobj import api


def test():
    _ = api
    _ = api.markup
    _ = api.directives


if __name__ == "__main__":
    from rstobj.tests import run_cov_test

    run_cov_test(
        __file__,
        "rstobj.api",
        preview=False,
    )
