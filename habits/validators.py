from rest_framework.serializers import ValidationError


class OnlyRewardOrPleasantHabit:

    def __init__(self, field1, field2):
        self.field1 = field1
        self.field2 = field2

    def __call__(self, value):
        tmp_val = dict(value).get(self.field1)
        tmp_val2 = dict(value).get(self.field2)
        if tmp_val and tmp_val2:
            raise ValidationError('У привычки может быть только вознаграждение или только связанная привычка,'
                                  ' не оба пункта вместе')
