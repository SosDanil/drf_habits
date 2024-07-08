from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView

from habits.models import Reward, Habit
from habits.paginations import HabitPaginator
from habits.serializers import RewardSerializer, HabitSerializer, CreateUpdateHabitSerializer


class RewardViewSet(viewsets.ModelViewSet):
    """Viewset for cars"""
    serializer_class = RewardSerializer
    queryset = Reward.objects.all()


class HabitCreateAPIView(CreateAPIView):
    serializer_class = CreateUpdateHabitSerializer
    queryset = Habit.objects.all()


class HabitPublicListAPIView(ListAPIView):
    serializer_class = HabitSerializer
    queryset = Habit.objects.filter(is_public=True)


class HabitOwnerListAPIView(ListAPIView):
    serializer_class = HabitSerializer
    pagination_class = HabitPaginator

    def get_queryset(self):
        queryset = Habit.objects.filter(owner=self.request.user)
        return queryset


class HabitRetrieveAPIView(RetrieveAPIView):
    serializer_class = HabitSerializer
    queryset = Habit.objects.all()


class HabitUpdateAPIView(UpdateAPIView):
    serializer_class = CreateUpdateHabitSerializer
    queryset = Habit.objects.all()


class HabitDestroyAPIView(DestroyAPIView):
    queryset = Habit.objects.all()
