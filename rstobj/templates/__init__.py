# -*- coding: utf-8 -*-

import os
from jinja2 import Environment
from jinja2 import FileSystemLoader
from jinja2 import StrictUndefined

# StrictUndefined: a typo in a template raises instead of rendering nothing.
env = Environment(
    loader=FileSystemLoader(os.path.dirname(__file__)),
    undefined=StrictUndefined,
)
