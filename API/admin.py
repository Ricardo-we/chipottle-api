from django.contrib import admin
from .models import Admins, Events, Products, Sales

# Register your models here.
admin.site.register(Admins)
admin.site.register(Events)
admin.site.register(Products)
admin.site.register(Sales)