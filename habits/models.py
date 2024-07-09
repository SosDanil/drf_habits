from django.conf import settings
from django.db import models


class Reward(models.Model):
    title = models.CharField(max_length=200, verbose_name='название')
    description = models.TextField(null=True, blank=True, verbose_name='описание')

    class Meta:
        verbose_name = 'вознаграждение'
        verbose_name_plural = 'вознаграждения'

    def __str__(self):
        return self.title


class Habit(models.Model):
    DAILY = "Раз в день"
    EVERY_TWO_DAYS = "Раз в два дня"
    EVERY_THREE_DAYS = "Раз в три дня"
    EVERY_FOUR_DAYS = "Раз в четыре дня"
    EVERY_FIVE_DAYS = "Раз в пять дней"
    EVERY_SIX_DAYS = "Раз в шесть дней"
    WEEKLY = "Раз в неделю"

    PERIODICITY_CHOICES = (
        (DAILY, "Раз в день"),
        (EVERY_TWO_DAYS, "Раз в два дня"),
        (EVERY_THREE_DAYS, "Раз в три дня"),
        (EVERY_FOUR_DAYS, "Раз в четыре дня"),
        (EVERY_FIVE_DAYS, "Раз в пять дней"),
        (EVERY_SIX_DAYS, "Раз в шесть дней"),
        (WEEKLY, "Раз в неделю"),
    )

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='владелец',
                              related_name='habit')
    related_habit = models.ForeignKey('self', on_delete=models.SET_NULL, verbose_name='связанная привычка',
                                      related_name='habit', null=True, blank=True)
    reward = models.ForeignKey(Reward, on_delete=models.SET_NULL, verbose_name='вознаграждение', related_name='habit',
                               null=True, blank=True)

    is_pleasant = models.BooleanField(verbose_name='приятная привычка?', default=False)
    is_public = models.BooleanField(verbose_name='публичная привычка?', default=False)

    activity = models.CharField(max_length=300, verbose_name='описание привычки')
    time = models.TimeField(verbose_name='время, в которое выполняется', null=True, blank=True)
    place = models.CharField(max_length=150, verbose_name='место', null=True, blank=True)
    duration = models.DurationField(verbose_name='продолжительность действия в сек.', default=None, null=True,
                                    blank=True)
    periodicity = models.CharField(max_length=50, choices=PERIODICITY_CHOICES, verbose_name='периодичность',
                                   default=DAILY)
    last_datetime = models.DateTimeField(auto_now_add=True, verbose_name='время последнего выполнения привычки',
                                         null=True, blank=True)

    class Meta:
        verbose_name = 'привычка',
        verbose_name_plural = 'привычки'

    def __str__(self):
        return f'{self.activity}, ({self.is_pleasant}, {self.is_public}), владелец: {self.owner}'
