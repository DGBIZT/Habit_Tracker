from django.core.exceptions import PermissionDenied, ValidationError
from rest_framework import viewsets, permissions
from django_filters.rest_framework import DjangoFilterBackend
from .models import Habit
from .serializers import HabitSerializer
from .paginators import CustomPagination
from .validators import validate_linked_habit_and_reward, validate_pleasant_habit, validate_linked_habit, validate_periodicity, validate_execution_time


class HabitViewSet(viewsets.ModelViewSet):
    """Управление привычками"""
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomPagination  # Используем импортированную пагинацию
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['is_public']

    def perform_create(self, serializer):
        try:
            habit = serializer.save(user=self.request.user)
            # Дополнительная валидация после сохранения
            validate_linked_habit_and_reward(habit)
            validate_pleasant_habit(habit)
            validate_linked_habit(habit)
            validate_periodicity(habit)
            validate_execution_time(habit)
        except ValidationError as e:
            raise PermissionDenied(str(e))

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
