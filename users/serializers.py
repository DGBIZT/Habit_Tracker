from rest_framework import serializers
from users.models import CustomUser

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = "__all__"

    def create(self, validated_data):
        # Хешируем пароль перед сохранением
        password = validated_data.pop('password')
        user = CustomUser(**validated_data)
        user.set_password(password)  # Используем встроенный метод
        user.save()
        return user