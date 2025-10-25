from django.urls import reverse
from django.contrib.auth import get_user_model  # Импортируем функцию получения модели пользователя
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from habit.models import Habit  # Предполагаю, что модель находится в приложении habit
from habit.paginators import CustomPagination
from users.models import CustomUser

from rest_framework import status
from django.utils import timezone



class HabitViewSetTestCase(APITestCase):
    def setUp(self):
        User = get_user_model()  # Получаем актуальную модель пользователя

        # Создаем тестового пользователя
        self.user = User.objects.create_user(
            username='testuser',
            password='123456',
            email='testuser@example.com'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        # Создаем тестовые данные со всеми полями модели
        self.habit_data = {
            'place': 'Дом',
            'time': '08:00:00',  # Время в формате HH:MM:SS
            'action': 'Утренняя зарядка',
            'is_pleasant': False,
            'linked_habit': None,
            'periodicity': 1,
            'reward': 'Хорошее настроение',
            'execution_time': 2,  # В минутах
            'is_public': True
        }

    def test_create_habit(self):
        # Создаем приятную привычку для связи
        pleasant_habit_data = {
            'place': 'Дом',
            'time': '09:00:00',
            'action': 'Приятная привычка',
            'is_pleasant': True,
            'periodicity': 1,
            'reward': '',  # Для приятной привычки награда не нужна
            'execution_time': 2,  # В минутах
            'is_public': True
        }

        # Создаем приятную привычку
        pleasant_response = self.client.post(
            reverse('habit:habits-list'),
            pleasant_habit_data,
            format='json'
        )

        # Выводим ошибки валидации, если они есть
        if pleasant_response.status_code == 400:
            print("Ошибки валидации при создании приятной привычки:")
            print(pleasant_response.data)

        # Проверяем успешность создания приятной привычки
        self.assertEqual(pleasant_response.status_code, status.HTTP_201_CREATED)
        pleasant_habit_id = pleasant_response.data['id']

        # Создаем основную привычку с ссылкой на приятную
        self.habit_data = {
            'place': 'Дом',
            'time': '08:00:00',
            'action': 'Утренняя зарядка',
            'is_pleasant': False,
            'linked_habit': pleasant_habit_id,
            'periodicity': 1,
            'reward': 'Хорошее настроение',
            'execution_time': 2,  # В минутах
            'is_public': True
        }

        response = self.client.post(
            reverse('habit:habits-list'),
            self.habit_data,
            format='json'
        )

        # Выводим ошибки валидации, если они есть
        if response.status_code == 400:
            print("Ошибки валидации при создании основной привычки:")
            print(response.data)

        # Проверяем, что статус ответа корректный
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Добавляем проверку данных
        self.assertEqual(response.data['execution_time'], 2)
        self.assertEqual(response.data['place'], 'Дом')
        self.assertEqual(response.data['action'], 'Утренняя зарядка')
        self.assertEqual(response.data['linked_habit'], pleasant_habit_id)

    def test_create_habit_with_invalid_execution_time(self):
        invalid_data = self.habit_data.copy()
        invalid_data['execution_time'] = 3  # Превышает 2 минуты

        response = self.client.post(
            reverse('habit:habits-list'),
            invalid_data,
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('execution_time', response.data)
        self.assertEqual(
            response.data['execution_time'][0],
            'Время выполнения не должно превышать 2 минуты'
        )

    def test_validation_execution_time(self):
        """Тест валидации времени выполнения"""
        invalid_data = self.habit_data.copy()
        invalid_data['execution_time'] = 3  # Невалидное значение

        response = self.client.post(reverse('habit-list'), invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('execution_time', response.data)

    def test_pleasant_habit_validation(self):
        """Тест валидации приятной привычки"""
        pleasant_data = self.habit_data.copy()
        pleasant_data['is_pleasant'] = True
        pleasant_data['linked_habit'] = None  # Приятная привычка не может иметь связанной

        # Создаем приятную привычку
        response = self.client.post(reverse('habit:habit-list'), pleasant_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Пытаемся создать связанную привычку для приятной
        linked_habit = Habit.objects.first()
        invalid_data = pleasant_data.copy()
        invalid_data['linked_habit'] = linked_habit.id

        # Отправляем запрос
        response = self.client.post(reverse('habit:habit-list'), invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Проверяем наличие ошибки в non_field_errors
        self.assertIn('non_field_errors', response.data)
        self.assertEqual(
            str(response.data['non_field_errors'][0]),
            'ID связанной привычки должен быть числом'
        )

    def test_list_habits(self):
        """Тест получения списка привычек"""
        Habit.objects.create(user=self.user, **self.habit_data)
        response = self.client.get(reverse('habit:habit-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)

    def test_retrieve_habit(self):
        """Тест получения отдельной привычки"""
        habit = Habit.objects.create(user=self.user, **self.habit_data)
        # Используем правильный URL для получения конкретного объекта
        response = self.client.get(reverse('habit:habit-detail', kwargs={'pk': habit.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Проверяем корректность возвращаемых данных
        self.assertEqual(response.data['action'], self.habit_data['action'])  # Используем существующее поле action
        self.assertEqual(response.data['place'], self.habit_data['place'])  # Используем существующее поле place
        self.assertEqual(response.data['id'], habit.pk)

    def test_update_habit(self):
        """Тест обновления привычки"""
        # Создаем привычку с тестовыми данными
        habit = Habit.objects.create(user=self.user, **self.habit_data)

        # Выбираем поле, которое реально существует в модели
        updated_data = {'action': 'Новое действие'}  # Используем существующее поле action

        # Используем правильный URL и kwargs
        response = self.client.patch(
            reverse('habit:habit-detail', kwargs={'pk': habit.pk}),
            updated_data,
            format='json'
        )

        # Проверяем статус ответа
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Проверяем, что поле обновилось
        self.assertEqual(response.data['action'], updated_data['action'])

        # Дополнительно можно проверить сохранение в базе
        habit.refresh_from_db()
        self.assertEqual(habit.action, updated_data['action'])

    def test_delete_habit(self):
        """Тест удаления привычки"""
        habit = Habit.objects.create(user=self.user, **self.habit_data)
        response = self.client.delete(reverse('habit:habit-detail', args=[habit.pk]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Habit.objects.count(), 0)

    def test_permission_denied(self):
        """Тест проверки разрешений"""
        # Создаем другого пользователя
        other_user = CustomUser.objects.create_user(username='otheruser', password='123456')
        other_client = APIClient()
        other_client.force_authenticate(user=other_user)

        habit = Habit.objects.create(user=self.user, **self.habit_data)
        response = other_client.delete(reverse('habit:habit-detail', args=[habit.pk]))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_validation(self):
        """Тест валидации данных"""
        invalid_data = {
            'place': 'Место',  # недостаточно полей для создания
        }
        response = self.client.post(reverse('habit:habit-list'), invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_filtering(self):
        """Тест фильтрации публичных привычек"""
        # Создаем публичные и непубличные привычки
        Habit.objects.create(
            user=self.user,
            action='Публичная привычка',  # используем существующее поле action
            time='12:00:00',  # добавляем обязательное поле time
            place='Место',  # добавляем обязательное поле place
            is_public=True
        )
        Habit.objects.create(
            user=self.user,
            action='Приватная привычка',  # используем существующее поле action
            time='12:00:00',  # добавляем обязательное поле time
            place='Место',  # добавляем обязательное поле place
            is_public=False
        )

        # Фильтрация публичных привычек
        response = self.client.get(reverse('habit:habit-list') + '?is_public=true')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)
        self.assertTrue(response.data[0]['is_public'])

        # Фильтрация всех привычек пользователя
        response = self.client.get(reverse('habit:habit-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_pagination(self):
        """Тест пагинации"""
        # Создаем много привычек для тестирования пагинации
        for i in range(100):
            Habit.objects.create(
                user=self.user,
                action=f'Привычка {i}',  # используем существующее поле action
                time='12:00:00',  # добавляем обязательное поле time
                place='Место',  # добавляем обязательное поле place
                is_public=True
            )

        response = self.client.get(reverse('habit:habit-list'))
        self.assertTrue('next' in response.data)
        self.assertEqual(len(response.data['results']), CustomPagination.page_size)

    def test_unauthenticated_access(self):
        """Тест доступа без аутентификации"""
        self.client.force_authenticate(user=None)

        # Проверка POST
        response = self.client.post(reverse('habit:habit-list'), self.habit_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Проверка GET
        habit = Habit.objects.create(user=self.user, **self.habit_data)
        response = self.client.get(reverse('habit:habit-detail', args=[habit.pk]))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_public_habit_access(self):
        """Тест доступа к публичным привычкам неавторизованным пользователем"""
        # Создаем публичную привычку
        public_habit = Habit.objects.create(
            user=self.user,
            action='Публичная привычка',  # используем существующее поле action
            time='12:00:00',  # добавляем обязательное поле time
            place='Место',  # добавляем обязательное поле place
            is_public=True
        )

        # Авторизованный пользователь
        response = self.client.get(reverse('habit:habit-detail', args=[public_habit.pk]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Неавторизованный пользователь
        self.client.force_authenticate(user=None)
        response = self.client.get(reverse('habit:habit-detail', args=[public_habit.pk]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_private_habit_access(self):
        """Тест доступа к приватным привычкам неавторизованным пользователем"""
        # Создаем приватную привычку
        private_habit = Habit.objects.create(
            user=self.user,
            action='Приватная привычка',  # используем существующее поле action
            time='12:00:00',  # добавляем обязательное поле time
            place='Место',  # добавляем обязательное поле place
            is_public=False
        )

        # Неавторизованный пользователь
        self.client.force_authenticate(user=None)
        response = self.client.get(reverse('habit:habit-detail', args=[private_habit.pk]))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Другой авторизованный пользователь
        other_user = CustomUser.objects.create_user(username='otheruser', password='123456')
        self.client.force_authenticate(user=other_user)
        response = self.client.get(reverse('habit:habit-detail', args=[private_habit.pk]))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def tearDown(self):
        """Очистка после тестов"""
        Habit.objects.all().delete()
        CustomUser.objects.all().delete()

