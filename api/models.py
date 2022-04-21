from cgitb import lookup
from datetime import datetime
from email.policy import default
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.validators import UniqueValidator
from django.forms import CharField
from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile
import random, string
from django.core.exceptions import ValidationError

# Create your models here.

department_choices = (('electronics', 'Electronics'), ('computers', 'Computers'),
 ('arts_and_crafts', 'Arts & Crafts'), ('automotive', 'Automotive'), ('womens_fasion', 'Womens fasion'),
 ('mens_fasion', 'Mens fasion'), ('health', 'Health'), ('movies_and_games', 'Movies & Games'),
 ('software', 'Software'), ('sports', 'Sports'),('books', 'Books'), ('general', 'General'))

def sku_generator(size=10, chars=string.ascii_lowercase+string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

class Product(models.Model):
    sku = models.CharField(max_length=10, default=sku_generator)
    name = models.CharField(max_length=225, default='item_name')
    product_description = models.TextField(max_length=1000, default='description')
    price = models.FloatField(validators=[MinValueValidator(0.1)], default=10.50)
    department = models.CharField(max_length=225, choices=department_choices, default='general')
    date_listed = models.DateTimeField(max_length=225, default=datetime.now)
    product_weight = models.FloatField(validators=[MinValueValidator(0.1)], default=0.1)
    product_height = models.FloatField(validators=[MinValueValidator(0)], default=1)
    product_width = models.FloatField(validators=[MinValueValidator(0)], default=1)
    product_length = models.FloatField(validators=[MinValueValidator(0)], default=1)
    product_image = models.ImageField(upload_to='images/', default='image/default.jpg')
    product_rating = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)], default=1)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def validate_unique(self, *args, **kwargs):
        if self.sku:
            if self.__class__.objects.filter(sku=self.sku).exists():
                raise ValidationError(
                    message='Invalid sku: This sku value already exists', 
                    code='invalid', 
                    params={'value': self.sku}
                )
        super(Product, self).validate_unique(*args, **kwargs)

    def save(self, *args, **kwargs):
            self.validate_unique()
            super(Product, self).save(*args, **kwargs)

class Catalogue(models.Model):
    name = models.CharField(max_length=225)
    description = models.TextField(max_length=1000)

    product = models.ManyToManyField(Product, related_name='catalogue')

    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name 
