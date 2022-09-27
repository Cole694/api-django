from urllib import request
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.exceptions import ValidationError

from api.models import Catalogue, Product
from api.serializers import CatalogueSerializer, ProductSerializer
from rest_framework import permissions

class CatalogueViewSet(viewsets.ModelViewSet):
    queryset = Catalogue.objects.all()
    serializer_class = CatalogueSerializer
    permissions_classes = [permissions.IsAuthenticated]

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    template_name = 'product.html'
    permissions_classes = [permissions.IsAuthenticated]
# added this to test ssh with github