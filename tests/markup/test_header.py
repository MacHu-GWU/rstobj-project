#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
from rstobj.tests import compare_with
from rstobj.markup.header import Header, Header2


class TestHeader(object):
    def test_no_ref_key(self):
        header = Header(title="Section 1", header_level=1)
        rst = header.render(bar_length=80)
        compare_with(rst, "rstobj.markup.header.Header.no-ref_key.rst")

    def test_no_ref_key_auto_bar(self):
        header = Header(title="Section 1", header_level=1)
        rst = header.render()
        compare_with(
            rst, "rstobj.markup.header.Header.no-ref_key-auto-bar.rst")

    def test_has_ref_key_auto_bar(self):
        header = Header(title="Section 1", header_level=1,
                        ref_label="section_1")
        rst = header.render()
        compare_with(
            rst, "rstobj.markup.header.Header.has-ref_key-auto-bar.rst")

    def test_raise_not_none_error(self):
        with pytest.raises(ValueError):
            Header(title="Section ")


class TestHeader2(object):
    def test_has_ref_key_auto_bar(self):
        header = Header2(title="Section 1.1", ref_label="section_1_1")
        rst = header.render()
        compare_with(
            rst, "rstobj.markup.header.Header2.has-ref_key-auto-bar.rst")

    def test_auto_label(self):
        header = Header2(title="Section 2", auto_label=True)
        rst = header.render()
        compare_with(rst, "rstobj.markup.header.Header2.auto-ref_key.rst")


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
