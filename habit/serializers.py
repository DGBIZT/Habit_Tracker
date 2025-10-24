from rest_framework import serializers
from .models import Habit

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