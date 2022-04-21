from itertools import product
from urllib import request
from .models import Product, Catalogue
from rest_framework import serializers
from django.core.exceptions import ValidationError as ModelValidationError
from rest_framework.exceptions import ValidationError, APIException

class CatalogueSerializer(serializers.ModelSerializer):

    class Meta:
        model = Catalogue
        fields = ['name', 'description']

class ProductSerializer(serializers.ModelSerializer):
    catalogue = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    def create(self, validated_data):
        try:
            return Product.objects.create(**validated_data)
        except ModelValidationError as e:
            raise ValidationError(
                code=409,
                detail=e.message
            )

    class Meta:
        model = Product
        fields = ['sku', 'name', 'product_description', 'price', 'department', 'date_listed',
         'product_weight', 'product_height', 'product_width', 'product_length', 'product_image', 'product_rating', 'catalogue']

    

