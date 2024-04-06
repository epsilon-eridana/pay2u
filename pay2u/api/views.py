from rest_framework import status, viewsets

from .serializers import CategoryListSerializer, CategoryDetailSerializer
from services.models import Category


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategoryListSerializer

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return CategoryDetailSerializer
        return self.serializer_class
