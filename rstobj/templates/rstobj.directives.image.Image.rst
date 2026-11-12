{% extends "rstobj.directives.base.Directive.rst" %}
{% block other %}
{%- if obj.height is not none %}
{{ tab }}:height: {{ obj.height }}px
{%- endif %}
{%- if obj.width is not none %}
{{ tab }}:width: {{ obj.width }}px
{%- endif %}
{%- if obj.scale is not none %}
{{ tab }}:scale: {{ obj.scale }}%
{%- endif %}
{%- if obj.alt_text is not none %}
{{ tab }}:alt:{% if obj.alt_text %} {{ obj.alt_text }}{% endif %}
{%- endif %}
{%- if obj.align is not none %}
{{ tab }}:align: {{ obj.align }}
{%- endif %}
{% endblock %}