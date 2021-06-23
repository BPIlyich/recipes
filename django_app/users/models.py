from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    """
    Модель пользователя для возможных в будущем изменений
    """

    def __str__(self):
        return self.username
