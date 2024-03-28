from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from .constants import MAX_LIMIT_VALUE, MIN_LIMIT_VALUE

User = get_user_model()


class Category(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.title


class Evaluation(models.Model):
    """Модель оценки."""
    service = models.ForeignKey(
        'Service',
        on_delete=models.CASCADE,
        related_name='evaluations',
        verbose_name='Сервис',
        help_text='Нужно выбрать сервис.'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='evaluations',
        verbose_name='Пользователь',
        help_text='Пользователь который оценивает сервис.'
    )
    score = models.PositiveSmallIntegerField(
        validators=[
            MaxValueValidator(
                limit_value=MAX_LIMIT_VALUE,
                message=f'Оценка больше {MAX_LIMIT_VALUE}.'
            ),
            MinValueValidator(
                limit_value=MIN_LIMIT_VALUE,
                message=f'Оценка меньше {MIN_LIMIT_VALUE}.'
            )
        ],
        verbose_name='Оценка',
        help_text=(f'Оцените сервис, в диапазоне от {MIN_LIMIT_VALUE}'
                   f'до {MAX_LIMIT_VALUE}')
    )

    class Meta:
        ordering = ('-pk',)
        verbose_name = 'Оценка'
        verbose_name_plural = 'Оценки'
        constraints = [models.UniqueConstraint(
            fields=['service', 'user'],
            name='unique_evaluation'
        )]

    def __str__(self):
        return f"{self.service} - {self.user} / {self.score}"


class Service(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()

    def __str__(self):
        return self.title


class Payment(models.Model):
    amount = models.DecimalField(
        max_digits=14, decimal_places=2
    )
    date = models.DateTimeField(
        'Дата оплаты', auto_now_add=True, db_index=True
    )


class Subscription(models.Model):
    service = models.ForeignKey(
        Service, on_delete=models.SET_NULL,
        related_name="subscription", blank=True, null=True
    )
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL,
        related_name="subscription", blank=True, null=True
    )
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(
        max_digits=14, decimal_places=2
    )
    period = ...

    def __str__(self):
        return self.title


class Follow(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="follower"  # !
    )
    subscription = models.ForeignKey(
        Subscription, on_delete=models.CASCADE, related_name="subscription"  # !
    )
    payment = models.ForeignKey(
        Payment, on_delete=models.CASCADE, related_name="follower"  # !
    )
    date_subscription = models.DateTimeField(
        'Дата начала', auto_now_add=True, db_index=True
    )
    date_payment = models.DateTimeField(
        'Дата списания', auto_now_add=True, db_index=True
    )
    status = ...

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "subscription"], name="unique_follow"
            )
        ]


class Cashback(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="follower"  # !
    )
    payment = models.ForeignKey(
        Payment, on_delete=models.CASCADE, related_name="follower"  # !
    )
    amount = models.DecimalField(
        max_digits=14, decimal_places=2
    )
    status = ...
    balance = models.DecimalField(
        max_digits=14, decimal_places=2
    )
    interest_rate = ...
