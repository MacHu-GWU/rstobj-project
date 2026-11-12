---
description: "The case-driven tests: rstobj/tests/cases.py and its Case flags, the byte-exact snapshot files and RSTOBJ_UPDATE_SNAPSHOTS, the docutils validity check and its Sphinx stand-ins, the include fixture, the per-module test files, and the Rendering Gallery docs page built from the same cases. Read when adding or changing a test case, when a snapshot or validity check fails, or when the docs gallery breaks."
---

# Cases, Snapshots, and the Gallery

One list of cases is the single source of truth for both the tests and the "Rendering Gallery" docs page.

---

## 1. A case

In `rstobj/tests/cases.py`, a case is a small function registered with `@case(module, title, gallery=True, live=True)`:

```python
@case(M_TABLE, "Table with a header row")
def list_table_with_header():
    table = ListTable(data=[["id", "name"], [1, "Alice"]], title="Users")
    return table.render()
```

| Part | Meaning |
| :--- | :--- |
| `module` | The rstobj module under test; the per-module test file selects its cases with `cases_for(module)`. |
| function name | With the module, forms `Case.id` (`directives.table.list_table_with_header`), the snapshot file name. Keep it unique. |
| `title` | The case's heading in the gallery. |
| `gallery=False` | Edge case: tested, not shown in the docs. |
| `live=False` | Shown in the docs as code and text, but not rendered on the page: headers, `contents`, and `include` would change the page's own structure. |
| body | Must end with one `return <expr>` line: `Case.code` shows the body to readers with that line turned into `rst = <expr>`. |

---

## 2. What each case checks

`Case.check()`, run by `test_case` in every `tests/<subpackage>/test_<...>.py`:

1. The output equals `rstobj/tests/snapshots/<case.id>.rst` **byte for byte**. No stripping: indentation, trailing whitespace, and leading and trailing newlines are all part of the contract.
2. `assert_valid_rst` (`rstobj/tests/rst_check.py`) parses the output with docutils and fails on any warning or error. It registers a stand-in for Sphinx's `:ref:` role and turns off syntax highlighting (no Pygments lexer lookup). The snapshot's path is passed as `source_path`, so `.. include:: include-me.txt` resolves to `rstobj/tests/snapshots/include-me.txt`, the include fixture.

Each module's test file also runs `find_orphan_snapshots(module)`, which fails on a snapshot that no case produces anymore.

---

## 3. Updating snapshots

After an intended output change:

```bash
RSTOBJ_UPDATE_SNAPSHOTS=1 .venv/bin/pytest tests -q
git diff rstobj/tests/snapshots
```

Review every changed file: the diff **is** the output change users will see. A new case's snapshot is created the same way. Delete a snapshot by hand when you remove its case.

---

## 4. The Rendering Gallery

- `rstobj/docs/__init__.py` builds `doc_data["gallery_rst"]` from `CASES`, with rstobj itself (`Header2`, `Header3`, `CodeBlockPython`, `CodeBlockRst`). `GROUP_TITLES` sets the section order and titles; a new module needs an entry there, or its cases are not shown.
- `docs/source/01-Rendering-Gallery/index.rst` inserts it with `.. jinja:: doc_data`. For a `live` case, the page shows the snapshot through `.. include::` inside a `.. card::`, with a path relative to the page folder (`DIR_GALLERY_PAGE`). So the docs render exactly the bytes the tests assert.
- `docs/source/conf.py` imports `doc_data` under `except ImportError` only: any other error in the gallery code fails the build instead of emptying the page.
- `mise run build-doc` runs Sphinx with `-W --keep-going`, and `.readthedocs.yml` sets `fail_on_warning: true`: a case whose live output makes Sphinx warn fails the docs build.
- Sphinx resolves a nested include, and an image URI inside an included snapshot, relative to the **page**, not the snapshot. That is why include cases are not live, and why `image_with_scale` uses `../_static/rstobj-logo.png`: `:scale:` needs a local image whose size Sphinx can read.
