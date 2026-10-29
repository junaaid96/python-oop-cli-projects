# 09 · Django REST Framework

DRF turns models into a JSON API. Code: [`serializers.py`](../../projects/16_django_freelance_hub/marketplace/serializers.py), [`api_views.py`](../../projects/16_django_freelance_hub/marketplace/api_views.py), [`permissions.py`](../../projects/16_django_freelance_hub/marketplace/permissions.py).

## Endpoints in the project
| Method | URL | Who |
|---|---|---|
| GET | `/api/v1/projects/?search=&ordering=-budget&status=open&page=2` | anyone |
| POST | `/api/v1/projects/` | clients |
| PATCH/DELETE | `/api/v1/projects/{id}/` | the owner |
| GET/POST | `/api/v1/projects/{id}/proposals/` | owner reads, freelancers post |
| POST | `/api/v1/proposals/{id}/accept/` | the owner |
| POST | `/api/v1/auth/token/` | get a token |

## Serializers
Convert model ↔ JSON and validate input — the API version of a form.
```python
class ProjectSerializer(serializers.ModelSerializer):
    client = serializers.ReadOnlyField(source="client.username")
    skills = serializers.SlugRelatedField(
        many=True, slug_field="name", queryset=Skill.objects.all()
    )
    proposal_count = serializers.IntegerField(read_only=True)  # from annotate()

    def validate_title(self, value): ...  # field validation

    # def validate(self, attrs): ...                             # cross-field
```
Nested serializers are read-only by default; for writes, override `create()`/`update()` or accept IDs.

## Views → ViewSets → Routers
| Level | Example | Use |
|---|---|---|
| `APIView` | `def get(self, request)` | full control |
| Generic views | `ListCreateAPIView` | one resource, little code |
| `ModelViewSet` | list/create/retrieve/update/destroy | CRUD + `@action` extras |

`DefaultRouter().register("projects", ProjectViewSet)` generates the URLs. `@action(detail=True, methods=["post"])` adds `/projects/{id}/proposals/`.

## Authentication & permissions
- Auth classes (settings `DEFAULT_AUTHENTICATION_CLASSES`): Session (browser), Token (`rest_framework.authtoken`), JWT via `djangorestframework-simplejwt`. Order matters: the first class decides the `WWW-Authenticate` header, so we list Token first to get **401** (not 403) for anonymous writes.
- Permissions: `has_permission` (view level) and `has_object_permission` (after `get_object()`). The project combines `IsClientOrReadOnly` and `IsOwnerOrReadOnly`.
- 401 = who are you? 403 = I know you, but no.

## Pagination, filtering, ordering, throttling
```python
REST_FRAMEWORK = {
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 10,
    "DEFAULT_THROTTLE_RATES": {"anon": "100/hour", "user": "1000/hour"},
}
filter_backends = (filters.SearchFilter, filters.OrderingFilter)
search_fields = ("title", "skills__name")
ordering_fields = ("budget", "created_at")
```
Use `CursorPagination` for large, changing feeds; `django-filter` for `?budget_min=` style filters. Paginated querysets must be ordered.

## Performance
Serializers trigger N+1s too: `get_queryset()` uses `with_related()`. Never put a query inside `SerializerMethodField` without prefetching.

## Business rules
Views call `services.submit_proposal(...)`; a `BusinessRuleError` becomes HTTP 400. Same rules power HTML and API, and are unit-tested without HTTP.

## Testing
```python
api = APIClient()
api.force_authenticate(user)
assert api.post("/api/v1/projects/", payload).status_code == 201
```
See [13 · Testing](13_testing.md). Generate an OpenAPI schema with `drf-spectacular`.

## Exercises
1. Add `django-filter` with `budget_min`/`budget_max`.
2. Add a `/api/v1/me/` endpoint.
3. Add JWT auth with simplejwt and test refresh.
