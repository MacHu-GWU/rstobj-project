{% extends "rstobj.directives.base.Directive.rst" %}
{% block other %}
{%- set width = tab|length + 4 %}
{%- if obj.header %}
{{ tab }}:header-rows: 1
{%- else %}
{{ tab }}:header-rows: 0
{%- endif %}
{%- if obj.index %}
{{ tab }}:stub-columns: 1
{%- else %}
{{ tab }}:stub-columns: 0
{%- endif %}
{%- if obj.widths %}
{{ tab }}:widths: {{ obj.widths_arg }}
{%- endif %}
{%- if obj.align is not none %}
{{ tab }}:align: {{ obj.align }}
{%- endif %}
{% for row in obj.data %}
{%- for item in row %}
{%- if loop.index0 == 0 %}
{{ tab }}* - {{ obj._render_nested(item, width) }}
{%- else %}
{{ tab }}  - {{ obj._render_nested(item, width) }}
{%- endif %}
{%- endfor %}
{%- endfor %}
{% endblock %}