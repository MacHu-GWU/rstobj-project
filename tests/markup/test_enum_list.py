# -*- coding: utf-8 -*-

import pytest
from rstobj.tests import compare_with
from rstobj.markup.enum_list import EnumList


class TestEnumList(object):
    def test(self):
        obj = EnumList(items="a,b,c".split(","), start_num=3)
        rst = obj.render()
        compare_with(rst, "rstobj.markup.enum_list.EnumList.render.rst")


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
