from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOrOwnerOrReadOnly(BasePermission):
    """
    Создание / Редактирование / Удаление доступно только для администрации
    или автора
    """
    owner_field_name = 'author'

    def has_object_permission(self, request, view, obj):
        return bool(
            request.method in SAFE_METHODS or (
                request.user and (
                    request.user.is_staff or
                    getattr(obj, owner_field_name) == request.user
                )
            )
        )


class IsAdminOrReadOnly(BasePermission):
    """
    Создание / Редактирование / Удаление доступно только для администрации
    """

    def has_permission(self, request, view):
        return bool(
            request.method in SAFE_METHODS or
            request.user and request.user.is_staff
        )
