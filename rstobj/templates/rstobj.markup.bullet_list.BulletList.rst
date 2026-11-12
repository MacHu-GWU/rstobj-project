{%- for item in obj.items %}
- {{ obj._render_nested(item, 2) }}
{%- endfor %}
