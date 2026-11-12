.. _rendering-gallery:

Rendering Gallery
==============================================================================
Every example on this page is a unit test. For each one you see the Python code, the exact reStructuredText it produces, and how Sphinx renders that text.

The examples come from ``rstobj/tests/cases.py``. The tests compare each output byte for byte with its file in ``rstobj/tests/snapshots/`` and check that docutils parses it without a warning; this page includes those same files. To add an example, add a case function there, then run the tests with ``RSTOBJ_UPDATE_SNAPSHOTS=1`` to create its snapshot.

.. jinja:: doc_data

    {{ doc_data.gallery_rst }}
