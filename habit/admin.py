from django.contrib import admin
from .models import Habit

@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'action',
        'time',
        'place',
        'is_pleasant',
        'linked_habit',
        'periodicity',
        'reward',
        'execution_time',
        'is_public'
    )
    search_fields = ('action', 'place', 'reward')
    list_filter = ('is_pleasant', 'is_public')
    # Убрали created_at из readonly_fields
    fieldsets = (
        (None, {
            'fields': ('user', 'action', 'time', 'place')
        }),
        ('Характеристики привычки', {
            'fields': ('is_pleasant', 'linked_habit', 'periodicity', 'reward', 'execution_time')
        }),
        ('Настройки', {
            'fields': ('is_public',)
        })
    )
