from rest_framework.routers import DefaultRouter

from habits.apps import HabitsConfig
from habits.views import RewardViewSet

app_name = HabitsConfig.name

router = DefaultRouter()
router.register(r'rewards', RewardViewSet, basename='rewards')

urlpatterns = [

] + router.urls
