from django.urls import include, path
from rest_framework.routers import DefaultRouter

from habit.apps import HabitConfig

from .views import PublicHabitViewSet, UserHabitViewSet

router = DefaultRouter()
# urls.py
router.register(r"user-habits", UserHabitViewSet, basename="user-habit")
router.register(r"public-habits", PublicHabitViewSet, basename="public-habit")


urlpatterns = [
    path("", include(router.urls)),
]
app_name = HabitConfig.name
