# -*- coding: utf-8 -*-

import pytest
from rstobj.tests import compare_with
from rstobj.markup.bullet_list import BulletList


class TestBulletList(object):
    def test(self):
        obj = BulletList(items="a,b,c".split(","))
        rst = obj.render()
        compare_with(rst, "rstobj.markup.bullet_list.BulletList.render.rst")


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
