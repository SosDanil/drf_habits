from django.shortcuts import render
from rest_framework import viewsets

from habits.models import Reward
from habits.serializers import RewardSerializer


class RewardViewSet(viewsets.ModelViewSet):
    """Viewset for cars"""
    serializer_class = RewardSerializer
    queryset = Reward.objects.all()
