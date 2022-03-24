from django.db import models
import datetime
# Create your models here.
class Products(models.Model):
    item_name = models.CharField(max_length=255)
    item_description = models.TextField()
    item_price = models.FloatField()
    item_image = models.ImageField(upload_to="chipottle-api/products")

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"

class Admins(models.Model):
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    admin_key = models.CharField(max_length=255, unique=True)
    
    class Meta:
        verbose_name = "Admin"
        verbose_name_plural = "Admins"

class Sales(models.Model):
    sold_product = models.ForeignKey(Products, on_delete=models.CASCADE)
    date = models.DateTimeField(default=datetime.datetime.now())
    class Meta:
        verbose_name = "Sale"
        verbose_name_plural = "Sales"

class Events(models.Model):
    event_name = models.CharField(max_length=255)
    event_image = models.ImageField(null=True, blank=True, upload_to="chipottle-api/products")

    class Meta:
        verbose_name = "Event"
        verbose_name_plural = "Events"