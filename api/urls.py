from django import views
from django.db import router
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CatalogueViewSet, ProductViewSet

router = DefaultRouter()
router.register(r'catalogue', CatalogueViewSet, basename='catalogue')
router.register(r'product', ProductViewSet, basename='products')

urlpatterns = [
    path('api/', include(router.urls)),
]
