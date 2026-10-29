from typing import Any

from rest_framework.permissions import SAFE_METHODS, BasePermission
from rest_framework.request import Request
from rest_framework.views import APIView


class IsClientOrReadOnly(BasePermission):
    """Anyone may read; only users with the CLIENT role may create projects."""

    def has_permission(self, request: Request, view: APIView) -> bool:
        if request.method in SAFE_METHODS:
            return True
        return bool(getattr(request.user, "is_client", False))


class IsOwnerOrReadOnly(BasePermission):
    """Object-level: only the project's client may change or delete it."""

    def has_object_permission(self, request: Request, view: APIView, obj: Any) -> bool:
        if request.method in SAFE_METHODS:
            return True
        return bool(obj.client_id == request.user.pk)
