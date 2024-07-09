from datetime import timedelta

from celery import shared_task

from habits.models import Habit
from habits.services import send_telegram_message
from django.utils import timezone


@shared_task
def remind_about_habit():
    print('working task')
    periodicity = ["Раз в день", "Раз в два дня", "Раз в три дня", "Раз в четыре дня", "Раз в пять дней",
                   "Раз в шесть дней", "Раз в неделю"]
    now = timezone.now()
    habits = Habit.objects.filter(is_pleasant=False)

    for habit in habits:
        chat_id = habit.owner.telegram_chat_id
        message = f"Я буду {habit.activity} в {habit.time} в {habit.place}"

        if habit.last_datetime < now:
            if chat_id:
                send_telegram_message(chat_id, message)
            if habit.periodicity == periodicity[0]:
                habit.last_datetime = now + timedelta(days=1)
            elif habit.periodicity == periodicity[1]:
                habit.last_datetime = now + timedelta(days=2)
            elif habit.periodicity == periodicity[2]:
                habit.last_datetime = now + timedelta(days=3)
            elif habit.periodicity == periodicity[3]:
                habit.last_datetime = now + timedelta(days=4)
            elif habit.periodicity == periodicity[4]:
                habit.last_datetime = now + timedelta(days=5)
            elif habit.periodicity == periodicity[5]:
                habit.last_datetime = now + timedelta(days=6)
            elif habit.periodicity == periodicity[6]:
                habit.last_datetime = now + timedelta(days=7)
            habit.save()
