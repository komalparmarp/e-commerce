from .models import *
from rest_framework import serializers
from myapp.models import Product, User
from rest_framework.exceptions import ValidationError, NotAcceptable, PermissionDenied
from myapp.serializers import ProductSerializer


class CartProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['product_id', 'product_name', 'store_id', 'product_price', 'quantity']


class CartListCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = "__all__"


class CartRetrieveUpdateDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = "__all__"


class CartItemViewSerializer(serializers.ModelSerializer):
    # product = ProductSerializer()

    class Meta:
        model = CartItem
        fields = '__all__'


class CartItemCreateSerializer(serializers.ModelSerializer):
    # product = ProductSerializer()

    class Meta:
        model = CartItem

        fields = ('cart', 'quantity', 'product', 'coupon', 'price', 'total_price', 'user')

    def create(self, validated_data, user):

        product = validated_data['product']
        quantity = validated_data['quantity']
        cart = validated_data['cart']

        coupon = validated_data["coupon"]
        u = validated_data["user"]
        user = self.context.get('request').user

        amount = product.product_price * quantity
        coupon_amount = coupon.discount_amount
        if coupon.discount_type == 'F':
            total_price = amount - coupon.discount_amount

        else:
            discount = amount * (coupon_amount / 100)

            total_price = amount - discount

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
                                    total_price=total_price,
                                    user=u)

        return c


class CartItemUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ('cart', 'quantity', 'price', 'coupon', 'product', 'total_price')


class CartItemRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['cart', 'product', 'quantity', 'coupon', 'price', 'total_price']
