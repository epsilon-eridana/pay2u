from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

MAX_LIMIT_VALUE = 10000
MIN_LIMIT_VALUE = 1
MAX_LIMIT_VALUE_CASHBACK = 100
MIN_LIMIT_VALUE_CASHBACK = 0
DEFAULT_CASHBACK = 0
MAX_LIMIT_VALUE_PRICE = 999999
MIN_LIMIT_VALUE_PRICE = 0
DEFAULT_PRICE = 0
DEFAULT_DURATION = 1


class Category(models.Model):
    """Модель категории."""
    name = models.CharField(
        max_length=200,
        unique=True,
        verbose_name='Название'
    )
    slug = models.SlugField(
        primary_key=True,
        max_length=200,
        verbose_name='Slug'
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Tag(models.Model):
    """Модель тега."""
    name = models.CharField(
        max_length=200,
        unique=True,
        verbose_name='Название',
    )
    slug = models.SlugField(
        primary_key=True,
        max_length=200,
        verbose_name='Slug',
    )
    color = models.CharField(
        max_length=7,
        verbose_name='Цвет',
    )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Option(models.Model):
    """Модель опций сервиса подписок."""
    icon = models.ImageField(
        upload_to='services/options/icons/'
    )
    name = models.CharField(
        max_length=200,
        verbose_name='Название'
    )

    class Meta:
        verbose_name = 'Опция'
        verbose_name_plural = 'Опции'

    def __str__(self):
        return self.name


class Image(models.Model):
    """Модель изображений сервиса."""
    image = models.ImageField(
        upload_to='services/images/',
        verbose_name='Изображение'
    )

    class Meta:
        verbose_name = 'Изображение'
        verbose_name_plural = 'Изображения'

    def __str__(self):
        return str(self.pk)


class Rate(models.Model):
    """Модель тарифа подписки."""
    name = models.CharField(
        max_length=200,
        verbose_name='Название',
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
        ],
        default=DEFAULT_PRICE
    )
    price_month = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        verbose_name='Месячная плата',
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
        default=DEFAULT_PRICE
    )
    duration = models.IntegerField(
        validators=[
            MaxValueValidator(
                limit_value=MAX_LIMIT_VALUE,
                message=f'Количество дне должно быть меньше '
                        f'{MAX_LIMIT_VALUE}.'
            ),
            MinValueValidator(
                limit_value=MIN_LIMIT_VALUE,
                message=f'Количество дне должно быть больше '
                        f'{MIN_LIMIT_VALUE}.'
            )
        ],
        verbose_name='Количество дней',
        default=DEFAULT_DURATION
    )
    cashback = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        verbose_name='Процент кэшбэка',
        validators=[
            MaxValueValidator(
                limit_value=MAX_LIMIT_VALUE_CASHBACK,
                message=f'Значение должно быть меньше '
                        f'{MAX_LIMIT_VALUE_CASHBACK}.'
            ),
            MinValueValidator(
                limit_value=MIN_LIMIT_VALUE_CASHBACK,
                message=f'Значение должно быть больше '
                        f'{MIN_LIMIT_VALUE_CASHBACK}.'
            )
        ],
        default=DEFAULT_CASHBACK
    )

    class Meta:
        verbose_name = 'Тариф'
        verbose_name_plural = 'Тарифы'

    def __str__(self):
        return self.name


class Service(models.Model):
    """Модель сервиса подписки."""
    name = models.CharField(
        max_length=200,
        verbose_name='Название'
    )
    short_description = models.CharField(
        max_length=200,
        verbose_name='Краткое описание'
    )
    description = models.TextField(
        max_length=1000,
        verbose_name='Описание'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='services',
        verbose_name='Категория'
    )
    icon = models.ImageField(
        upload_to='services/icons/',
        verbose_name='Иконка'
    )
    tags = models.ManyToManyField(
        Tag,
        related_name='services',
        verbose_name='Теги'
    )
    options = models.ManyToManyField(
        Option,
        through='ServiceOptions',
        related_name='service',
        verbose_name='Опции'
    )
    rates = models.ManyToManyField(
        Rate,
        through='ServiceRate',
        related_name='service',
        verbose_name='Тарифы'
    )
    images = models.ManyToManyField(
        Image,
        through='ServiceImage',
        related_name='service',
        verbose_name='Изображение'
    )
    url = models.URLField(
        verbose_name='Ссылка на сервис'
    )

    class Meta:
        verbose_name = 'Сервис'
        verbose_name_plural = 'Сервисы'

    def __str__(self):
        return self.name


class ServiceImage(models.Model):
    """Вспомогательная модель: Сервис - Изображение."""
    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        related_name='service_image',
        verbose_name='Сервис'
    )
    image = models.OneToOneField(
        Image,
        on_delete=models.CASCADE,
        related_name='service_image',
        verbose_name='Изображение'
    )

    class Meta:
        verbose_name = 'Сервис-изображение'
        verbose_name_plural = verbose_name
        constraints = [models.UniqueConstraint(
            fields=['service', 'image'],
            name='unique_image'
        )]


class ServiceRate(models.Model):
    """Вспомогательная модель: Сервис - Тариф."""
    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        related_name='service_rate',
        verbose_name='Сервис'
    )
    rate = models.OneToOneField(
        Rate,
        on_delete=models.CASCADE,
        related_name='service_rate',
        verbose_name='Тариф'
    )

    class Meta:
        verbose_name = 'Сервис-тариф'
        verbose_name_plural = verbose_name
        constraints = [models.UniqueConstraint(
            fields=['service', 'rate'],
            name='unique_rate'
        )]


class ServiceOptions(models.Model):
    """Вспомогательная модель: Сервис - Опция."""
    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        related_name='service_option',
        verbose_name='Сервис подписки'
    )
    option = models.OneToOneField(
        Option,
        on_delete=models.CASCADE,
        related_name='service_option',
        verbose_name='Опция сервиса'
    )

    class Meta:
        verbose_name = 'Сервис-опции'
        verbose_name_plural = verbose_name
        constraints = [models.UniqueConstraint(
            fields=['service', 'option'],
            name='unique_options'
        )]
