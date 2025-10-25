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

from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from .models import Habit
from .validators import (
    validate_linked_habit_and_reward,
    validate_pleasant_habit,
    validate_periodicity,
    validate_execution_time,
    validate_linked_habit,
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
        errors = {}

        # Валидация связанной привычки
        try:
            validate_linked_habit(data)
        except ValidationError as e:
            errors['linked_habit'] = str(e)

        # Валидация связанных привычек и награды
        try:
            validate_linked_habit_and_reward(data)
        except ValidationError as e:
            errors['linked_habit_and_reward'] = str(e)

        # Валидация приятной привычки
        try:
            validate_pleasant_habit(data)
        except ValidationError as e:
            errors['pleasant_habit'] = str(e)

        # Валидация периодичности
        try:
            validate_periodicity(data)
        except ValidationError as e:
            errors['periodicity'] = str(e)

        # Валидация времени выполнения
        try:
            validate_execution_time(data)
        except ValidationError as e:
            errors['execution_time'] = str(e)

        if errors:
            raise serializers.ValidationError(errors)

        return data
