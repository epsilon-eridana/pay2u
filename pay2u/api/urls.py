from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CategoryViewSet, ServiceViewSet

app_name = 'api'

router_v1 = DefaultRouter()
router_v1.register('categories', CategoryViewSet, basename='categories')
router_v1.register('services', ServiceViewSet, basename='services')

urlpatterns = [
    path('v1/', include(router_v1.urls)),
]
