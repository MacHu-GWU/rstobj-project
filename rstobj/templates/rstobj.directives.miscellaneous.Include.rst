{% extends "rstobj.directives.base.Directive.rst" %}
{% block other %}
{%- if obj.start_line is not none %}
{{ tab }}:start-line: {{ obj.start_line }}
{%- endif %}
{%- if obj.end_line is not none %}
{{ tab }}:end-line: {{ obj.end_line }}
{%- endif %}
{%- if obj.start_after is not none %}
{{ tab }}:start-after: {{ obj.start_after }}
{%- endif %}
{%- if obj.end_before is not none %}
{{ tab }}:end-before: {{ obj.end_before }}
{%- endif %}
{%- if obj.literal %}
{{ tab }}:literal:
{%- endif %}
{%- if obj.code is not none %}
{{ tab }}:code: {{ obj.code }}
{%- endif %}
{%- if obj.number_lines is not none %}
{{ tab }}:number-lines: {{ obj.number_lines }}
{%- endif %}
{%- if obj.encoding is not none %}
{{ tab }}:encoding: {{ obj.encoding }}
{%- endif %}
{%- if obj.tab_width is not none %}
{{ tab }}:tab-width: {{ obj.tab_width }}
{%- endif %}
{% endblock %}