# -*- coding: utf-8 -*-

import pytest

from rstobj.tests.cases import cases_for
from rstobj.tests.cases import case_id
from rstobj.tests.cases import find_orphan_snapshots

from rstobj.markup.header import Header
from rstobj.markup.header import _display_width
from rstobj.markup.header import to_label

MODULE = "rstobj.markup.header"


@pytest.mark.parametrize("case", cases_for(MODULE), ids=case_id)
def test_case(case):
    """
    The output equals its snapshot byte for byte, and docutils parses it
    without a warning.
    """
    case.check()


def test_no_orphan_snapshots():
    assert find_orphan_snapshots(MODULE) == []


class TestHeader:
    def test_header_level_none(self):
        with pytest.raises(ValueError):
            Header(title="Section 1", header_level=None)

    @pytest.mark.parametrize("header_level", [0, 8])
    def test_header_level_out_of_range(self, header_level):
        with pytest.raises(ValueError):
            Header(title="Section", header_level=header_level)

    def test_bar_length_shorter_than_title(self):
        header = Header(title="THIS IS A VERY LONG TITLE", bar_length=6)
        assert header.bar_length == len("THIS IS A VERY LONG TITLE")

    def test_explicit_ref_label_wins_over_auto_label(self):
        header = Header(title="Section 1", ref_label="my-label", auto_label=True)
        assert header.ref_label == "my-label"


@pytest.mark.parametrize(
    "text, width",
    [
        ("Section 1", 9),
        ("中文", 4),
        ("😀", 2),
        ("e\u0301", 1),  # e + combining acute accent
        ("", 0),
    ],
)
def test_display_width(text, width):
    assert _display_width(text) == width


@pytest.mark.parametrize(
    "title, label",
    [
        ("Hello World", "Hello-World"),
        ("  a  __  b  ", "a-b"),
        ("`code` (x)", "code-x"),
        ("(*)", ""),
    ],
)
def test_to_label(title, label):
    assert to_label(title) == label


if __name__ == "__main__":
    from rstobj.tests import run_cov_test

    run_cov_test(
        __file__,
        "rstobj.markup.header",
        preview=False,
    )
