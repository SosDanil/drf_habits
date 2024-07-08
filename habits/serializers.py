from rest_framework import serializers

from habits.models import Reward, Habit
from habits.validators import OnlyRewardOrPleasantHabitValidator, DurationValidator, OnlyPleasantHabitValidator, \
    PleasantDoesNotHaveRewardOrHabitValidator


class RewardSerializer(serializers.ModelSerializer):

    class Meta:
        model = Reward
        fields = '__all__'


class HabitSerializer(serializers.ModelSerializer):

    class Meta:
        model = Habit
        fields = '__all__'


class CreateUpdateHabitSerializer(serializers.ModelSerializer):

    class Meta:
        model = Habit
        fields = '__all__'
        validators = [
            OnlyRewardOrPleasantHabitValidator(field1='reward', field2='related_habit'),
            DurationValidator(field='duration'),
            OnlyPleasantHabitValidator(field='related_habit'),
            PleasantDoesNotHaveRewardOrHabitValidator(field1='is_pleasant', field2='related_habit', field3='reward')
        ]
