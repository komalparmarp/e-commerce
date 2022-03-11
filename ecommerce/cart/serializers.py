from .models import *
from rest_framework import serializers
from myapp.models import Product, User
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError, NotAcceptable, PermissionDenied
from rest_framework.response import Response
from coupon.models import Coupon


class CartProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['product_id', 'product_name', 'store_id', 'product_price', 'quantity']


class CartViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem

        fields = '__all__'


class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem

        fields = ('cart', 'quantity', 'product', 'coupon',)

    def create(self, validated_data, user):
        print(validated_data)
        product = validated_data['product']
        quantity = validated_data['quantity']
        cart = validated_data['cart']

        coupon = validated_data["coupon"]
        user = self.context.get('request').user

        print(product)

        amount = product.product_price * quantity
        coupon_amount = coupon.discount_amount
        if coupon.discount_type == 'F':
            total_price = amount - coupon.discount_amount
            print(total_price)
        else:
            discount = amount * (coupon_amount / 100)
            print(discount)
            total_price = amount - discount
            print()
        coupon_max_limit = coupon.max_limit
        user_limit = coupon.per_user
        if user:
            user_count = len(CartItem.objects.filter(cart=cart, coupon=coupon))
            coupon_count = len(CartItem.objects.filter(coupon=coupon))

            if coupon_count > user_limit:
                raise ValidationError("Coupon limit is over")
            if user_count > coupon_max_limit:
                raise ValidationError("Per User limit is Over")

            coupon.max_limit = coupon.max_limit - 1

            coupon.save()

        else:
            raise ValidationError("Coupon Doesn't")

        c = CartItem.objects.create(cart=cart,
                                    product=product,
                                    quantity=quantity,
                                    coupon=coupon,
                                    price=amount,
                                    total_price=total_price)

        return c


class CartUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ('quantity',)


class CartRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['cart', 'product', 'quantity', 'coupon', 'price', 'total_price']
