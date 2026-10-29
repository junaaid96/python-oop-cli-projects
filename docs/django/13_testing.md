# 13 · Testing with pytest-django

Config lives in `pyproject.toml`:
```toml
[tool.pytest.ini_options]
DJANGO_SETTINGS_MODULE = "hub_site.settings"
pythonpath = ["projects/16_django_freelance_hub"]
```

```python
pytestmark = pytest.mark.django_db  # every test may use the (test) database


@pytest.fixture
def client_user() -> User:
    return User.objects.create_user("ada", "ada@example.com", "pw", role=User.Role.CLIENT)


def test_project_list_page(client, project):  # `client` = Django test client fixture
    assert b"Build a REST API" in client.get("/").content
```

What the project's [tests](../../projects/16_django_freelance_hub/tests/test_freelance_hub.py) cover:
- **ORM**: custom QuerySet, annotation, DB constraint (`IntegrityError`).
- **Query counts**: `CaptureQueriesContext` (or the `django_assert_num_queries` fixture) to lock in N+1 fixes.
- **Services**: business rules without HTTP.
- **HTML views**: status codes, redirects, role checks with `client.force_login`.
- **API**: `APIClient`, `force_authenticate`, 401 vs 403, validation errors, pagination, a full proposal flow, token auth.

Tips: tests run in a transaction and roll back; use `factory_boy` for bigger data; `@pytest.mark.django_db(transaction=True)` when testing `on_commit`/`select_for_update` for real; `settings` fixture to override settings per test; keep tests fast (SQLite in memory is the default for tests).

```bash
uv run pytest projects/16_django_freelance_hub -v
```
