# 15 · Django & DRF interview Q&A

Short answers; follow the links for depth.

## Django core
1. **Project vs app?** Project = settings + root URLs; app = a reusable feature package. ([01](01_project_structure.md))
2. **Request lifecycle?** Server → middleware → URL resolver → view → response → middleware (reverse).
3. **What is middleware?** A callable wrapping every request/response; e.g. sessions, CSRF, auth. Order in `MIDDLEWARE` matters.
4. **MVT vs MVC?** Django's View ≈ MVC controller, Template ≈ view; the framework itself is the "controller" routing.
5. **Signals — when?** Decoupled reactions (e.g. create a profile on user create). Avoid for core business logic: hidden control flow; prefer explicit service calls.
6. **Why a custom user model?** Changing later is painful; set `AUTH_USER_MODEL` before the first migration. ([07](07_auth_and_permissions.md))
7. **`AbstractUser` vs `AbstractBaseUser`?** Extend vs build from scratch.
8. **`null=True` vs `blank=True`?** DB allows NULL vs form allows empty. Strings: prefer `blank=True` with `""`.
9. **`auto_now` vs `auto_now_add`?** Every save vs creation only.
10. **Manager vs QuerySet?** Manager is the entry point (`objects`); put chainable logic on a QuerySet and expose it with `as_manager()`.

## ORM
11. **N+1?** One query for the list plus one per row for a relation. Fix with `select_related` (FK, JOIN) or `prefetch_related` (M2M/reverse, extra query). ([02](02_models_and_orm.md))
12. **Are QuerySets lazy?** Yes; evaluated on iteration, `list()`, slicing with step, `len()`, `bool()`.
13. **`F()` and `Q()`?** Column references in SQL (race-free `F("views") + 1`) and OR/NOT conditions.
14. **`annotate` vs `aggregate`?** Per-row value vs one summary dict.
15. **`update()` vs `save()`?** Single SQL UPDATE, no `save()`/signals vs per-object with hooks.
16. **Avoid race conditions?** `transaction.atomic` + `select_for_update`, `F()` expressions, DB constraints. (`services.accept_proposal`)
17. **`exists()` vs `count()`?** `exists()` stops at the first row.
18. **Raw SQL safely?** `Model.objects.raw(sql, params)` / `cursor.execute(sql, params)`; never f-strings.
19. **Migrations conflict?** `makemigrations --merge`; prevent with small, frequent migrations.
20. **Index what?** Columns in frequent `filter`/`order_by` (composite in that order); check with `EXPLAIN` (`qs.explain()`).

## Views, forms, templates
21. **FBV or CBV?** FBV for unique flows, CBV for CRUD/reuse. ([04](04_views.md))
22. **How does CSRF work?** Secret cookie + token in form; middleware compares on unsafe methods.
23. **Form validation order?** field clean → `clean_<field>` → `clean()` → model `full_clean`.
24. **Prevent XSS?** Auto-escaping; avoid `|safe` on user data; CSP.

## DRF
25. **Serializer vs ModelSerializer?** Manual fields vs generated from a model.
26. **`APIView` vs `GenericAPIView` vs `ViewSet`?** Increasing abstraction; ViewSets + routers for CRUD. ([09](09_drf.md))
27. **`has_permission` vs `has_object_permission`?** Every request vs only after `get_object()` (not for list views!).
28. **401 vs 403?** Unauthenticated vs authenticated but forbidden. First auth class sets `WWW-Authenticate`.
29. **Session vs Token vs JWT?** Browser cookies + CSRF; opaque DB token; signed self-contained token (stateless, harder to revoke — use short expiry + refresh).
30. **Pagination types?** PageNumber, LimitOffset, Cursor (stable for big, changing feeds).
31. **Throttling?** Rate limits by scope (`anon`, `user`, custom) using the cache.
32. **Where does business logic go?** Services; serializers validate shape, views do HTTP.
33. **Nested writes?** Override `create`/`update` in the serializer, wrapped in a transaction.
34. **Optimise a slow endpoint?** Count queries, `select_related`/`prefetch_related`, `only()`, pagination, caching, indexes.
35. **API versioning?** URL prefix (`/api/v1/`) or `DEFAULT_VERSIONING_CLASS`.

## Production
36. **What does `check --deploy` check?** DEBUG, HSTS, secure cookies, SSL redirect, `SECRET_KEY` strength, etc. ([12](12_security_checklist.md))
37. **WSGI vs ASGI?** Sync vs async protocol; ASGI for websockets/long I/O.
38. **Static vs media?** Your assets (`collectstatic`) vs user uploads (object storage).
39. **Why Celery and `on_commit`?** Move slow work out of requests; run only after the data is committed. ([11](11_caching_and_celery.md))
40. **Scale reads?** Caching, read replicas (database routers), CDN, denormalised counters.
