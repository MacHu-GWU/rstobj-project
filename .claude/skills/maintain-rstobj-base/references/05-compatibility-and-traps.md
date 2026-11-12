---
description: "What a patch, minor, or major release may change in rstobj's output and API, the known design limitations deliberately left for later releases, and the traps that already broke a release. Read when deciding which version number a change needs, or before changing output that users may depend on."
---

# Compatibility and Known Traps

---

## 1. What each release may change

The maintainer's rule: a release that only improves quality (tests, docs, fixes) is a patch; a new feature or a behavior change gets a higher version. Applied to rstobj:

| Release | May change |
| :--- | :--- |
| Patch (`x.y.Z`) | Tests, docs, tooling. Output that was **invalid** reStructuredText or plainly wrong (a dropped field, a Python repr). Whitespace only (trailing spaces, whitespace-only lines). Every output that was valid stays byte-identical otherwise. |
| Minor (`x.Y.0`) | A new public name in `api.py` (such as a new class). New optional fields or options that render nothing by default. Raising a new error where the old output was invalid anyway. |
| Major (`X.0.0`) | Any change to output that was valid, a removed or renamed public name, a changed field default, or changed field semantics. |

To check a change against this table, compare the snapshot diff (`04-cases-snapshots-gallery.md` section 3): every changed snapshot must have been invalid or wrong before.

---

## 2. Known limitations, deliberately left for later

Found in the 2.0.1 review; each changes behavior users can see, so none fits a patch. The planned work is in the `x.y.z (Backlog)` section of `release-history.rst`.

| Limitation | Where | Needs |
| :--- | :--- | :--- |
| A list item or table cell holds one string or one object, so "text with a nested list under it" needs string concatenation. Planned: a `Blocks` container. | `BulletList`, `EnumList`, `ListTable` | Minor |
| No validation at construction: an empty `ListTable`, rows of unequal length, `widths` of the wrong length, or `header=True` with one row render invalid output. | `rstobj/directives/table.py` | Minor (raise `ValueError`) |
| `Image.AlignOptions` accepts `top`/`middle`/`bottom`, which are only valid inside a substitution definition. Only documented now. | `rstobj/directives/image.py` | Minor to raise |
| String items and titles are inserted as raw reStructuredText, never escaped: a backtick in a `URI` title breaks the link silently. | all templates | Major (changes output for users who escape by hand) |
| `URI` renders a named reference (`` `_ ``): two links with the same title and different targets make docutils warn. | `rstobj.markup.hyperlink.URI.rst` | Major to default to anonymous (`` `__ ``); minor as an opt-in field |
| `Header` computes `ref_label` and `bar_length` once in `__post_init__`; changing `title` afterwards leaves them stale. | `rstobj/markup/header.py` | Major |
| Leading and trailing newlines differ between classes (`02-rendering-and-indentation.md` section 3). | templates | Major |

---

## 3. Traps that already broke a release

- **Templates missing from the wheel.** The `.rst` templates are package data. `[tool.setuptools.package-data]` in `pyproject.toml` must list `templates/*.rst`; without it, 2.0.0 installed from PyPI raised `TemplateNotFound` on the first `render()`, while every local test passed (tests import the source tree). After touching packaging config, build a wheel (`mise run build`) and check that `rstobj/templates/*.rst` is in it.
- **Validity was never tested before 2.0.1.** The old golden files were compared after stripping whitespace, and nothing parsed the output, so invalid option names and broken indentation shipped for years. Keep every case going through `assert_valid_rst`.
