from django.shortcuts import render
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from users.serializers import UserSerializer
from users.models import CustomUser
from rest_framework import generics,status
from django.http import Http404
from rest_framework.exceptions import PermissionDenied

class UserCreateAPIView(generics.CreateAPIView):
    """Регистрация нового пользователя"""
    serializer_class = UserSerializer
    queryset = CustomUser.objects.all()
    permission_classes = (AllowAny,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class UserRetrieveAPIView(generics.RetrieveAPIView):
    """Получение информации о пользователе из БД"""
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)
    queryset = CustomUser.objects.all()


    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

class UserUpdateAPIView(generics.UpdateAPIView):
    """Обновление данных пользователя"""
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    def get_object(self):
        # Проверяем, является ли пользователь суперпользователем
        if self.request.user.is_superuser:
            try:
                return CustomUser.objects.get(pk=self.kwargs['pk'])
            except CustomUser.DoesNotExist:
                raise Http404("Пользователь не найден")
        # Для обычных пользователей возвращаем только их профиль
        return self.request.user

class UserDestroyAPIView(generics.DestroyAPIView):
    """ Удаление учетной записи пользователя из системы """
    queryset = CustomUser.objects.all()
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        # Пользователь может удалять только свою учетную запись
        if self.request.user.is_superuser:
            return CustomUser.objects.get(pk=self.kwargs['pk'])
        return self.request.user

    class UserDestroyAPIView(generics.DestroyAPIView):
        queryset = CustomUser.objects.all()
        permission_classes = (IsAuthenticated,)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance != request.user and not request.user.is_superuser:
            raise PermissionDenied("У вас нет прав на удаление этого пользователя")
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
