from rest_framework import serializers
from .models import Habit
from .validators import (
    validate_linked_habit_and_reward,
    validate_linked_habit,
    validate_pleasant_habit,
    validate_periodicity,
    validate_execution_time
)


class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = [
            'id',
            'user',
            'place',
            'time',
            'action',
            'is_pleasant',
            'linked_habit',
            'periodicity',
            'reward',
            'execution_time',
            'is_public'
        ]
        read_only_fields = ['user']

    def validate(self, data):
        # Базовая валидация
        validate_linked_habit_and_reward(data)
        validate_pleasant_habit(data)

        # Дополнительная валидация при наличии связанной привычки
        if 'linked_habit' in data:
            validate_linked_habit(data)

        # Валидация периодичности
        if 'periodicity' in data:
            validate_periodicity(data)

        # Валидация времени выполнения
        if 'execution_time' in data:
            validate_execution_time(data)

        return data
