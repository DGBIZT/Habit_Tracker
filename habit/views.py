from django.core.exceptions import PermissionDenied
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Habit
from .serializers import HabitSerializer
from .paginators import CustomPagination
from .permissions import IsAuthenticatedOrPublic


class HabitViewSet(viewsets.ModelViewSet):
    """Управление привычками"""
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticatedOrPublic]
    pagination_class = CustomPagination  # Используем импортированную пагинацию
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['is_public']  # разрешаем фильтрацию по публичности
    search_fields = ['action', 'place']  # добавляем поиск по полям

    def perform_create(self, serializer):
        # Просто сохраняем объект с текущим пользователем
        serializer.save(user=self.request.user)

    def get_queryset(self):
        if self.action == 'list':
            if self.request.query_params.get('public') == 'true':
                return Habit.objects.filter(is_public=True)
            return Habit.objects.filter(user=self.request.user)
        return super().get_queryset()

    def check_object_permissions(self, request, obj):
        super().check_object_permissions(request, obj)
        if request.method in ['PUT', 'PATCH', 'DELETE']:
            if obj.user != request.user:
                raise PermissionDenied("У вас нет прав на изменение этой привычки")

    def perform_destroy(self, instance):
        if instance.user != self.request.user:
            raise PermissionDenied("У вас нет прав на удаление этой привычки")
        return super().perform_destroy(instance)

    def retrieve(self, request, *args, **kwargs):
        habit = self.get_object()
        if not habit.is_public and habit.user != request.user:
            raise PermissionDenied("У вас нет прав на просмотр этой привычки")
        return super().retrieve(request, *args, **kwargs)
