from celery import shared_task
import requests
from habit.models import Habit, Notification
from telegram import Bot
from django.conf import settings


@shared_task
def send_notifications():
    # Получаем все привычки, требующие уведомления
    habits = Habit.objects.filter(is_active=True)

    for habit in habits:
        if habit.is_time_to_notify():  # Ваша логика проверки времени
            try:
                # Отправляем уведомление через Telegram
                bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
                message = f"Напоминание: пора выполнить привычку '{habit.name}'"
                bot.send_message(chat_id=habit.user.telegram_id, text=message)

                # Сохраняем факт отправки уведомления
                Notification.objects.create(
                    habit=habit,
                    status='sent'
                )
            except Exception as e:
                Notification.objects.create(
                    habit=habit,
                    status='error',
                    error_message=str(e)
                )


@shared_task
def send_simple_request(url, data):
    try:
        response = requests.post(url, json=data)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        return {'error': str(e)}
