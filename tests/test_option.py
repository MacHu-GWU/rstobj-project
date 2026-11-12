# -*- coding: utf-8 -*-

from rstobj.option import Options

import pytest

from rstobj.directives.codeblock import CodeBlockPython
from rstobj.directives.table import ListTable
from rstobj.tests.rst_check import assert_valid_rst


@pytest.fixture
def two_space_tab():
    original = Options.tab
    Options.tab = "  "
    yield
    Options.tab = original


def test_tab_changes_every_indent(two_space_tab):
    """
    Changing Options.tab changes the directive option indent and the nested
    content indent together, so the output stays valid.
    """
    table = ListTable(
        data=[["lang", "code"], ["python", CodeBlockPython.from_string("x = 1")]],
        title="Code",
    )
    rst = table.render()
    assert rst == (
        ".. list-table:: Code\n"
        "  :header-rows: 1\n"
        "  :stub-columns: 0\n"
        "\n"
        "  * - lang\n"
        "    - code\n"
        "  * - python\n"
        "    - .. code-block:: python\n"
        "\n"
        "        x = 1\n"
    )
    assert_valid_rst(rst)


if __name__ == "__main__":
    from rstobj.tests import run_cov_test

    run_cov_test(
        __file__,
        "rstobj.option",
        preview=False,
    )
