from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser
from rest_framework.viewsets import ModelViewSet
from drf_spectacular.utils import extend_schema_view, extend_schema

from .mixins import OwnerPermMixin, MultiSerializerViewSetMixin
from .serializers import (
    UserProfileSerializer,
    UserStaffStatusSerializer,
    UserActiveStatusSerializer
)

User = get_user_model()


@extend_schema_view(
    create=extend_schema(description='Создание профиля пользователя'),
    retrieve=extend_schema(description='Получение профиля пользователя'),
    update=extend_schema(description='Полное обновление профиля пользователя'),
    partial_update=extend_schema(
        description='Частичное обновление профиля пользователя'),
    destroy=extend_schema(description='Удаление профиля пользователя'),
    list=extend_schema(description='Получение списка профилей пользователей'),
)
class UserProfileViewSet(MultiSerializerViewSetMixin, OwnerPermMixin, ModelViewSet):
    """
    CRUD для пользователя
    """
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    serializer_action_classes = {
        'set_staff_status': UserStaffStatusSerializer,
        'set_active_status': UserActiveStatusSerializer,
    }
    owner_field = 'pk'

    @extend_schema(
        description='Изменение статуса пользователя до админа и обратно')
    @action(detail=True, methods=['PATCH'], name='set staff status',
            permission_classes=[IsAdminUser])
    def set_staff_status(self, request, pk=None):
        return self._custom_update_action(request, UserStaffStatusSerializer, pk)

    @extend_schema(
        description='Блокировка / разблокировка пользователя')
    @action(detail=True, methods=['PATCH'], name='set active status',
            permission_classes=[IsAdminUser])
    def set_active_status(self, request, pk=None):
        return self._custom_update_action(request, UserActiveStatusSerializer, pk)

    def _custom_update_action(self, request, serializer, pk=None):
        user = self.get_object()
        serializer = serializer(data=request.data)
        if serializer.is_valid():
            serializer.update(user, serializer.validated_data)
            return Response(serializer.data)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

