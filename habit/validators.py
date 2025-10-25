from django.core.exceptions import ValidationError
from .models import Habit


def validate_linked_habit_and_reward(data):
    # Получаем значения из словаря
    linked_habit = data.get('linked_habit')
    reward = data.get('reward')

    # Проверяем условия
    if linked_habit and reward:
        raise ValidationError("Нельзя одновременно указывать связанную привычку и награду")


# validators.py
def validate_linked_habit(data):
    linked_habit_id = data.get('linked_habit')

    # Проверяем, что linked_habit_id является числом
    if linked_habit_id is not None:
        if not isinstance(linked_habit_id, int):
            raise ValidationError("ID связанной привычки должен быть числом")

        try:
            linked_habit = Habit.objects.get(pk=linked_habit_id)
            if not linked_habit.is_pleasant:
                raise ValidationError("Связанные привычки должны быть приятными")
        except Habit.DoesNotExist:
            raise ValidationError("Связанная привычка не найдена")


def validate_pleasant_habit(data):
    # Получаем значение из словаря
    is_pleasant = data.get('is_pleasant')
    linked_habit_id = data.get('linked_habit')

    if linked_habit_id and is_pleasant:
        raise ValidationError("Приятная привычка не может быть связана с другой привычкой")

# validators.py
def validate_periodicity(data):
    periodicity = data.get('periodicity')
    if periodicity is not None:
        if periodicity <= 0:
            raise ValidationError("Периодичность должна быть положительным числом")
        if periodicity > 7:
            raise ValidationError("Периодичность не может превышать 7 дней")


# validators.py
def validate_execution_time(data):
    execution_time = data.get('execution_time')
    if execution_time is not None:
        if execution_time <= 0:
            raise ValidationError("Время выполнения должно быть положительным числом")
        if execution_time > 120:
            raise ValidationError("Время выполнения не может превышать 120 секунд")

