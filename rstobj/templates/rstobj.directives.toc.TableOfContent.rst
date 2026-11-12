{% extends "rstobj.directives.base.Directive.rst" %}
{% block other %}
{%- if obj.depth is not none %}
{{ tab }}:depth: {{ obj.depth }}
{%- endif %}
{%- if obj.local %}
{{ tab }}:local:
{%- endif %}
{%- if obj.backlinks is not none %}
{{ tab }}:backlinks: {{ obj.backlinks }}
{%- endif %}
{% endblock %}