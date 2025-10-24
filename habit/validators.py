from django.core.exceptions import ValidationError
from .models import Habit

def validate_linked_habit_and_reward(habit):
    if habit.linked_habit and habit.reward:
        raise ValidationError("Нельзя одновременно указывать связанную привычку и вознаграждение")

def validate_linked_habit(habit):
    if habit.linked_habit:
        if not habit.linked_habit.is_pleasant:
            raise ValidationError("Связанные привычки могут быть только приятными")

def validate_pleasant_habit(habit):
    if habit.is_pleasant:
        if habit.linked_habit or habit.reward:
            raise ValidationError("У приятной привычки не может быть вознаграждения или связанной привычки")

def validate_periodicity(habit):
    if habit.periodicity > 7:
        raise ValidationError("Нельзя выполнять привычку реже, чем 1 раз в 7 дней")

def validate_execution_time(habit):
    if habit.execution_time > 120:
        raise ValidationError("Время выполнения не может превышать 120 секунд")
