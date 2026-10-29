# 07 · Auth & permissions

## Custom user model (do it on day one)
```python
class User(AbstractUser):
    class Role(models.TextChoices):
        CLIENT = "CLIENT", "Client"
        FREELANCER = "FREELANCER", "Freelancer"

    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=Role.choices)
```
`AUTH_USER_MODEL = "marketplace.User"`; refer to it with `settings.AUTH_USER_MODEL` in FKs and `get_user_model()` in code.

| | `AbstractUser` | `AbstractBaseUser` |
|---|---|---|
| Gives | full user (username, groups, permissions, admin) | only password + login mechanics |
| Use when | adding fields | totally custom identity (e.g. phone-only) |

## Authentication
- `authenticate()`, `login()`, `logout()`; built-in `LoginView`/`LogoutView`/password reset views via `include("django.contrib.auth.urls")`.
- Passwords are hashed (PBKDF2 by default; add Argon2 with `argon2-cffi`). Never store or log raw passwords.

## Authorization
- Model permissions are auto-created: `marketplace.add_project`, `change_`, `delete_`, `view_`. Check with `user.has_perm("marketplace.change_project")`.
- **Groups** bundle permissions (e.g. "Moderators").
- **Object-level** rules ("only the owner can edit") are code: `UserPassesTestMixin`, DRF `has_object_permission`, or `django-guardian`/`django-rules`.
- Role checks belong in one place (`user.is_client`), not sprinkled `if user.role == "CLIENT"` strings.

## Exercises
1. Add a "Moderators" group that may change any project, and test it.
2. Switch login to email by setting `USERNAME_FIELD = "email"` on a fresh database.
