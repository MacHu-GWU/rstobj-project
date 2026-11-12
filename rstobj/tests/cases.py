# -*- coding: utf-8 -*-

"""
Rendering cases: the single source of truth for both the tests and the
"Rendering Gallery" docs page.

Each case is a small function that builds rstobj objects and returns the
rendered reStructuredText. For every case:

- the unit tests compare the output byte for byte with
  ``rstobj/tests/snapshots/<case.id>.rst``, and check that docutils parses it
  without any warning;
- the docs show the function body, the exact snapshot text, and (for
  ``live`` cases) the snapshot rendered by Sphinx.

To regenerate the snapshots after an intended output change, run the tests
with ``RSTOBJ_UPDATE_SNAPSHOTS=1``, then review the diff in git.
"""

from __future__ import annotations

import typing as T
import os
import inspect
import textwrap
import dataclasses
from pathlib import Path

from ..directives.codeblock import Code
from ..directives.codeblock import CodeBlock
from ..directives.codeblock import CodeBlockEmpty
from ..directives.codeblock import CodeBlockPython
from ..directives.image import Image
from ..directives.miscellaneous import Include
from ..directives.table import ListTable
from ..directives.toc import TableOfContent
from ..markup.bullet_list import BulletList
from ..markup.enum_list import EnumList
from ..markup.header import Header
from ..markup.header import Header1
from ..markup.header import Header2
from ..markup.header import Header3
from ..markup.header import Header4
from ..markup.header import Header5
from ..markup.header import Header6
from ..markup.header import Header7
from ..markup.hyperlink import URI
from ..markup.hyperlink import Reference
from .rst_check import assert_valid_rst

#: Folder of the expected outputs, one ``<case.id>.rst`` file per case.
DIR_SNAPSHOTS = Path(__file__).absolute().parent / "snapshots"

#: Set this environment variable to ``1`` to rewrite the snapshots.
ENV_UPDATE_SNAPSHOTS = "RSTOBJ_UPDATE_SNAPSHOTS"


@dataclasses.dataclass(frozen=True)
class Case:
    """
    One rendering case.
    """

    # fmt: off
    func: T.Callable[[], str]  #: Builds the objects and returns the rendered text.
    module: str  #: The rstobj module under test, such as ``rstobj.directives.table``.
    title: str  #: One line shown as the heading in the docs gallery.
    gallery: bool = True  #: Show this case in the docs gallery.
    live: bool = True  #: Also render the output in the docs (False for headers, toc, include).
    # fmt: on

    @property
    def id(self) -> str:
        """
        Unique id, also the snapshot file name, such as
        ``directives.table.list_table_with_header``.
        """
        return f"{self.module.removeprefix('rstobj.')}.{self.func.__name__}"

    @property
    def path_snapshot(self) -> Path:
        """
        The expected output file.
        """
        return DIR_SNAPSHOTS / f"{self.id}.rst"

    @property
    def code(self) -> str:
        """
        The body of the case function, as a user would write it: the last
        ``return <expr>`` becomes ``rst = <expr>``.
        """
        lines = inspect.getsource(self.func).splitlines()
        body_start = next(
            i for i, line in enumerate(lines) if line.lstrip().startswith("def ")
        )
        body = textwrap.dedent("\n".join(lines[body_start + 1 :])).strip("\n")
        body_lines = body.split("\n")
        last_return = max(
            i for i, line in enumerate(body_lines) if line.startswith("return ")
        )
        body_lines[last_return] = "rst = " + body_lines[last_return][len("return ") :]
        return "\n".join(body_lines)

    def render(self) -> str:
        """
        Run the case and return the rendered text.
        """
        return self.func()

    def read_snapshot(self) -> str:
        """
        Return the expected output.
        """
        return self.path_snapshot.read_text(encoding="utf-8")

    def check(self):
        """
        Assert that the output equals the snapshot exactly and is valid
        reStructuredText.
        """
        rst = self.render()
        if os.environ.get(ENV_UPDATE_SNAPSHOTS) == "1":
            self.path_snapshot.write_text(rst, encoding="utf-8")
        assert self.path_snapshot.exists(), (
            f"missing snapshot {self.path_snapshot}, "
            f"run the tests with {ENV_UPDATE_SNAPSHOTS}=1 to create it"
        )
        assert rst == self.read_snapshot(), (
            f"output of case {self.id!r} differs from {self.path_snapshot.name}:\n"
            f"{rst!r}\n!=\n{self.read_snapshot()!r}"
        )
        assert_valid_rst(rst, source_path=self.path_snapshot)


CASES: list[Case] = []


def case(
    module: str,
    title: str,
    gallery: bool = True,
    live: bool = True,
):
    """
    Register the decorated function as a :class:`Case`.
    """

    def decorator(func: T.Callable[[], str]) -> T.Callable[[], str]:
        CASES.append(
            Case(
                func=func,
                module=module,
                title=title,
                gallery=gallery,
                live=live,
            )
        )
        return func

    return decorator


def cases_for(module: str) -> list[Case]:
    """
    Return the cases of one module, for ``pytest.mark.parametrize``.
    """
    return [c for c in CASES if c.module == module]


USER_CLASS = """
class User:
    def __init__(self, id, name):
        self.id = id

        self.name = name
""".strip()

# ------------------------------------------------------------------------------
# rstobj.directives.codeblock
# ------------------------------------------------------------------------------
M_CODEBLOCK = "rstobj.directives.codeblock"


@case(M_CODEBLOCK, "Plain code text, indented", gallery=False)
def code_indented():
    code = Code(text=USER_CLASS)
    return code.render(indent=1)


@case(M_CODEBLOCK, "Literal block (``::``)")
def literal_block():
    block = CodeBlockEmpty(code=Code(text=USER_CLASS))
    return block.render()


@case(M_CODEBLOCK, "Literal block, indented one level", gallery=False)
def literal_block_indented():
    block = CodeBlockEmpty.from_string(USER_CLASS)
    return block.render(indent=1)


@case(M_CODEBLOCK, "Code block without a language")
def code_block_no_language():
    block = CodeBlock(code=Code(text=USER_CLASS))
    return block.render()


@case(M_CODEBLOCK, "Python code block")
def code_block_python():
    block = CodeBlockPython.from_string(USER_CLASS)
    return block.render()


@case(M_CODEBLOCK, "Code block with ``:class:`` and ``:name:``")
def code_block_with_class_and_name():
    block = CodeBlockPython(
        code=Code(text="print('Hello World!')"),
        class_="my-code",
        name="hello-world-code",
    )
    return block.render()


# ------------------------------------------------------------------------------
# rstobj.directives.image
# ------------------------------------------------------------------------------
M_IMAGE = "rstobj.directives.image"
PYTHON_LOGO = "https://www.python.org/static/img/python-logo.png"


@case(M_IMAGE, "Image with only a URI")
def image_uri_only():
    image = Image(uri=PYTHON_LOGO)
    return image.render()


@case(M_IMAGE, "Image with every option")
def image_with_everything():
    image = Image(
        uri=PYTHON_LOGO,
        height=82,
        width=290,
        alt_text="Python Logo",
        align=Image.AlignOptions.center,
        class_="my-image",
        name="python-logo",
    )
    return image.render()


# ``:scale:`` needs the image size, so this case uses a local file; the path is
# relative to the docs gallery page.
@case(M_IMAGE, "Image scaled to 50%")
def image_with_scale():
    image = Image(uri="../_static/rstobj-logo.png", scale=50)
    return image.render()


@case(M_IMAGE, "Image, indented one level", gallery=False)
def image_indented():
    image = Image(uri=PYTHON_LOGO, alt_text="")
    return image.render(indent=1)


# ------------------------------------------------------------------------------
# rstobj.directives.miscellaneous
# ------------------------------------------------------------------------------
M_MISC = "rstobj.directives.miscellaneous"

# ``include-me.txt`` lives next to the snapshots, so the include paths resolve
# when the tests parse the output.


@case(M_MISC, "Include a file", live=False)
def include_file():
    include = Include(path="include-me.txt")
    return include.render()


@case(M_MISC, "Include a range of lines", live=False)
def include_line_range():
    include = Include(path="include-me.txt", start_line=2, end_line=4)
    return include.render()


@case(M_MISC, "Include the text between two markers", live=False)
def include_between_markers():
    include = Include(
        path="include-me.txt",
        start_after="Line 1",
        end_before="Line 5",
    )
    return include.render()


@case(M_MISC, "Include a file as a numbered literal block", live=False)
def include_as_literal():
    include = Include(
        path="include-me.txt",
        literal=True,
        number_lines=1,
        encoding="utf-8",
        tab_width=4,
    )
    return include.render()


@case(M_MISC, "Include a file as highlighted code", live=False)
def include_as_code():
    include = Include(path="include-me.txt", code="text")
    return include.render()


@case(M_MISC, "``literal=False`` adds no option", gallery=False)
def include_literal_false():
    include = Include(path="include-me.txt", literal=False)
    return include.render()


# ------------------------------------------------------------------------------
# rstobj.directives.table
# ------------------------------------------------------------------------------
M_TABLE = "rstobj.directives.table"


@case(M_TABLE, "Table with a header row")
def list_table_with_header():
    table = ListTable(
        data=[["id", "name"], [1, "Alice"], [2, "Bob"]],
        title="Users",
        header=True,
    )
    return table.render()


@case(M_TABLE, "Table with an index column and no header")
def list_table_with_index():
    table = ListTable(
        data=[["2015-01-01", 100], ["2015-01-02", 105], ["2015-01-03", 97]],
        title="Price",
        index=True,
        header=False,
    )
    return table.render()


@case(M_TABLE, "Table with column widths, alignment, class and name")
def list_table_with_widths():
    table = ListTable(
        data=[
            ["date", "message"],
            ["2015-01-01", "this is a very long sentence"],
            ["2015-01-02", "this is a very long sentence"],
        ],
        title="Daily Message",
        widths=[20, 80],
        align=ListTable.AlignOptions.center,
        class_="my-table",
        name="daily-message",
    )
    return table.render()


@case(M_TABLE, "Table with code blocks in its cells")
def list_table_with_codeblock():
    code = "from __future__ import print_function\n\nprint('Hello World!')"
    table = ListTable(
        data=[
            ["lang", "example"],
            ["python2", CodeBlock(code=Code(text=code))],
            ["python3", CodeBlockPython(code=Code(text=code))],
        ],
        title="Hello World Examples",
    )
    return table.render()


@case(M_TABLE, "Table with code blocks, indented one level", gallery=False)
def list_table_with_codeblock_indented():
    code = "from __future__ import print_function\n\nprint('Hello World!')"
    table = ListTable(
        data=[
            ["lang", "example"],
            ["python2", CodeBlock(code=Code(text=code))],
        ],
        title="Hello World Examples",
    )
    return table.render(indent=1)


@case(M_TABLE, "Table with multi-line text and lists in its cells")
def list_table_with_multiline_cells():
    table = ListTable(
        data=[
            ["topic", "notes"],
            ["multi-line text", "first paragraph\n\nsecond paragraph"],
            ["nested list", BulletList(items=["apple", "banana"])],
        ],
    )
    return table.render()


@case(M_TABLE, "An empty ``widths`` list adds no option", gallery=False)
def list_table_with_empty_widths():
    table = ListTable(data=[["id"], [1]], widths=[])
    return table.render()


# ------------------------------------------------------------------------------
# rstobj.directives.toc
# ------------------------------------------------------------------------------
M_TOC = "rstobj.directives.toc"


@case(M_TOC, "Table of contents without options", live=False)
def toc_basic():
    toc = TableOfContent()
    return toc.render()


@case(M_TOC, "Table of contents with every option", live=False)
def toc_with_everything():
    toc = TableOfContent(
        title="Table of Content",
        depth=1,
        backlinks=TableOfContent.BacklinksOptions.top,
        local=True,
        class_="my-toc",
    )
    return toc.render()


@case(M_TOC, "``name`` is not rendered: ``contents`` has no such option", gallery=False)
def toc_ignores_name():
    toc = TableOfContent(name="my-toc")
    return toc.render()


# ------------------------------------------------------------------------------
# rstobj.markup.bullet_list
# ------------------------------------------------------------------------------
M_BULLET = "rstobj.markup.bullet_list"


@case(M_BULLET, "Bullet list")
def bullet_list_basic():
    blist = BulletList(items=["a", "b", "c"])
    return blist.render()


@case(M_BULLET, "Bullet list with multi-line items")
def bullet_list_multiline_items():
    blist = BulletList(items=["line 1\nline 2", "paragraph 1\n\nparagraph 2"])
    return blist.render()


@case(M_BULLET, "Nested bullet list and a code block in a list")
def bullet_list_nested():
    blist = BulletList(
        items=[
            "fruits",
            BulletList(items=["apple", "banana"]),
            CodeBlockPython.from_string("print('Hello World!')"),
        ]
    )
    return blist.render()


@case(M_BULLET, "Already indented continuation lines are kept", gallery=False)
def bullet_list_pre_indented_item():
    blist = BulletList(items=["line 1\n  line 2"])
    return blist.render()


# ------------------------------------------------------------------------------
# rstobj.markup.enum_list
# ------------------------------------------------------------------------------
M_ENUM = "rstobj.markup.enum_list"


@case(M_ENUM, "Enumerated list starting at 3")
def enum_list_basic():
    elist = EnumList(items=["a", "b", "c"], start_num=3)
    return elist.render()


@case(M_ENUM, "Enumerated list with multi-line and nested items")
def enum_list_nested():
    elist = EnumList(
        items=[
            "line 1\nline 2",
            EnumList(items=["x", "y"]),
            "the marker of this item is wider\nand the text still lines up",
        ],
        start_num=9,
    )
    return elist.render()


# ------------------------------------------------------------------------------
# rstobj.markup.header
# ------------------------------------------------------------------------------
M_HEADER = "rstobj.markup.header"


@case(M_HEADER, "Header with a fixed bar length", live=False)
def header_fixed_bar():
    header = Header(title="Section 1", header_level=1, bar_length=80)
    return header.render()


@case(M_HEADER, "Header with an automatic bar length", live=False)
def header_auto_bar():
    header = Header(title="Section 1", header_level=1)
    return header.render()


@case(M_HEADER, "Header with a reference label", live=False)
def header_with_ref_label():
    header = Header(title="Section 1", header_level=1, ref_label="section_1")
    return header.render()


@case(M_HEADER, "Level 2 header with a reference label", live=False)
def header2_with_ref_label():
    header = Header2(title="Section 1.1", ref_label="section_1_1")
    return header.render()


@case(M_HEADER, "Level 2 header with an automatic label", live=False)
def header2_auto_label():
    header = Header2(title="Section 2", auto_label=True)
    return header.render()


@case(M_HEADER, "Every header level", live=False)
def header_all_levels():
    headers = [
        Header1(title="Level 1"),
        Header2(title="Level 2"),
        Header3(title="Level 3"),
        Header4(title="Level 4"),
        Header5(title="Level 5"),
        Header6(title="Level 6"),
        Header7(title="Level 7"),
    ]
    return "\n".join(header.render() for header in headers)


@case(M_HEADER, "Wide (CJK and emoji) characters count twice in the bar", live=False)
def header_wide_characters():
    header = Header(title="中文标题 😀", header_level=1, auto_label=True)
    return header.render()


@case(M_HEADER, "A title that slugifies to nothing gets no label", gallery=False)
def header_empty_auto_label():
    header = Header(title="(*)", header_level=1, auto_label=True)
    return header.render()


# ------------------------------------------------------------------------------
# rstobj.markup.hyperlink
# ------------------------------------------------------------------------------
M_HYPERLINK = "rstobj.markup.hyperlink"


@case(M_HYPERLINK, "External link")
def uri_basic():
    uri = URI(title="Python Homepage", link="https://www.python.org")
    return uri.render()


@case(M_HYPERLINK, "Sphinx cross-reference to a label")
def reference_basic():
    ref = Reference(title="Release History", label="release_history")
    return ref.render()


def case_id(case: Case) -> str:
    """
    Test id for ``pytest.mark.parametrize(..., ids=case_id)``.
    """
    return case.func.__name__


def find_orphan_snapshots(module: str) -> list[str]:
    """
    Return the snapshot files of ``module`` that no case produces anymore.
    """
    prefix = module.removeprefix("rstobj.") + "."
    expected = {c.path_snapshot.name for c in cases_for(module)}
    return sorted(
        path.name
        for path in DIR_SNAPSHOTS.glob(f"{prefix}*.rst")
        if path.name not in expected
    )
