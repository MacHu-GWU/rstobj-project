# -*- coding: utf-8 -*-

import pytest

from rstobj.tests.cases import cases_for
from rstobj.tests.cases import case_id
from rstobj.tests.cases import find_orphan_snapshots

MODULE = "rstobj.markup.enum_list"


@pytest.mark.parametrize("case", cases_for(MODULE), ids=case_id)
def test_case(case):
    """
    The output equals its snapshot byte for byte, and docutils parses it
    without a warning.
    """
    case.check()


def test_no_orphan_snapshots():
    assert find_orphan_snapshots(MODULE) == []


if __name__ == "__main__":
    from rstobj.tests import run_cov_test

    run_cov_test(
        __file__,
        "rstobj.markup.enum_list",
        preview=False,
    )
