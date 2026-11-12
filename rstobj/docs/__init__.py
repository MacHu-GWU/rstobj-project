# -*- coding: utf-8 -*-

"""
Data passed to the ``.. jinja:: doc_data`` directive in the docs
(see ``jinja_contexts`` in ``docs/source/conf.py``).

``doc_data["gallery_rst"]`` is the body of the "Rendering Gallery" page. It is
built from the same cases the unit tests check (:mod:`rstobj.tests.cases`),
with rstobj itself.
"""

import os

from ..directives.codeblock import CodeBlockPython
from ..directives.codeblock import CodeBlockRst
from ..markup.header import Header2
from ..markup.header import Header3
from ..paths import path_enum
from ..tests.cases import CASES
from ..tests.cases import Case

#: The folder of the gallery page; include paths are relative to it.
DIR_GALLERY_PAGE = path_enum.dir_docs_source / "01-Rendering-Gallery"

#: Module of the cases -> section title, in page order.
GROUP_TITLES = {
    "rstobj.markup.header": "Headers",
    "rstobj.markup.hyperlink": "Links and References",
    "rstobj.markup.bullet_list": "Bullet Lists",
    "rstobj.markup.enum_list": "Enumerated Lists",
    "rstobj.directives.codeblock": "Code Blocks",
    "rstobj.directives.image": "Images",
    "rstobj.directives.table": "List Tables",
    "rstobj.directives.toc": "Table of Contents",
    "rstobj.directives.miscellaneous": "Include",
}

BAR_LENGTH = 78

NOT_LIVE_NOTE = (
    "*Not rendered on this page: a header, a table of contents, or an "
    "include would change the structure of the page itself.*"
)


def _render_case(case: Case) -> str:
    """
    Python code, the exact output (the snapshot), and the output rendered by
    Sphinx.
    """
    parts = [
        Header3(title=case.title, bar_length=BAR_LENGTH).render().strip("\n"),
        "**Python**",
        CodeBlockPython.from_string(case.code).render(),
        "**reStructuredText**",
        CodeBlockRst.from_string(case.read_snapshot().strip("\n")).render(),
        "**Rendered**",
    ]
    if case.live:
        include_path = os.path.relpath(case.path_snapshot, DIR_GALLERY_PAGE)
        parts.append(
            f".. card::\n\n    .. include:: {include_path.replace(os.sep, '/')}"
        )
    else:
        parts.append(NOT_LIVE_NOTE)
    return "\n\n".join(parts)


def build_gallery_rst() -> str:
    """
    Return the reStructuredText body of the gallery page.
    """
    sections = []
    for module, title in GROUP_TITLES.items():
        cases = [c for c in CASES if c.module == module and c.gallery]
        if not cases:  # pragma: no cover
            continue
        sections.append(
            Header2(title=title, bar_length=BAR_LENGTH).render().strip("\n")
        )
        for case in cases:
            sections.append(_render_case(case))
    return "\n\n".join(sections) + "\n"


doc_data = {
    "gallery_rst": build_gallery_rst(),
}
