from .models import Admins, Events, Products, Sales
from rest_framework import serializers

class EventsSerializer(serializers.Serializer):
    model = Events
    fields = '__all__'

class AdminsSerializer(serializers.ModelSerializer):
    model = Admins
    fields = '__all__'

class ProductsSerializer(serializers.Serializer):
    model = Products
    fields = '__all__'

class SalesSerializer(serializers.Serializer):
    model = Sales
    fields = '__all__'
