from django.contrib.auth.models import AbstractUser
from django.db import models

from users.constants import NAME, EMAIL
from users.validators import validate_username

USER = 'user'
ADMIN = 'admin'
MODERATOR = 'moderator'

CHOICES = (
    (USER, 'Аутентифицированный пользователь'),
    (ADMIN, 'Администратор'),
    (MODERATOR, 'Модератор')
)


class User(AbstractUser):

    username = models.CharField(
        'Имя пользователя',
        max_length=NAME,
        unique=True,
        validators=(validate_username,)
    )
    email = models.EmailField(
        'Адрес электронной почты',
        max_length=EMAIL,
        unique=True
    )
    bio = models.TextField(
        'Биография',
        blank=True,
    )
    first_name = models.CharField(
        'Имя',
        blank=True,
        max_length=NAME
    )
    last_name = models.CharField(
        'Фамилия',
        blank=True,
        max_length=NAME
    )
    role = models.CharField(
        'Роль',
        max_length=max(len(role) for role, _ in CHOICES),
        choices=CHOICES,
        default=USER,
    )

    class Meta:
        verbose_name = 'Пользователь'
        ordering = ('username',)

    def __str__(self):
        return self.username

    @property
    def is_admin(self):
        return self.role == ADMIN or self.is_superuser or self.is_staff

    @property
    def is_moderator(self):
        return self.role == MODERATOR
