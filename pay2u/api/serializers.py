from rest_framework import serializers

from services.models import (
    Category, Service, Tag, Rate, Image, Option
)


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Таг."""
    class Meta:
        model = Tag
        fields = ('name', 'color', 'slug')


class ServiceCategorySerializer(serializers.ModelSerializer):
    """Сериализатор для модели Сервиса."""
    tags = TagSerializer(many=True)
    cashback = serializers.SerializerMethodField()
    price_month = serializers.SerializerMethodField()
    is_followed = serializers.SerializerMethodField()

    class Meta:
        model = Service
        fields = (
            'name',
            'icon',
            'tags',
            'cashback',
            'price_month',
            'is_followed'
        )

    def get_cashback(self, obj):
        rates_with_cashback = obj.rates.all()
        if rates_with_cashback:
            max_cashback_rate = max(
                rates_with_cashback, key=lambda rate: rate.cashback
            )
            return max_cashback_rate.cashback
        return None

    def get_price_month(self, obj):
        rates_with_price = obj.rates.all()
        if rates_with_price:
            min_cashback_rate = min(
                rates_with_price, key=lambda rate: rate.price_month
            )
            return min_cashback_rate.price_month
        return None

    def get_is_followed(self, obj):
        user = self.context.get("view").request.user
        if user.is_anonymous:
            # Добавлено на время разработки
            return False
        rate_ids = obj.rates.values_list('id', flat=True)
        return user.subscriptions.filter(
            rate_id__in=rate_ids
        ).exists()


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
    services = ServiceCategorySerializer(
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


class RateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rate
        fields = (
            'id',
            'name',
            'price',
            'price_month',
            'duration',
            'cashback',
            'is_active'
        )


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = (
            'id',
            'image',
        )


class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = (
            'id',
            'icon',
            'name'
        )


class ServiceSerializer(serializers.ModelSerializer):
    tags = TagSerializer(
        many=True,
        read_only=True
    )
    options = OptionSerializer(
        many=True,
        read_only=True
    )
    rates = RateSerializer(
        many=True,
        read_only=True
    )
    images = ImageSerializer(
        many=True,
        read_only=True
    )

    class Meta:
        model = Service
        fields = (
            'id',
            'name',
            'short_description',
            'description',
            'category',
            'tags',
            'options',
            'rates',
            'images',
            'url'
        )
