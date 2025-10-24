from habit.apps import HabitConfig
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import HabitViewSet


app_name = HabitConfig.name


router = DefaultRouter()
router.register(r'habits', HabitViewSet, basename="habits")

urlpatterns = [

] + router.urls
