from django.db import models

from services.models import Service
from subscriptions.models import User


class PromoCode(models.Model):
    """Модель промокода сервиса."""
    class Type(models.TextChoices):
        SUBSCRIPTION = "SUBSCRIPTION", "subscription"
        DISCOUNT = "DISCOUNT", "discount"

    name = models.CharField(
        max_length=200,
        verbose_name='Название'
    )
    key = models.CharField(
        max_length=200,
        verbose_name='Ключ активации'
    )
    type = models.CharField(
        max_length=12,
        choices=Type.choices,
        default=Type.SUBSCRIPTION,
        verbose_name='Тип операции'
    )
    service = models.ForeignKey(
        Service,
        related_name='promo_code',
        on_delete=models.CASCADE,
        verbose_name='Сервис'
    )
    user = models.ForeignKey(
        User,
        related_name='promo_code',
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )

    class Meta:
        verbose_name = 'Промокод'
        verbose_name_plural = 'Промокоды'
        constraints = [models.UniqueConstraint(
            fields=['key', 'user'],
            name='unique_key'
        )]

    def __str__(self):
        return f'{self.name} | {self.service} / {self.user}'
