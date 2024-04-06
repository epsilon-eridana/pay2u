from rest_framework import status, viewsets

from .serializers import CategorySerializer
from services.models import Category


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет для модели категории."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
