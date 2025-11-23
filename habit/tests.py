from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from habit.models import Habit


class HabitViewSetTestCase(APITestCase):
    def setUp(self):
        super().setUp()
        Habit.objects.all().delete()  # Очищаем все привычки перед тестом
        # Создаем тестового пользователя
        self.user = get_user_model().objects.create_user(
            username='testuser',
            password='123456',
            email='testuser@example.com'
        )
        self.client.force_authenticate(user=self.user)

        # Базовые данные для создания привычки
        self.base_habit_data = {
            'place': 'Дом',
            'time': '08:00:00',
            'action': 'Утренняя зарядка',
            'is_pleasant': False,
            'linked_habit': None,
            'periodicity': 1,
            'reward': 'Хорошее настроение',
            'execution_time': 2,
            'is_public': True
        }

    def test_create_user_habit(self):
        # Используем полное имя URL с namespace
        response = self.client.post(
            reverse('habit:user-habit-list'),  # Важно: habit:user-habit-list
            self.base_habit_data,
            format='json'
        )

        # Проверяем успешность создания
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['user'], self.user.id)

        # Проверяем корректность сохраненных данных
        self.assertEqual(response.data['execution_time'], 2)
        self.assertEqual(response.data['place'], 'Дом')
        self.assertEqual(response.data['action'], 'Утренняя зарядка')

    def test_create_pleasant_habit(self):
        # Создаем приятную привычку
        pleasant_habit_data = {
            **self.base_habit_data,
            'is_pleasant': True,
            'linked_habit': None
        }

        # Удаляем поле reward полностью
        del pleasant_habit_data['reward']

        # Важно: используем правильное имя URL
        response = self.client.post(
            reverse('habit:user-habit-list'),
            pleasant_habit_data,
            format='json'
        )

        # Добавляем вывод ошибок для отладки
        if response.status_code != status.HTTP_201_CREATED:
            print("Response data:", response.data)
            print("Response errors:", response.json())

        # Проверяем успешность создания
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response.data['is_pleasant'])

        # Дополнительные проверки
        self.assertEqual(response.data['user'], self.user.id)
        self.assertEqual(response.data['action'], pleasant_habit_data['action'])

    # def test_create_habit_with_linked(self):
    #     # Создаём приятную привычку
    #     pleasant_habit_data = {
    #         **self.base_habit_data,
    #         'is_pleasant': True,
    #         'reward': 'Моральное удовлетворение',
    #         'linked_habit': None,
    #         'place': 'Дом',
    #         'time': '10:00:00',
    #         'action': 'Утренняя зарядка',
    #         'periodicity': 1,
    #         'execution_time': 2,
    #         'is_public': False
    #     }
    #
    #     try:
    #         # Получаем URL
    #         pleasant_url = reverse('habit:user-habit-list')
    #         print(f"Полученный URL: {pleasant_url}")
    #
    #         # Отправляем POST запрос для приятной привычки
    #         pleasant_response = self.client.post(
    #             pleasant_url,
    #             pleasant_habit_data,
    #             format='json'
    #         )
    #
    #         # Проверяем статус ответа
    #         self.assertEqual(pleasant_response.status_code, status.HTTP_201_CREATED)
    #         pleasant_id = int(pleasant_response.data['id'])
    #         print(f"Создан ID приятной привычки: {pleasant_id}")
    #
    #         # В тестовом методе
    #         linked_habit_data = {
    #             **self.base_habit_data,
    #             'is_pleasant': False,
    #             'linked_habit': pleasant_id,  # Указываем ID связанной привычки
    #             'place': 'Офис',
    #             'time': '15:00:00',
    #             'action': 'Уборка рабочего места',
    #             'periodicity': 1,
    #             'execution_time': 2,
    #             'is_public': False
    #             # Убираем поле reward, так как есть связанная привычка
    #         }
    #
    #         print(f"Данные для связанной привычки: {linked_habit_data}")
    #         print(f"Тип linked_habit: {type(linked_habit_data['linked_habit'])}")
    #
    #         # Получаем URL для второй привычки
    #         linked_url = reverse('habit:user-habit-list')
    #         print(f"URL для связанной привычки: {linked_url}")
    #
    #         # Отправляем второй POST запрос
    #         response = self.client.post(
    #             linked_url,
    #             linked_habit_data,
    #             format='json'
    #         )
    #
    #         # Выводим ошибки валидации для второго запроса
    #         if response.status_code != status.HTTP_201_CREATED:
    #             print("Ошибки валидации для связанной привычки:", response.data)
    #             print("Статус ответа:", response.status_code)
    #
    #         # Проверяем успешность создания
    #         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    #         self.assertEqual(response.data['linked_habit'], pleasant_id)
    #
    #         # Дополнительные проверки
    #         self.assertEqual(response.data['user'], self.user.id)
    #         self.assertEqual(response.data['action'], linked_habit_data['action'])
    #
    #     except Exception as e:
    #         print(f"Произошла ошибка: {e}")
    #         raise

    def test_create_pleasant_with_link_fails(self):
        # Создаем обычную привычку
        base_habit_response = self.client.post(
            reverse('habit:user-habit-list'),
            self.base_habit_data,
            format='json'
        )
        base_id = base_habit_response.data['id']

        # Пытаемся создать приятную привычку со ссылкой
        pleasant_with_link_data = {
            **self.base_habit_data,
            'is_pleasant': True,
            'linked_habit': base_id
        }

        response = self.client.post(
            reverse('habit:user-habit-list'),
            pleasant_with_link_data,
            format='json'
        )

        # Проверяем результат
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('non_field_errors', response.data)
        self.assertEqual(
            response.data['non_field_errors'][0],
            'Приятная привычка не может быть связана с другой привычкой'
        )

    # Тест на обновление привычки
    def test_update_habit(self):
        # Создаем привычку
        response = self.client.post(
            reverse('habit:user-habit-list'),
            self.base_habit_data,
            format='json'
        )
        habit_id = response.data['id']

        # Обновляем данные
        updated_data = {
            **self.base_habit_data,
            'action': 'Обновленное действие'
        }

        # Отправляем PUT запрос
        response = self.client.put(
            reverse('habit:user-habit-detail', kwargs={'pk': habit_id}),
            updated_data,
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['action'], 'Обновленное действие')

    # Тест на удаление привычки
    def test_delete_habit(self):
        # Проверяем, что base_habit_data существует
        if not hasattr(self, 'base_habit_data'):
            raise AssertionError("base_habit_data не определен в тестовом классе")

        # Создаем привычку
        response = self.client.post(
            reverse('habit:user-habit-list'),
            self.base_habit_data,  # Используем base_habit_data
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)  # Добавляем проверку создания
        habit_id = response.data['id']

        # Проверяем, что привычка действительно создана
        created_habit = Habit.objects.get(id=habit_id)
        self.assertEqual(created_habit.user, self.user)  # Проверяем связь с пользователем

        # Удаляем привычку
        delete_response = self.client.delete(
            reverse('habit:user-habit-detail', kwargs={'pk': habit_id})
        )

        # Проверяем статус удаления
        self.assertEqual(delete_response.status_code, status.HTTP_204_NO_CONTENT)

        # Проверяем, что привычка удалена из базы данных
        with self.assertRaises(Habit.DoesNotExist):
            Habit.objects.get(id=habit_id)

    # Тест на получение списка привычек
    def test_list_habits(self):
        # Создаем несколько привычек
        for i in range(3):
            self.client.post(
                reverse('habit:user-habit-list'),
                self.base_habit_data,
                format='json'
            )

        # Получаем список
        response = self.client.get(
            reverse('habit:user-habit-list')
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)

    # Тест на фильтрацию привычек!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # def test_filter_habits(self):
    #     # Очищаем базу данных перед тестом
    #     Habit.objects.all().delete()
    #
    #     # Создаем привычки
    #     response1 = self.client.post(
    #         reverse('habit:user-habit-list'),
    #         {**self.base_habit_data, 'action': 'Утренняя зарядка'},
    #         format='json'
    #     )
    #     self.assertEqual(response1.status_code, status.HTTP_201_CREATED)
    #
    #     response2 = self.client.post(
    #         reverse('habit:user-habit-list'),
    #         {**self.base_habit_data, 'action': 'Вечерняя прогулка'},
    #         format='json'
    #     )
    #     self.assertEqual(response2.status_code, status.HTTP_201_CREATED)
    #
    #     # Проверяем общее количество привычек
    #     all_habits = self.client.get(reverse('habit:user-habit-list'))
    #     self.assertEqual(len(all_habits.data), 2)
    #
    #     # Фильтруем по действию
    #     response = self.client.get(
    #         reverse('habit:user-habit-list') + '?search=зарядка'
    #     )
    #
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(len(response.data), 1)  # Ожидаем только одну запись
    #
    #     # Проверяем содержимое
    #     if response.data:
    #         self.assertEqual(response.data[0]['action'], 'Утренняя зарядка')
    #     else:
    #         self.fail("Фильтрация не вернула ожидаемых результатов")

        # Тест на публичные привычки

    def test_public_habits(self):
        # Создаем публичную привычку
        public_habit_data = {
            **self.base_habit_data,
            'is_public': True
        }
        response = self.client.post(
            reverse('habit:user-habit-list'),
            public_habit_data,
            format='json'
        )
        habit_id = response.data['id']

        # Получаем через публичный endpoint
        response = self.client.get(
            reverse('habit:public-habit-detail', kwargs={'pk': habit_id})
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['is_public'], True)

    # Тест на проверку прав доступа для публичных привычек
    def test_public_habits_permissions(self):
        # Создаем приватную привычку
        private_habit_data = {
            **self.base_habit_data,
            'is_public': False
        }
        response = self.client.post(
            reverse('habit:user-habit-list'),
            private_habit_data,
            format='json'
        )
        habit_id = response.data['id']

        # Пытаемся получить через публичный endpoint
        response = self.client.get(
            reverse('habit:public-habit-detail', kwargs={'pk': habit_id})
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # Тест на проверку прав доступа для чужого контента

    def test_permission_denied_for_other_user(self):
        # Создаем второго пользователя
        other_user = get_user_model().objects.create_user(
            username='otheruser',
            password='123456',
            email='other@example.com'
        )

        # Создаем привычку от имени первого пользователя
        response = self.client.post(
            reverse('habit:user-habit-list'),
            self.base_habit_data,
            format='json'
        )
        habit_id = response.data['id']

        # Авторизуемся как другой пользователь
        self.client.force_authenticate(user=other_user)

        # Пытаемся получить привычку
        response = self.client.get(
            reverse('habit:user-habit-detail', kwargs={'pk': habit_id})
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # Пытаемся обновить привычку
        response = self.client.put(
            reverse('habit:user-habit-detail', kwargs={'pk': habit_id}),
            self.base_habit_data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # Пытаемся удалить привычку
        response = self.client.delete(
            reverse('habit:user-habit-detail', kwargs={'pk': habit_id})
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # Тест на валидацию периодичности
    def test_periodicity_validation(self):
        # Проверяем минимальную периодичность
        invalid_periodicity_data = {
            **self.base_habit_data,
            'periodicity': 0
        }
        response = self.client.post(
            reverse('habit:user-habit-list'),
            invalid_periodicity_data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Проверяем наличие ошибки в non_field_errors
        self.assertIn('non_field_errors', response.data)
        self.assertIn(
            'Периодичность должна быть положительным числом',
            str(response.data['non_field_errors'])
        )

        # Проверяем максимальную периодичность
        invalid_periodicity_data = {
            **self.base_habit_data,
            'periodicity': 8
        }
        response = self.client.post(
            reverse('habit:user-habit-list'),
            invalid_periodicity_data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Проверяем наличие ошибки в non_field_errors
        self.assertIn('non_field_errors', response.data)
        self.assertIn(
            'Периодичность не может превышать 7 дней',
            str(response.data['non_field_errors'])
        )

    def test_execution_time_validation(self):
        # Создаем базовые валидные данные со всеми обязательными полями
        base_habit_data = {
            'place': 'Дом',
            'time': '12:00:00',  # Время в формате HH:MM:SS
            'action': 'Новая привычка',
            'is_pleasant': False,
            'periodicity': 1,
            'reward': 'Вознаграждение',
            'execution_time': 2,  # В минутах
            'is_public': False
        }

        # Проверяем минимальное время (0)
        invalid_time_data_min = {
            **base_habit_data,
            'execution_time': 0
        }
        response = self.client.post(
            reverse('habit:user-habit-list'),
            invalid_time_data_min,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Проверяем ошибку для минимального значения
        if 'execution_time' in response.data:
            self.assertIn(
                'Время выполнения должно быть положительным числом',
                str(response.data['execution_time'])
            )
        elif 'non_field_errors' in response.data:
            self.assertIn(
                'Время выполнения должно быть положительным числом',
                str(response.data['non_field_errors'])
            )
        else:
            self.fail("Ошибка валидации не найдена в ожидаемых местах")

        # Проверяем максимальное время (3 минуты)
        invalid_time_data_max = {
            **base_habit_data,
            'execution_time': 3
        }
        response = self.client.post(
            reverse('habit:user-habit-list'),
            invalid_time_data_max,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Проверяем ошибку для максимального значения
        if 'execution_time' in response.data:
            self.assertIn(
                'Время выполнения не должно превышать 2 минуты',
                str(response.data['execution_time'])
            )
        elif 'non_field_errors' in response.data:
            self.assertIn(
                'Время выполнения не должно превышать 2 минуты',
                str(response.data['non_field_errors'])
            )
        else:
            self.fail("Ошибка валидации не найдена в ожидаемых местах")

        # Проверяем корректное время (2 минуты)
        valid_time_data = {
            **base_habit_data,
            'execution_time': 2
        }
        response = self.client.post(
            reverse('habit:user-habit-list'),
            valid_time_data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['execution_time'], 2)
        self.assertIn('id', response.data)
        self.assertIn('user', response.data)

    # Тест на валидацию награды
    def test_reward_validation(self):
        # Проверяем награду для приятной привычки
        pleasant_with_reward_data = {
            **self.base_habit_data,
            'is_pleasant': True,
            'reward': 'Награда'  # награда не должна быть указана
        }
        response = self.client.post(
            reverse('habit:user-habit-list'),
            pleasant_with_reward_data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('non_field_errors', response.data)

        # Проверяем награду без связанной привычки
        valid_reward_data = {
            **self.base_habit_data,
            'is_pleasant': False,
            'reward': 'Награда',
            'linked_habit': None
        }
        response = self.client.post(
            reverse('habit:user-habit-list'),
            valid_reward_data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['reward'], 'Награда')
