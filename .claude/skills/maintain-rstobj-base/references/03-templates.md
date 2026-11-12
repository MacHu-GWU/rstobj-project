---
description: "Rules for writing the jinja2 templates in rstobj/templates: file names, option lines, the None-versus-falsy test for each option, real hyphenated option names, no trailing whitespace, the tab variable, and checking options against the docutils directive. Read before editing or adding a template, or when a directive option renders wrong."
---

# Templates

Templates live in `rstobj/templates/`, one per class or shared family (`01-architecture.md`).

---

## 1. Shape of a directive template

```jinja
{% extends "rstobj.directives.base.Directive.rst" %}
{% block other %}
{%- if obj.option_name is not none %}
{{ tab }}:option-name: {{ obj.option_name }}
{%- endif %}
{% endblock %}
```

- One `{%- if %}` block per option, in a stable order: the snapshots lock it (`02-rendering-and-indentation.md` explains the output shape they record).
- `{%-` strips the newline before the tag, so each option starts its own line and no blank line appears between options.
- Indent option lines with `{{ tab }}`, never with literal spaces. A literal indent breaks the output as soon as a user changes `Options.tab` (tested in `tests/test_option.py`).

---

## 2. Option rules (each was a real bug fixed in 2.0.1)

| Rule | Why |
| :--- | :--- |
| Use the directive's real option name, with hyphens: `:start-line:`, `:number-lines:`, `:tab-width:`. The Python field keeps underscores. | docutils rejects unknown option names, and the whole directive fails. |
| A flag option (no value, such as `:literal:`, `:local:`) uses a truthiness test: `{%- if obj.literal %}`. | `is not none` rendered `:literal:` for `literal=False`. |
| A list option tests truthiness too: `{%- if obj.widths %}`. | `widths=[]` rendered an empty `:widths:`, which docutils rejects. |
| A valued option tests `is not none`, so `0` still renders. | |
| No trailing space when a value can be empty: `.. code-block::{% if obj.meta_lang %} {{ obj.meta_lang }}{% endif %}`, and the same for `:alt:` and the directive argument. | Trailing whitespace makes dirty diffs. |
| Render every field the class declares, or document that it is ignored. | `Image.scale` and the code block `class_`/`name` were silently dropped. |
| Do not render an option the directive does not have; set `meta_supports_name = False` for `:name:`. | `contents` has no `:name:`; rendering it made docutils reject the directive. |

---

## 3. Checking an option

Look up the directive's option list before adding one: <https://docutils.sourceforge.io/docs/ref/rst/directives.html> (`code-block` is Sphinx's: <https://www.sphinx-doc.org/en/master/usage/restructuredtext/directives.html#directive-code-block>). Then add a case that sets the option: the tests parse the output with docutils, so a wrong name or value fails there.
