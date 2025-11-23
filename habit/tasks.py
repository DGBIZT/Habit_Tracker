import logging

import requests
from celery import shared_task
from django.conf import settings
from telegram import Bot
from telegram.error import TelegramError

from habit.models import Habit, Notification

logger = logging.getLogger(__name__)


@shared_task
def send_notifications():
    """
    Задача для отправки уведомлений о привычках
    """
    try:
        # Получаем активные привычки
        habits = Habit.objects.filter(is_active=True)

        for habit in habits:
            if habit.is_time_to_notify():  # Проверяем, нужно ли отправлять уведомление
                try:
                    # Проверяем наличие Telegram ID
                    if not habit.user.telegram_id:
                        logger.warning(f"Нет Telegram ID для пользователя {habit.user.id}")
                        continue

                    # Отправляем уведомление
                    bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
                    message = (
                        f"Напоминание: пора выполнить привычку '{habit.action}'\n"
                        f"Место: {habit.place}\n"
                        f"Время: {habit.time}"
                    )
                    bot.send_message(chat_id=habit.user.telegram_id, text=message)

                    # Сохраняем успешную отправку
                    Notification.objects.create(habit=habit, status="sent")

                except TelegramError as te:
                    logger.error(f"Ошибка Telegram: {te}")
                    Notification.objects.create(habit=habit, status="error", error_message=str(te))

                except Exception as e:
                    logger.error(f"Неизвестная ошибка: {e}")
                    Notification.objects.create(habit=habit, status="error", error_message=str(e))

    except Exception as e:
        logger.critical(f"Критическая ошибка в задаче send_notifications: {e}")


@shared_task
def send_simple_request(url, data):
    """
    Отправка POST-запроса с данными
    """
    try:
        response = requests.post(url, json=data, timeout=10)  # Добавляем таймаут
        response.raise_for_status()
        return response.json()

    except requests.RequestException as e:
        logger.error(f"Ошибка при отправке запроса: {e}")
        return {"error": str(e)}
