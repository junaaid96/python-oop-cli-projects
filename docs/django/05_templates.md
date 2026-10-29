# 05 · Templates

```django
{% extends "marketplace/base.html" %}
{% block content %}
  {% for project in object_list %}
    <a href="{% url 'project-detail' project.pk %}">{{ project.title }}</a>
    {{ project.proposal_count }} proposal{{ project.proposal_count|pluralize }}
  {% empty %}No projects.{% endfor %}
{% endblock %}
```

- **Inheritance**: `base.html` defines `{% block %}`s; pages `{% extends %}` and fill them.
- **Variables** `{{ }}`, **tags** `{% %}`, **filters** `|date:"Y-m-d"`, `|default:"-"`, `|linebreaksbr`.
- `{% url 'name' arg %}` builds links from URL names, so changing a path never breaks templates.
- `{% include "partial.html" %}` for reusable fragments; Django 6.0 adds **template partials** (`{% partialdef %}`/`{% partial %}`) for fragments inside one file, handy with htmx.
- **Auto-escaping** prevents XSS. `|safe` and `mark_safe` turn it off — only for trusted HTML.
- Keep logic out of templates: compute in the view or a model method. Templates calling `project.skills.all` in a loop is an N+1 unless the view prefetched it.
- Custom filters/tags live in `app/templatetags/`.

## Exercises
1. Add a `money` filter that formats `Decimal` as `$1,234.00`.
2. Move the project card into a partial and reuse it on two pages.
