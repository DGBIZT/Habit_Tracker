from django.core.management.base import BaseCommand
from habit.models import Habit
from django.contrib.auth import get_user_model  # Используем get_user_model
from django.utils import timezone
import random


# Получаем актуальную модель пользователя
User = get_user_model()


class Command(BaseCommand):
    help = 'Заполняет базу данных тестовыми привычками'

    def handle(self, *args, **kwargs):
        # Проверяем наличие пользователей
        if not User.objects.exists():
            # Создаем тестового пользователя
            user = User.objects.create_user(
                username='testuser',
                password='1234',
                email='test@example.com'
            )
        else:
            # Берем первого найденного пользователя
            user = User.objects.first()

        # Массивы для генерации случайных данных
        places = ['Дома', 'Офис', 'Парк', 'Спортзал', 'Кафе']
        actions = [
            'Утренняя зарядка',
            'Планирование задач',
            'Чтение книги',
            'Медитация',
            'Пробежка',
            'Йога'
        ]
        rewards = [
            'Хорошее настроение',
            'Эффективный день',
            'Отдых',
            'Прогресс',
            'Бонус от босса'
        ]

        # Создаем 10 случайных привычек
        for i in range(10):
            habit = Habit.objects.create(
                user=user,
                place=random.choice(places),
                time=timezone.now().time(),
                action=random.choice(actions),
                is_pleasant=random.choice([True, False]),
                linked_habit=Habit.objects.first() if random.choice([True, False]) else None,
                periodicity=random.randint(1, 7),
                reward=random.choice(rewards),
                execution_time=random.randint(5, 20),
                is_public=random.choice([True, False])
            )

            self.stdout.write(self.style.SUCCESS(f'Создана привычка: {habit.action}'))

        self.stdout.write(self.style.SUCCESS('Заполнение базы данных завершено'))
