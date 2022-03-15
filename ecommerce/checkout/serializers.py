from rest_framework import serializers
from .models import *
from address.models import Address
from cart.serializers import CartItemCreateSerializer
from cart.models import CartItem
from address.serializers import AddressSerializer, AddressCreateSerializer
# from coupon.serializers import CouponViewSerializer
from cart.models import Cart


class CheckoutViewSerializer(serializers.ModelSerializer):
    address = AddressSerializer()

    # coupon=CouponViewSerializer()

    class Meta:
        model = CheckOut
        fields = ['id', 'customer', 'cart', 'address', ]
        # 'coupon']


class CheckoutSerializer(serializers.ModelSerializer):
    country = serializers.CharField(max_length=20, allow_null=True, allow_blank=True)
    state = serializers.CharField(max_length=20, allow_null=True, allow_blank=True)
    city = serializers.CharField(max_length=30, allow_null=True, allow_blank=True)
    street_address = serializers.CharField(max_length=50, allow_null=True, allow_blank=True)
    pincode = serializers.CharField(max_length=16, allow_null=True, allow_blank=True)

    # cart = serializers.PrimaryKeyRelatedField(queryset=CartItem.objects.all(), required=True)
    # cart = serializers.StringRelatedField(read_only=True)
    # cart = serializers.SerializerMethodField('get_cart')

    # check_cart = CartItemSerializer(read_only=True)

    class Meta:
        model = CheckOut
        fields = ['id', 'customer', 'cart', 'country', 'state', 'city', 'street_address', 'pincode', ]
        # 'coupon']

    # def get_cart(self, cart):
    #     # check = cart.cart
    #     print(cart)
    #     # return check

    def create(self, validated_data):
        cart = validated_data.pop('cart', None)
        print(cart)
        # coupon = validated_data.pop('coupon', None)
        # print(coupon)

        # check_cart = validated_data.pop("cart", None)
        customer = validated_data.pop("customer", None)
        address = Address.objects.create(country=validated_data['country'],

                                         customer=customer,
                                         state=validated_data['state'],
                                         city=validated_data['city'],
                                         street_address=validated_data['street_address'],
                                         pincode=validated_data['pincode'],
                                         )
        print(cart)
        c = CheckOut.objects.create(cart=cart, customer=customer, address=address, )
        # coupon=coupon)

        return address
