from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from services.models import Rate
from users.models import User

MAX_LIMIT_VALUE_PRICE = 999999
MIN_LIMIT_VALUE_PRICE = 0
DEFAULT_CASHBACK = 0


class Subscription(models.Model):
    """Модель подписки пользователя."""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscriptions',
        verbose_name='Пользователь'
    )
    rate = models.ForeignKey(
        Rate,
        on_delete=models.CASCADE,
        related_name='subscriptions',
        verbose_name='Тариф'
    )
    date_start = models.DateTimeField(
        verbose_name='Дата начала',
        auto_now_add=True,
        db_index=True
    )
    date_end = models.DateTimeField(
        verbose_name='Дата окончания',
        db_index=True
    )
    extension = models.BooleanField(
        default=True,
        verbose_name='Статус продления'
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'

    def __str__(self):
        return f'{self.user} / {self.rate.name}'


class Payment(models.Model):
    """Модель покупок."""
    rate = models.OneToOneField(
        Rate,
        on_delete=models.CASCADE,
        related_name='payment',
        verbose_name='Тариф'
    )
    price = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        verbose_name='Цена',
        validators=[
            MaxValueValidator(
                limit_value=MAX_LIMIT_VALUE_PRICE,
                message=f'Значение должно быть меньше '
                        f'{MAX_LIMIT_VALUE_PRICE}.'
            ),
            MinValueValidator(
                limit_value=MIN_LIMIT_VALUE_PRICE,
                message=f'Значение должно быть больше '
                        f'{MIN_LIMIT_VALUE_PRICE}.'
            )
        ]
    )
    cashback = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        verbose_name='Кэшбэк',
        validators=[
            MaxValueValidator(
                limit_value=MAX_LIMIT_VALUE_PRICE,
                message=f'Значение должно быть меньше '
                        f'{MAX_LIMIT_VALUE_PRICE}.'
            ),
            MinValueValidator(
                limit_value=MIN_LIMIT_VALUE_PRICE,
                message=f'Значение должно быть больше '
                        f'{MIN_LIMIT_VALUE_PRICE}.'
            )
        ],
        default=DEFAULT_CASHBACK
    )
    date = models.DateTimeField(
        verbose_name='Дата',
        auto_now_add=True,
        db_index=True
    )


    class Meta:
        verbose_name = 'Покупка'
        verbose_name_plural = 'Покупки'

    def __str__(self):
        return f'{self.subscription} / {self.price}'
