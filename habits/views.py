from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView

from habits.models import Reward, Habit
from habits.serializers import RewardSerializer, HabitSerializer


class RewardViewSet(viewsets.ModelViewSet):
    """Viewset for cars"""
    serializer_class = RewardSerializer
    queryset = Reward.objects.all()


class HabitCreateAPIView(CreateAPIView):
    serializer_class = HabitSerializer
    queryset = Habit.objects.all()


class HabitListAPIView(ListAPIView):
    serializer_class = HabitSerializer
    queryset = Habit.objects.all()


class HabitRetrieveAPIView(RetrieveAPIView):
    serializer_class = HabitSerializer
    queryset = Habit.objects.all()


class HabitUpdateAPIView(UpdateAPIView):
    serializer_class = HabitSerializer
    queryset = Habit.objects.all()


class HabitDestroyAPIView(DestroyAPIView):
    queryset = Habit.objects.all()
