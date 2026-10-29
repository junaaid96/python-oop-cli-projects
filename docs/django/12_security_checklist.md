# 12 · Security checklist

Run `python manage.py check --deploy` with production settings; fix every warning.

| Risk | Django's defence | Your job |
|---|---|---|
| SQL injection | ORM parameterises queries | never format strings into `raw()`/`extra()`; pass `params` |
| XSS | templates auto-escape | avoid `|safe`/`mark_safe` on user input; add a CSP (built in since Django 6.0) |
| CSRF | `CsrfViewMiddleware` + `{% csrf_token %}` | keep it on; DRF session auth enforces CSRF too |
| Clickjacking | `XFrameOptionsMiddleware` | keep it on |
| Mass assignment | explicit `fields` on forms/serializers | never `"__all__"` on input |
| Broken access control | permissions & object checks | test "user B can't edit user A's data" (see the tests) |
| Secrets leak | — | env vars, rotate `SECRET_KEY` with `SECRET_KEY_FALLBACKS` |
| Brute force | — | throttling (DRF), `django-axes`, 2FA for staff |

Production settings (already in the project when `DEBUG=0`):
```python
DEBUG = False
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 2592000
ALLOWED_HOSTS = ["api.example.com"]
```
Also: keep Django on a supported release (patch releases are security fixes), `pip-audit`/Dependabot for dependencies, validate uploads (size, type, store outside the web root), and never expose stack traces (`DEBUG=False`).
