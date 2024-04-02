from django.contrib.auth import get_user_model
from django.db import models

from .services.models import Rate

User = get_user_model()


class Subscription(models.Model):
    """Модель подписки пользователя."""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscriptions'
    )
    rate = models.ForeignKey(
        Rate,
        on_delete=models.CASCADE,
        related_name='subscriptions'
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

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'

    def __str__(self):
        return f'{self.user} / {self.rate.name}'
