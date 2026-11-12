.. code-block::{% if obj.meta_lang %} {{ obj.meta_lang }}{% endif %}
{%- if obj.class_ is not none %}
{{ tab }}:class: {{ obj.class_ }}
{%- endif %}
{%- if obj.name is not none %}
{{ tab }}:name: {{ obj.name }}
{%- endif %}

{{ obj.code.render(indent=1) }}