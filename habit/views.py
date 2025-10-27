from django.core.exceptions import PermissionDenied
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Habit
from .serializers import HabitSerializer
from .paginators import CustomPagination
from .permissions import IsAuthenticatedOrPublic

class UserHabitViewSet(viewsets.ModelViewSet):
    """Управление привычками текущего пользователя"""
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticatedOrPublic]
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['action', 'place']

    def get_queryset(self):
        return Habit.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def check_object_permissions(self, request, obj):
        # Проверяем права через существующее разрешение
        super().check_object_permissions(request, obj)
        if request.method in ['PUT', 'PATCH', 'DELETE']:
            if obj.user != request.user:
                raise PermissionDenied("У вас нет прав на изменение этой привычки")

    def perform_destroy(self, instance):
        if instance.user != self.request.user:
            raise PermissionDenied("У вас нет прав на удаление этой привычки")
        return super().perform_destroy(instance)


class PublicHabitViewSet(viewsets.ReadOnlyModelViewSet):
    """Просмотр публичных привычек"""
    queryset = Habit.objects.filter(is_public=True)
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticatedOrPublic]
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['action', 'place']

    def retrieve(self, request, *args, **kwargs):
        habit = self.get_object()
        if not habit.is_public:
            raise PermissionDenied("Эта привычка не является публичной")
        return super().retrieve(request, *args, **kwargs)
