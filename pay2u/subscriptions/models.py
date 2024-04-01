from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Category(models.Model):
    """Модель категории."""
    name = models.CharField(
        max_length=200,
        unique=True,
        verbose_name='Название'
    )
    slug = models.SlugField(
        unique=True,
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
        max_length=200,
        unique=True,
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


class Options(models.Model):
    """Модель опций сервиса подписок."""
    icon = models.ImageField(
        upload_to='options/icons/'
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
        on_delete=models,
        related_name='services',
        verbose_name='Категория'
    )
    icon = models.ImageField(
        upload_to='services/images/',
        verbose_name='Иконка'
    )
    tags = models.ManyToManyField(
        Tag,
        related_name='services',
        verbose_name='Теги'
    )
    options = models.ManyToManyField(
        Options,
        through='ServiceOptions',
        related_name='services',
        verbose_name='Опции'
    )

    class Meta:
        verbose_name = 'Сервис'
        verbose_name_plural = 'Сервисы'

    def __str__(self):
        return self.name


class ServiceOptions(models.Model):
    """Вспомогательная модель: Сервис - Опция."""
    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        related_name='Сервис подписки'
    )
    option = models.ForeignKey(
        Options,
        unique=True,
        on_delete=models.CASCADE,
        related_name='Опция сервиса'
    )

    class Meta:
        verbose_name = 'Сервис-опции'
        verbose_name_plural = verbose_name
        constraints = [models.UniqueConstraint(
            fields=['service', 'option'],
            name='unique_options'
        )]
