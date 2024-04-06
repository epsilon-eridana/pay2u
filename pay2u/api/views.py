from rest_framework import status, viewsets, mixins

from .serializers import (
    CategoryListSerializer,
    CategoryDetailSerializer,
    ServiceSerializer
)
from services.models import Category, Service


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all().prefetch_related(
        'services'
    )
    serializer_class = CategoryListSerializer

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return CategoryDetailSerializer
        return self.serializer_class


class ServiceViewSet(
    mixins.RetrieveModelMixin,viewsets.GenericViewSet
):
    queryset = Service.objects.all().prefetch_related(
        'tags',
        'rates',
        'options',
        'images'
    )
    serializer_class = ServiceSerializer
