from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import Habit
from .validators import (
    validate_linked_habit_and_reward,
    validate_pleasant_habit,
    validate_periodicity,
    validate_execution_time,
    validate_linked_habit,
)


class HabitSerializer(serializers.ModelSerializer):
    reward = serializers.CharField(required=False, allow_blank=True, allow_null=True)  # Добавляем настройки для reward

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

    def validate_reward(self, value):
        # Преобразуем пустую строку в None
        if value == '':
            return None
        return value

    def validate(self, data):
        errors = {}

        # Сначала проверяем, что приятная привычка не может быть связана
        try:
            validate_pleasant_habit(data)
        except ValidationError as e:
            errors['pleasant_habit'] = str(e)

        # Затем проверяем остальные валидации
        try:
            validate_linked_habit(data)
        except ValidationError as e:
            errors['linked_habit'] = str(e)

        try:
            validate_linked_habit_and_reward(data)
        except ValidationError as e:
            errors['linked_habit_and_reward'] = str(e)

        try:
            validate_periodicity(data)
        except ValidationError as e:
            errors['periodicity'] = str(e)

        try:
            validate_execution_time(data)
        except ValidationError as e:
            errors['execution_time'] = str(e)

        # Дополнительная проверка для приятной привычки
        if data.get('is_pleasant') and data.get('reward'):
            errors['reward'] = 'Приятная привычка не может иметь награду'

        if errors:
            raise serializers.ValidationError(errors)

        return data
