from .models import *
from rest_framework import serializers
from myapp.models import Product, User
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError, NotAcceptable, PermissionDenied
from rest_framework.response import Response


class CartProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['product_id', 'product_name', 'store_id', 'product_price', 'quantity']


class CartItemSerializer(serializers.ModelSerializer):
    # product_id = serializers.IntegerField()

    class Meta:
        model = CartItem
        # fields = '__all__'
        fields = ('cart', 'quantity', 'product', 'price')
        # extra_keyword = {'quantity': {'required:True'},
        #                  'product_id': {'required:True'}, }

    def validate(self, attrs):
        print(attrs)
        product = attrs.get('product')
        quantity = attrs.get('quantity')
        user = attrs.get('user')

        if product is None:
            raise ValidationError("Product is Not Available")
        #
        return attrs

    def create(self, validated_data, user):

        print(validated_data)
        product = validated_data['product']
        quantity = validated_data['quantity']
        cart = validated_data['cart']
        price = validated_data["price"]
        # cart_obj = Cart.objects.get(user=user)
        # product_obj = Product.objects.get(id=product)
        print(product)

        try:
            quan = CartItem.objects.get(cart=cart,
                                        product=product,
                                        quantity=quantity, price=price)
            quan.quantity += 1
            # quan.cart.count += 1
            quan.cart.save()
            quan.save()


        except CartItem.DoesNotExist:

            CartItem.objects.create(cart=cart,
                                    product=product,
                                    quantity=quantity,
                                    price=price)


class CartUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ('quantity',)

    # def get_object(self, pk):
    #     try:
    #         return CartItem.objects.get(pk=pk)
    #     except:
    #         raise ValidationError("objects dosen't exist")
    #
    # def update(self, request, *args, **kwargs):
    #     # quantity = request.data['quantity']
    #
    #     instance = self.get_object(pk=self.kwargs['pk'])
    #     instance.quantity = request.data.get('quantity')
    #     instance.save()
    #     return instance
    #
