from rest_framework import serializers
from rest_framework import status
from .models import *
from cart.serializers import CartViewSerializer


class OrderViewSerializer(serializers.ModelSerializer):
    order_cart = CartViewSerializer()

    class Meta:
        model = Order
        fields = '__all__'


class OrderCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['created_by', 'order_address', 'order_cart', 'created_on', 'status'
                                                                             '']


class OrderRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'


class OrderUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['updated_by', 'order_address', 'order_cart', 'updated_on', 'status']


class OrderDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
