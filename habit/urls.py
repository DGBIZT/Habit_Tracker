from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import HabitViewSet
from habit.apps import HabitConfig

router = DefaultRouter()
router.register(r'habits', HabitViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
app_name = HabitConfig.name
