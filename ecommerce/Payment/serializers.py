from rest_framework import serializers
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError
from .models import *
from cart.serializers import CartViewSerializer


class PaymentCraeteSerializer(serializers.ModelSerializer):

    class Meta:
        model = PaymentGetway
        fields = "__all__"


class PaymentGetSerializer(serializers.ModelSerializer):
    cart = CartViewSerializer()

    class Meta:
        model = PaymentGetway
        fields = '__all__'

class PaySerializer(serializers.ModelSerializer):
    class Meta:
        model =PaymentGetway
        fields='__all__'