{%- for item in obj.items %}
{%- set marker = (obj.start_num + loop.index0)|string + ". " %}
{{ marker }}{{ obj._render_nested(item, marker|length) }}
{%- endfor %}
