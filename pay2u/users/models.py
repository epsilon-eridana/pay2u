from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator

REGEX_SIGNS = RegexValidator(r'^[\w.@+-]+\Z', 'Поддерживаемые символы.')
REGEX_ME = RegexValidator(r'[^m][^e]', 'Имя пользователя не может быть "me".')
REGEX_PHONE = RegexValidator(r'^\+\d{11}$', 'Поддерживаемый формат.')


class User(AbstractUser):
    """Модель пользователей."""
    username = models.CharField(
        unique=True,
        max_length=150,
        validators=(REGEX_SIGNS, REGEX_ME),
        verbose_name='Никнейм пользователя',
        help_text='Укажите никнейм пользователя'
    )
    phone = models.CharField(
        unique=True,
        max_length=12,
        validators=(REGEX_PHONE,),
        verbose_name='Номер телефона пользователя',
        help_text='Укажите номер телефона пользователя'
    )
    first_name = models.CharField(
        max_length=150,
        verbose_name='Имя пользователя',
        help_text='Укажите имя пользователя'
    )
    last_name = models.CharField(
        max_length=150,
        verbose_name='Фамилия пользователя',
        help_text='Укажите фамилия пользователя'
    )
    REQUIRED_FIELDS = ['first_name', 'last_name', 'username']
    USERNAME_FIELD = 'phone'

    class Meta:
        ordering = ('id',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username
