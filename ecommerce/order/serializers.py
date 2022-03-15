from rest_framework import serializers
from .models import *
from rest_framework.validators import ValidationError


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['user', 'order_status', 'total_amount']


class OrderItemCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem

        fields = ('order', 'quantity', 'product', 'coupon', 'price', 'total_price', 'user')

    def create(self, validated_data, user):

        product = validated_data['product']
        quantity = validated_data['quantity']
        cart = validated_data['order']

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
            user_count = len(OrderItem.objects.filter(cart=cart, coupon=coupon))
            coupon_count = len(OrderItem.objects.filter(coupon=coupon))

            if coupon_count > user_limit:
                raise ValidationError("Coupon limit is over")
            if user_count > coupon_max_limit:
                raise ValidationError("Per User limit is Over")

            coupon.max_limit = coupon.max_limit - 1

            coupon.save()

        else:
            raise ValidationError("Coupon Doesn't")

        c = OrderItem.objects.create(cart=cart,
                                     product=product,
                                     quantity=quantity,
                                     coupon=coupon,
                                     price=amount,
                                     total_price=total_price,
                                     user=u)

        return c
