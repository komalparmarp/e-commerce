from rest_framework import serializers
from .models import *
from address.models import Address
from cart.serializers import CartItemSerializer


class CheckoutSerializer(serializers.ModelSerializer):
    country = serializers.CharField(max_length=20, allow_null=True, allow_blank=True)
    state = serializers.CharField(max_length=20, allow_null=True, allow_blank=True)
    city = serializers.CharField(max_length=30, allow_null=True, allow_blank=True)
    street_address = serializers.CharField(max_length=50, allow_null=True, allow_blank=True)
    pincode = serializers.CharField(max_length=16, allow_null=True, allow_blank=True)
    cart = CartItemSerializer(source='id')

    class Meta:
        model = CheckOut
        fields = ['customer', 'cart', 'country', 'state', 'city', 'street_address', 'pincode']

    def create(self, validated_data):
        cart = validated_data.pop("cart", None)
        customer = validated_data.pop("customer", None)
        print("=======================")
        print(cart)
        print(customer)
        print("=======================")

        address = Address.objects.create(country=validated_data['country'],
                                         customer=customer,
                                         state=validated_data['state'],
                                         city=validated_data['city'],
                                         street_address=validated_data['street_address'],
                                         pincode=validated_data['pincode'],
                                         )

        c = CheckOut.objects.create(cart=cart, customer=customer, address=address)
        c.save()
        return address
