---
description: "What render() returns: the indent and first_line_indent arguments, how list items and table cells indent nested content, why strings that are already indented are left alone, and the leading and trailing newlines each kind of object produces. Read when output is mis-indented, when changing base.py, or when nesting one object inside another."
---

# Rendering and Indentation

All of this is in `rstobj/base.py`.

---

## 1. `render(indent=None, first_line_indent=None)`

- With neither argument, `render()` returns the template output unchanged.
- With `indent=n`, every line gets `Options.tab * n` in front, trailing whitespace is stripped, and **blank lines stay empty** (`_indent_line`), so indented output never has whitespace-only lines.
- `first_line_indent=m` replaces the first line's indent with `Options.tab * m`. It also works without `indent` (indent counts as 0). A negative value raises `TypeError`.
- Code blocks use this to indent their code: the template calls `obj.code.render(indent=1)`.

---

## 2. Nested items: `_render_nested(value, width)`

List items and table cells start after a marker: `"- "` (width 2), `"9. "` / `"10. "` (width 3 / 4, per item), or `"    * - "` / `"      - "` in a list table (width `len(tab) + 4`). Templates call `obj._render_nested(item, width)`:

- **An `RstObj`:** rendered with `render()`, its leading and trailing newlines stripped, then every continuation line indented by `width` spaces (`_indent_continuation(..., force=True)`).
- **Anything else:** `str(value)`, taken as raw reStructuredText (never escaped). Its continuation lines are indented by `width` spaces **unless** every non-blank continuation line is already indented by at least `width` (`force=False`). That exception keeps the output of callers who indented their strings by hand before 2.0.1 unchanged.

`str_or_render(value, **kwargs)` is the older public helper (render an `RstObj`, `str()` anything else). Templates no longer call it; keep it for users.

---

## 3. Leading and trailing newlines

Output framing is not uniform, and callers that concatenate output depend on it, so it must not change in a patch release:

| Object | Starts with `\n` | Ends with `\n` |
| :--- | :--- | :--- |
| `Header` and subclasses, `BulletList`, `EnumList` | yes | no |
| Directives built on `Directive.rst` (`Image`, `ListTable`, `TableOfContent`, `Include`) | no | yes |
| `CodeBlockEmpty`, `CodeBlockBase` family, `Code`, `URI`, `Reference` | no | no |

The leading newline comes from the template text after a `{%- ... %}` tag. When nesting, `_render_nested` strips both ends, so framing does not leak into list items or cells.

---

## 4. A multi-line string is one paragraph

`"line 1\nline 2"` renders as one paragraph, "line 1 line 2": in reStructuredText a single newline inside a paragraph is a space. Separate paragraphs with a blank line (`"\n\n"`). This is reStructuredText, not a bug.
