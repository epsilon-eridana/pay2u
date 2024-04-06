from rest_framework import serializers

from services.models import Category, Service


class ServiceSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Сервиса."""
    class Meta:
        model = Service
        fields = (
            'name',
            'short_description',
            'description',
            'icon',
            'url'
        )


class CategoryListSerializer(serializers.ModelSerializer):
    """Сериализатор для списка категорий."""
    class Meta:
        model = Category
        fields = (
            'name',
            'slug'
        )


class CategoryDetailSerializer(serializers.ModelSerializer):
    """Сериализатор для детальной информации о категории."""
    services = ServiceSerializer(
        many=True,
        read_only=True
    )

    class Meta:
        model = Category
        fields = (
            'name',
            'slug',
            'services'
        )
