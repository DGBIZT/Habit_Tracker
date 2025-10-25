from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

User = get_user_model()


def validate_execution_time(value):
    if value > 2:
        raise ValidationError('Время выполнения не должно превышать 2 минуты')


class Habit(models.Model):
    # 1. Пользователь — создатель привычки
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='habits',
        verbose_name='Пользователь'
    )

    # 2. Место выполнения
    place = models.CharField(
        max_length=255,
        verbose_name='Место'
    )

    # 3. Время выполнения
    time = models.TimeField(
        verbose_name='Время'
    )

    # 4. Действие
    action = models.CharField(
        max_length=255,
        verbose_name='Действие'
    )

    # 5. Признак приятной привычки
    is_pleasant = models.BooleanField(
        default=False,
        verbose_name='Приятная привычка'
    )

    # 6. Связанная привычка
    linked_habit = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Связанная привычка',
        related_name='linked_habits'
    )

    # 7. Периодичность (по умолчанию ежедневная)
    periodicity = models.PositiveIntegerField(
        default=1,  # 1 день = ежедневно
        verbose_name='Периодичность (в днях)'
    )

    # 8. Вознаграждение
    reward = models.CharField(
        max_length=255,
        verbose_name='Вознаграждение'
    )

    # 9. Время на выполнение
    execution_time = models.PositiveIntegerField(
        default=2,
        verbose_name='Время выполнения (в минутах)',
        validators=[validate_execution_time]  # Используем обычную функцию
    )

    # 10. Признак публичности
    is_public = models.BooleanField(
        default=False,
        verbose_name='Публичность'
    )

    class Meta:
        verbose_name = 'Привычка'
        verbose_name_plural = 'Привычки'
        ordering = ['-id']

    def __str__(self):
        return f"{self.action} в {self.time} в {self.place}"

    def clean(self):
        if self.is_pleasant and self.linked_habit:
            raise ValidationError({'linked_habit': 'Приятные привычки не могут иметь связанных'})


class Notification(models.Model):
    habit = models.ForeignKey(Habit, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=[('sent', 'Отправлено'), ('error', 'Ошибка')])
    error_message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)