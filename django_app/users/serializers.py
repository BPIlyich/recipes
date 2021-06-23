from rest_framework.serializers import ModelSerializer, BooleanField
from django.contrib.auth import get_user_model

User = get_user_model()


class UserProfileSerializer(ModelSerializer):
    """
    Сериализатор для пользователя
    """

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
        )
        return user

    class Meta:
        model = User
        fields = ('id', 'username', 'password')
        read_only_fields = ('id',)
        extra_kwargs = {
            'password': {'write_only': True}
        }


class UserStaffStatusSerializer(ModelSerializer):
    """
    Сериализатор для повышения пользователя до админа и обратно
    """

    class Meta:
        model = User
        fields = ('id', 'username', 'is_staff')
        read_only_fields = ('id', 'username')
        extra_kwargs = {'is_staff': {'required': True}}


class UserActiveStatusSerializer(ModelSerializer):
    """
    Сериализатор для блокировки / разблокировки пользователя
    """

    class Meta:
        model = User
        fields = ('id', 'username', 'is_active')
        read_only_fields = ('id', 'username')
        extra_kwargs = {'is_active': {'required': True}}
