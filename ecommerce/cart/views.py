from django.shortcuts import render
from .serializers import *
from .models import *
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.permissions import AllowAny, IsAuthenticated


class CartListCreateView(generics.ListCreateAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartListCreateSerializer


class CartRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartRetrieveUpdateDeleteSerializer

    def delete(self, request, pk):
        s = Cart.objects.get(pk=pk)
        s.delete()
        return Response(status=status.HTTP_200_OK, data={'detail': 'Your Cart Is Successfully Deleted'})


class CartItemGetView(generics.RetrieveAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemViewSerializer

    def get(self, request):
        cart = CartItem.objects.all()
        serializer = CartItemViewSerializer(cart, many=True)
        return Response(serializer.data)


class CartItemCreateView(generics.CreateAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemCreateSerializer

    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})

        if serializer.is_valid():
            data = serializer.create(serializer.validated_data, request.user)
            data = CartItemViewSerializer(data).data
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CartItemUpdateQuantityView(generics.UpdateAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemUpdateSerializer
    permission_classes = [AllowAny]

    def put(self, request, *args, **kwargs):
        cart_item = CartItem.objects.get(pk=self.kwargs['pk'])
        product_price = cart_item.product.product_price
        dis = cart_item.coupon.discount_amount
        dis_type = cart_item.coupon.discount_type
        data = request.data
        cart_item.quantity = data['quantity']
        cart_item.price = product_price * data['quantity']

        if dis_type == 'F':
            cart_item.total_price = cart_item.price - dis
        else:
            discount = cart_item.price - (dis / 100)
            cart_item.total_price = cart_item.price - discount

        cart_item.save()
        serializer = CartItemUpdateSerializer(cart_item)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CartItemRetrieveView(generics.RetrieveAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemRetrieveSerializer

    def get(self, request, pk):
        cart = CartItem.objects.get(pk=pk)
        serializer = CartItemRetrieveSerializer(cart)
        return Response(serializer.data)


class CartItemDeleteView(generics.DestroyAPIView):
    queryset = CartItem.objects.all()
    permission_classes = [AllowAny]

    def delete(self, request, pk):
        cart = CartItem.objects.get(pk=pk)
        cart.delete()
        return Response(status=status.HTTP_200_OK, data={'detail': 'cart-item deleted'})
