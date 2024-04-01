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
        verbose_name='Слаг',
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

    class Meta:
        verbose_name = 'Сервис'
        verbose_name_plural = 'Сервисы'

    def __str__(self):
        return self.name
