from rest_framework import serializers

from habits.models import Reward


class RewardSerializer(serializers.ModelSerializer):

    class Meta:
        model = Reward
        fields = '__all__'
