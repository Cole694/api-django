from django.contrib import admin
from .models import Product, Catalogue

# Register your models here.

class CatalogueInline(admin.TabularInline):
    model = Catalogue.product.through

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ('name', 'sku')

@admin.register(Catalogue)
class CatalogueAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']