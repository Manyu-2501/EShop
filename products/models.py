from django.db import models
from base.models import BaseModel
# Create your models here.

class Category(BaseModel):
    category_name = models.CharField(max_length=50)
    category_image = models.ImageField(upload_to='categories')
    category_slug = models.SlugField(unique=True, blank=True, null=True)

class Product(BaseModel):
    product_name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    price = models.IntegerField()
    description = models.TextField()
    slug_field = models.SlugField(unique=True, blank=True, null=True)

class ProductImage(BaseModel):
    product = models.ForeignKey(Product , related_name='product_images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products')