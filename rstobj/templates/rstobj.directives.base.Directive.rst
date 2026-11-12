.. {{ obj.meta_directive_keyword }}::{% if obj.arg %} {{ obj.arg }}{% endif %}
{%- if obj.class_ is not none %}
{{ tab }}:class: {{ obj.class_ }}
{%- endif %}
{%- if obj.name is not none and obj.meta_supports_name %}
{{ tab }}:name: {{ obj.name }}
{%- endif %}
{%- block other %}{% endblock %}
