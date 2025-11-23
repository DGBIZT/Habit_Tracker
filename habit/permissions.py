from rest_framework import permissions


class IsAuthenticatedOrPublic(permissions.BasePermission):
    """
    Разрешение, позволяющее:
    - Публичный доступ для SAFE_METHODS (GET, HEAD, OPTIONS) к публичным объектам
    - Аутентифицированный доступ для остальных методов
    """

    def has_permission(self, request, view):
        # Проверка на уровне запроса
        if request.method in permissions.SAFE_METHODS:
            return True  # Публичные данные доступны всем для чтения
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Проверка на уровне объекта
        if request.method in permissions.SAFE_METHODS:
            # Для публичных методов проверяем публичность объекта или владение
            return obj.is_public or (request.user and obj.user == request.user)
        # Для остальных методов только владелец может изменять объект
        return request.user and obj.user == request.user
