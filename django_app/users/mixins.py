class OwnerPermMixin():
    """
    Mixin для ViewSet с дополнительным разграничением доступа:
    Админы - без фильтрации
    Обычные пользователи - только свое
    Остальные - ничего

    owner_field - строка. Название поля по которому определяем владельца.
    """
    owner_field = 'user'

    def get_queryset(self):
        """
        Обычные пользователи могут работать только со своим профилем
        """
        qs = super().get_queryset()
        if not self.request.user:
            qs = qs.none()
        elif not self.request.user.is_staff:
            qs = qs.filter(pk=self.request.user.pk)
        return qs


class MultiSerializerViewSetMixin(object):
    """
    https://stackoverflow.com/a/22922156
    """

    def get_serializer_class(self):
        """
        Look for serializer class in self.serializer_action_classes, which
        should be a dict mapping action name (key) to serializer class (value),
        i.e.:

        class MyViewSet(MultiSerializerViewSetMixin, ViewSet):
            serializer_class = MyDefaultSerializer
            serializer_action_classes = {
               'list': MyListSerializer,
               'my_action': MyActionSerializer,
            }

            @action
            def my_action:
                ...

        If there's no entry for that action then just fallback to the regular
        get_serializer_class lookup: self.serializer_class, DefaultSerializer.

        """
        try:
            return self.serializer_action_classes[self.action]
        except (KeyError, AttributeError):
            return super(MultiSerializerViewSetMixin, self).get_serializer_class()
