from rest_framework.serializers import ValidationError
from datetime import timedelta


class OnlyRewardOrPleasantHabitValidator:
    """ Исключает одновременный выбор связанной привычки и указания вознаграждения."""

    def __init__(self, field1, field2):
        self.field1 = field1
        self.field2 = field2

    def __call__(self, value):
        tmp_val = dict(value).get(self.field1)
        tmp_val2 = dict(value).get(self.field2)
        if tmp_val and tmp_val2:
            raise ValidationError('У привычки может быть только вознаграждение или только связанная привычка,'
                                  ' не оба пункта вместе')


class DurationValidator:
    """Проверяет, что время выполнения должно быть не больше 120 секунд и не меньше 1 секунды"""

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        tmp_val = dict(value).get(self.field)
        if tmp_val is not None:
            if tmp_val > timedelta(seconds=120):
                raise ValidationError('Продолжительность привычки не может быть больше 120 секунд')
            if tmp_val < timedelta(seconds=1):
                raise ValidationError('Продолжительность не может быть нулевой или отрицательной')


class OnlyPleasantHabitValidator:
    """Проверяет, что в связанные привычки могут попадать только привычки с признаком приятной привычки"""

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        tmp_val = dict(value).get(self.field)
        if tmp_val is not None:
            if tmp_val.is_pleasant == False:
                raise ValidationError('В связанные привычки можно указывать только приятные привычки')


class PleasantDoesNotHaveRewardOrHabitValidator:
    """Проверяет, что у приятной привычки не может быть вознаграждения или связанной привычки"""

    def __init__(self, field1, field2, field3):
        self.field1 = field1
        self.field2 = field2
        self.field3 = field3

    def __call__(self, value):
        tmp_val1 = value.get(self.field1)
        tmp_val2 = value.get(self.field2)
        tmp_val3 = value.get(self.field3)
        if tmp_val1 and tmp_val2 or tmp_val1 and tmp_val3:
            raise ValidationError('У приятной привычки не может быть вознаграждения или связанной привычки')
