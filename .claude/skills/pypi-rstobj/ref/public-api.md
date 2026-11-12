# rstobj 2.0.1 Public API

Full reference for using rstobj. Import with `import rstobj.api as rstobj`; classes are `rstobj.markup.X` and `rstobj.directives.X`. Every class is a keyword-only dataclass; `obj.render(indent=None, first_line_indent=None) -> str` returns the reST (see section 1).

---

## 1. `render()` and nesting

- `render(indent=n)`: prefix every line with n tabs (4 spaces each); trailing whitespace is stripped and blank lines stay empty.
- `render(first_line_indent=m)`: the first line gets m tabs instead; useful when the text continues a line you already started.
- Inside `BulletList`, `EnumList`, and `ListTable`, an rstobj object is rendered without its leading and trailing newlines, and its continuation lines are indented under the item marker. A string is inserted as raw reST, with its continuation lines indented the same way unless they already are.
- `RstObj.str_or_render(value, **kwargs) -> str`: `value.render(**kwargs)` for an rstobj object, `str(value)` otherwise.

---

## 2. Header, Header1 ... Header7 (`rstobj.markup`)

```python
Header(title: str, header_level: int = 1, ref_label: str | None = None, auto_label: bool = False, bar_length: int | None = None)
Header1(...) ... Header7(...)   # same fields, header_level preset to 1 ... 7
```

- `header_level`: 1-7, underline characters `=`, `-`, `~`, `+`, `*`, `#`, `^`. `ValueError` otherwise, or if `None`.
- `ref_label`: adds `.. _<ref_label>:` above the title, for Sphinx `:ref:`.
- `auto_label=True`: when `ref_label` is not given, slugify the title into it (spaces and `_` `~` become `-`; ``` `*()[]{}<>"' ``` are removed; case is kept). A title that slugifies to nothing gets no label.
- `bar_length`: underline length; raised to the title's display width if shorter (CJK and emoji count as 2 columns).
- `ref_label` and `bar_length` are computed once when the object is created: changing `title` later does not update them.
- Output starts with `"\n"`.

```python
header = rstobj.markup.Header(title="Hello World", header_level=1, auto_label=True)
rst = header.render()
```

Output (`repr` shows the exact newlines):

```python
'\n.. _Hello-World:\n\nHello World\n==========='
```

Rendered text:

```rst
.. _Hello-World:

Hello World
===========
```

---

## 3. BulletList (`rstobj.markup`)

```python
BulletList(items: list)
```

- Each item is a string (raw reST), a number, or an rstobj object. Continuation lines of a multi-line string are indented to stay in the item, unless already indented that far.
- An rstobj item (nested list, code block) is rendered and indented to fit. An item holds one thing: for "text with a nested list under it", build one string.
- Output starts with `"\n"`.

```python
fruits = rstobj.markup.BulletList(items=["apple", "banana"])
blist = rstobj.markup.BulletList(
    items=[
        "fruits",
        "some title here\n\n" + fruits.render().strip("\n"),
        rstobj.directives.CodeBlockPython.from_string("print('Hello World!')"),
    ]
)
rst = blist.render()
```

Output (`repr` shows the exact newlines):

```python
"\n- fruits\n- some title here\n\n  - apple\n  - banana\n- .. code-block:: python\n\n      print('Hello World!')"
```

Rendered text:

```rst
- fruits
- some title here

  - apple
  - banana
- .. code-block:: python

      print('Hello World!')
```

---

## 4. EnumList (`rstobj.markup`)

```python
EnumList(items: list, start_num: int = 1)
```

- Same item rules as `BulletList`; continuation lines line up with each item's own marker width (`9. ` vs `10. `).
- Output starts with `"\n"`.

```python
elist = rstobj.markup.EnumList(items=["first", "second\n\nwith a second paragraph"], start_num=9)
rst = elist.render()
```

Output (`repr` shows the exact newlines):

```python
'\n9. first\n10. second\n\n    with a second paragraph'
```

Rendered text:

```rst
9. first
10. second

    with a second paragraph
```

---

## 5. URI (alias URL) (`rstobj.markup`)

```python
URI(title: str, link: str)
```

- Renders a named hyperlink reference. Two `URI`s with the same title and different links in one document make docutils warn (duplicate target name).
- The title is not escaped: a backtick in it breaks the link.

```python
uri = rstobj.markup.URI(title="Python Homepage", link="https://www.python.org")
rst = uri.render()
```

Output (`repr` shows the exact newlines):

```python
'`Python Homepage <https://www.python.org>`_'
```

Rendered text:

```rst
`Python Homepage <https://www.python.org>`_
```

---

## 6. Reference (alias Ref) (`rstobj.markup`)

```python
Reference(title: str, label: str)
```

- Sphinx's `:ref:` role; resolves only in a Sphinx build where the label exists.

```python
ref = rstobj.markup.Reference(title="Release History", label="release_history")
rst = ref.render()
```

Output (`repr` shows the exact newlines):

```python
':ref:`Release History <release_history>`'
```

Rendered text:

```rst
:ref:`Release History <release_history>`
```

---

## 7. ListTable (`rstobj.directives`)

```python
ListTable(data: list[list], title: str = "", index: bool = False, header: bool = True, widths: list[int] | None = None, align: str | None = None, class_: str | None = None, name: str | None = None)
```

- `data`: rows of cells; a cell is a string (raw reST), a number, or an rstobj object.
- `header=True` renders `:header-rows: 1`; `index=True` renders `:stub-columns: 1`.
- `widths`: one int per column; `None` or `[]` renders no `:widths:`.
- `align`: `ListTable.AlignOptions.left` / `center` / `right`; `ValueError` otherwise.
- No validation of the data shape: an empty table, rows of different lengths, or a wrong number of widths render reST that docutils rejects.
- Output ends with `"\n"`.

```python
table = rstobj.directives.ListTable(
    data=[
        ["lang", "example"],
        ["python", rstobj.directives.CodeBlockPython.from_string("print('hi')")],
    ],
    title="Examples",
    widths=[20, 80],
)
rst = table.render()
```

Output (`repr` shows the exact newlines):

```python
".. list-table:: Examples\n    :header-rows: 1\n    :stub-columns: 0\n    :widths: 20 80\n\n    * - lang\n      - example\n    * - python\n      - .. code-block:: python\n\n            print('hi')\n"
```

Rendered text:

```rst
.. list-table:: Examples
    :header-rows: 1
    :stub-columns: 0
    :widths: 20 80

    * - lang
      - example
    * - python
      - .. code-block:: python

            print('hi')
```

---

## 8. Image (`rstobj.directives`)

```python
Image(uri: str, height: int | None = None, width: int | None = None, scale: int | None = None, alt_text: str | None = None, align: str | None = None, class_: str | None = None, name: str | None = None)
```

- `height`, `width`: pixels (`320` renders `320px`). `scale`: percent (`50` renders `50%`); Sphinx needs a local image to apply it.
- `align`: `Image.AlignOptions` values; a standalone image accepts only `left`, `center`, `right` (`top`, `middle`, `bottom` are for images in substitution definitions).
- Output ends with `"\n"`.

```python
image = rstobj.directives.Image(
    uri="https://www.python.org/static/img/python-logo.png",
    width=290,
    alt_text="Python Logo",
    align=rstobj.directives.Image.AlignOptions.center,
)
rst = image.render()
```

Output (`repr` shows the exact newlines):

```python
'.. image:: https://www.python.org/static/img/python-logo.png\n    :width: 290px\n    :alt: Python Logo\n    :align: center\n'
```

Rendered text:

```rst
.. image:: https://www.python.org/static/img/python-logo.png
    :width: 290px
    :alt: Python Logo
    :align: center
```

---

## 9. Code, CodeBlock and the language code blocks (`rstobj.directives`)

```python
Code(text: str)
CodeBlock(code: Code, class_: str | None = None, name: str | None = None)
CodeBlock.from_string(text: str) -> CodeBlock
CodeBlockPython, CodeBlockBash, CodeBlockSQL, CodeBlockJavaScript, CodeBlockHTML, CodeBlockCSS,
CodeBlockC, CodeBlockCPP, CodeBlockRuby, CodeBlockR, CodeBlockPerl, CodeBlockScala,
CodeBlockMake, CodeBlockLua, CodeBlockRst, CodeBlockMarkdown   # same fields and from_string
CodeBlockBase   # their base class; CodeBlockBase.LangOptions lists the language names
CodeBlockEmpty(code: Code)   # a `::` literal block; from_string(text)
```

- `CodeBlock` has no language (`.. code-block::`); each subclass sets one (`python`, `bash`, ..., `ReST` for `CodeBlockRst`, `md` for `CodeBlockMarkdown`).
- `CodeBlockEmpty` renders `::`; it has no options, so `class_` and `name` are ignored.
- `Code(text=...).render(indent=1)` is plain indented text.

```python
block = rstobj.directives.CodeBlockPython(
    code=rstobj.directives.Code(text="print('Hello World!')"),
    name="hello",
)
rst = block.render()
```

Output (`repr` shows the exact newlines):

```python
".. code-block:: python\n    :name: hello\n\n    print('Hello World!')"
```

Rendered text:

```rst
.. code-block:: python
    :name: hello

    print('Hello World!')
```

---

## 10. TableOfContent (`rstobj.directives`)

```python
TableOfContent(title: str | None = None, depth: int | None = None, local: bool = False, backlinks: str | None = None, class_: str | None = None, name: str | None = None)
```

- `backlinks`: `TableOfContent.BacklinksOptions.entry` / `top` / `none`; `ValueError` otherwise.
- `name` is ignored: the `contents` directive has no `:name:` option.
- Output ends with `"\n"`.

```python
toc = rstobj.directives.TableOfContent(title="Contents", depth=2, local=True)
rst = toc.render()
```

Output (`repr` shows the exact newlines):

```python
'.. contents:: Contents\n    :depth: 2\n    :local:\n'
```

Rendered text:

```rst
.. contents:: Contents
    :depth: 2
    :local:
```

---

## 11. Include (`rstobj.directives`)

```python
Include(path: str, start_line: int | None = None, end_line: int | None = None, start_after: str | None = None, end_before: str | None = None, literal: bool | None = None, code: str | None = None, number_lines: int | None = None, encoding: str | None = None, tab_width: int | None = None, class_: str | None = None, name: str | None = None)
```

- Fields map to docutils' hyphenated options (`start_line` renders `:start-line:`).
- `literal=True` renders `:literal:`; `False` or `None` renders nothing.
- `path` is relative to the document that contains the output; in Sphinx, relative to the page.
- Output ends with `"\n"`.

```python
include = rstobj.directives.Include(path="snippet.txt", start_line=2, end_line=10, literal=True)
rst = include.render()
```

Output (`repr` shows the exact newlines):

```python
'.. include:: snippet.txt\n    :start-line: 2\n    :end-line: 10\n    :literal:\n'
```

Rendered text:

```rst
.. include:: snippet.txt
    :start-line: 2
    :end-line: 10
    :literal:
```
