from rest_framework import serializers

from services.models import Category


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для модели Категории."""
    class Meta:
        model = Category
        fields = ('name', 'slug')
