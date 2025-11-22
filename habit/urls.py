from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserHabitViewSet, PublicHabitViewSet
from habit.apps import HabitConfig

router = DefaultRouter()
# urls.py
router.register(r'user-habits', UserHabitViewSet, basename='user-habit')
router.register(r'public-habits', PublicHabitViewSet, basename='public-habit')


urlpatterns = [
    path('', include(router.urls)),
]
app_name = HabitConfig.name
