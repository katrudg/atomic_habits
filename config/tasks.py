from datetime import time

import requests
from celery import shared_task

from config.settings import TELEGRAM_BOT_TOKEN
from habits.models import Habit
from user.models import User

@shared_task
def telegram_notifications(id):
    habit = Habit.objects.get(pk=id)
    user_telegram = User.objects.get(pk=habit.user.pk).telegram

    hours, minutes, seconds = map(int, habit['time_to_complete'].split(':'))

    total_seconds = hours * 3600 + minutes * 60 + seconds

    requests.post(
        url=f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage',
        data={
            'chat_id': user_telegram,
            'test': habit
        }
    )

    time.sleep(total_seconds)

    if habit['reward']:
        requests.post(
            url=f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage',
            data={
                'chat_id': user_telegram,
                'test': habit['reward']
            }
        )
    else:
        related_habit = Habit.objects.get(pk=habit['related_habit'])
        requests.post(
            url=f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage',
            data={
                'chat_id': user_telegram,
                'test': Habit.objects.get(pk=related_habit).action
            }
        )
