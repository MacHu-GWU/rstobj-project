---
description: "How rstobj is built: the RstObj base class, the template lookup by module and class name, the classes that share a template, the jinja2 environment, the Directive base template, and where the public API is defined. Read when you need to know where a piece of output comes from, or before adding or moving a class."
---

# Architecture

---

## 1. Objects and templates

- Every renderable class is a `@dataclass(kw_only=True)` subclass of `RstObj` (`rstobj/base.py`). All fields are keyword-only.
- `RstObj.template_name` returns `"<module>.<ClassName>.rst"`, such as `rstobj.directives.image.Image.rst`. The file lives in `rstobj/templates/`.
- `RstObj.render()` renders that template with two variables: `obj` (the object) and `tab` (`rstobj.option.Options.tab`, four spaces by default).
- `RstObj` itself has no template; only subclasses render.

---

## 2. Classes that share a template

Two families override `template_name` to point at one shared file:

| Classes | Template | Where the override is |
| :--- | :--- | :--- |
| `CodeBlockBase` and its 17 language subclasses (`CodeBlock`, `CodeBlockPython`, ...) | `rstobj.directives.codeblock.CodeBlockBase.rst` | `CodeBlockBase.template_name` in `rstobj/directives/codeblock.py` |
| `Header`, `HeaderLevel`, `Header1` ... `Header7` | `rstobj.markup.header.Header.rst` | `Header.template_name` in `rstobj/markup/header.py` |

A language subclass differs only by its `meta_lang` class variable (`CodeBlockBase.LangOptions`); a `HeaderN` subclass only by the default of `header_level`. `CodeBlockEmpty` (the `::` literal block) has its own template.

---

## 3. The jinja2 environment

`rstobj/templates/__init__.py` builds one module-level `env`:

- `FileSystemLoader` on the `rstobj/templates/` folder;
- `undefined=StrictUndefined`, so a misspelled attribute in a template raises `jinja2.exceptions.UndefinedError` instead of rendering an empty string (tested in `tests/test_base.py`);
- jinja2's default `keep_trailing_newline=False`: the final newline of a template file is dropped.

---

## 4. Directives

- `Directive` (`rstobj/directives/base.py`) adds the `class_` and `name` fields and two class variables: `meta_directive_keyword` (such as `"image"`) and `meta_supports_name` (False for `TableOfContent`, because `contents` has no `:name:` option).
- `rstobj.directives.base.Directive.rst` renders `.. <keyword>:: <arg>`, then `:class:` and `:name:`, then `{% block other %}`. `Image`, `ListTable`, `TableOfContent`, and `Include` extend it and fill `other` with their own options. Each subclass defines the `arg` property (the directive argument: `uri`, `path`, `title`).
- The code block templates do not extend `Directive.rst`: they render `:class:` and `:name:` themselves, and `CodeBlockEmpty` renders neither (a `::` literal block has no options).

---

## 5. Public API

- `rstobj/api.py` exposes two modules: `directives` (`rstobj/directives/api.py`) and `markup` (`rstobj/markup/api.py`). Users write `import rstobj.api as rstobj`, then `rstobj.markup.Header(...)`.
- `rstobj.option.Options` is **not** public API, though `render()`'s docstring mentions it. Do not export it.
- `rstobj/docs/` (gallery data) and `rstobj/tests/` (cases, snapshots, helpers) are excluded from the wheel by `[tool.setuptools.packages.find] exclude` in `pyproject.toml`.
