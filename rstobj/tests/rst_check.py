# -*- coding: utf-8 -*-

"""
Check that a piece of reStructuredText is valid, by parsing it with docutils.
"""

from __future__ import annotations

import io
from pathlib import Path

from docutils import nodes
from docutils.core import publish_doctree
from docutils.parsers.rst import roles


def _ref_role(name, rawtext, text, lineno, inliner, options=None, content=None):
    """
    Stand-in for Sphinx's ``:ref:`` role, which plain docutils does not know.
    """
    return [nodes.reference(rawtext, text)], []


roles.register_local_role("ref", _ref_role)


def find_rst_problems(
    rst: str,
    source_path: Path | None = None,
) -> str:
    """
    Parse ``rst`` with docutils and return every warning or error it reports,
    as one string. An empty string means the text is valid.

    :param source_path: the path the text pretends to come from, so that
        relative ``.. include::`` paths resolve next to it.
    """
    stream = io.StringIO()
    publish_doctree(
        rst,
        source_path=None if source_path is None else str(source_path),
        settings_overrides={
            "report_level": 2,  # report warnings and errors
            "halt_level": 5,  # never raise, collect everything
            "warning_stream": stream,
            "syntax_highlight": "none",  # no Pygments lexer lookup
            "file_insertion_enabled": True,
        },
    )
    return stream.getvalue()


def assert_valid_rst(
    rst: str,
    source_path: Path | None = None,
):
    """
    Fail with the docutils messages if ``rst`` is not valid reStructuredText.
    """
    problems = find_rst_problems(rst, source_path=source_path)
    assert problems == "", f"invalid reStructuredText:\n{problems}\n---\n{rst}"
