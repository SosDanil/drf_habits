from django.urls import path
from rest_framework.routers import DefaultRouter

from habits.apps import HabitsConfig
from habits.views import RewardViewSet, HabitListAPIView, HabitCreateAPIView, HabitRetrieveAPIView, HabitUpdateAPIView, \
    HabitDestroyAPIView, HabitPublicListAPIView, HabitOwnerListAPIView

app_name = HabitsConfig.name

router = DefaultRouter()
router.register(r'rewards', RewardViewSet, basename='rewards')

urlpatterns = [
    path('public_list/', HabitPublicListAPIView.as_view(), name='habit_public_list'),
    path('owner_list/', HabitOwnerListAPIView.as_view(), name='habit_owner_list'),
    path('create/', HabitCreateAPIView.as_view(), name='habit_create'),
    path('retrieve/<int:pk>/', HabitRetrieveAPIView.as_view(), name='habit_retrieve'),
    path('update/<int:pk>/', HabitUpdateAPIView.as_view(), name='habit_update'),
    path('delete/<int:pk>/', HabitDestroyAPIView.as_view(), name='habit_delete'),
] + router.urls
