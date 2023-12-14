from django.db import models
from base.models import BaseModel
from django.utils.text import slugify
# Create your models here.

class Category(BaseModel):
    category_name = models.CharField(max_length=50)
    category_image = models.ImageField(upload_to='categories')
    category_slug = models.SlugField(unique=True, blank=True, null=True)

    def save(self, *args, **kwargs ):
        self.category_slug = slugify(self.category_name)
        super(Category, self).save(*args, **kwargs)

    def __str__(self, *args, **kwargs):
        return self.category_name
    
class ColorVariant(BaseModel):
    color = models.CharField(max_length=32)
    price = models.IntegerField(default=0)

    def __str__(self, *args, **kwargs):
        return f'{self.color} Rs.{self.price}'

class SizeVariant(BaseModel):
    size = models.CharField(max_length=32)
    price = models.IntegerField(default=0)  

    def __str__(self, *args, **kwargs):
        return f'{self.size} Rs.{self.price}' 

class Product(BaseModel):
    product_name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    price = models.IntegerField()
    description = models.TextField()
    product_slug = models.SlugField(unique=True, blank=True, null=True)
    size_variant = models.ManyToManyField(SizeVariant)
    color_variant = models.ManyToManyField(ColorVariant)

    def save(self, *args, **kwargs ):
        self.product_slug = slugify(self.product_name)
        super(Product, self).save(*args, **kwargs)

    def __str__(self, *args, **kwargs):
        return self.product_name
    
    def get_price_by_size(self, size):
        return self.price + SizeVariant.objects.filter(product = self, size =size).last().price

class ProductImage(BaseModel):
    product = models.ForeignKey(Product , related_name='product_images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products')

