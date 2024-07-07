from rest_framework import serializers

from habits.models import Reward, Habit
from habits.validators import OnlyRewardOrPleasantHabit


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
        validators = [OnlyRewardOrPleasantHabit(field1='reward', field2='related_habit')]
