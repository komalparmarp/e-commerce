from django.shortcuts import render
from .serializers import *
from .models import *
from rest_framework import generics
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.exceptions import ValidationError, PermissionDenied, NotAcceptable
from myapp.models import Product


# Create your views here.
class CartGetView(generics.RetrieveAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartViewSerializer

    def get(self, request):
        cart = CartItem.objects.all()
        serializer = CartViewSerializer(cart, many=True)
        return Response(serializer.data)


class CartCreateView(generics.CreateAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer

    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        print(serializer)
        if serializer.is_valid():
            # serializer.save()
            serializer.create(serializer.validated_data, request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class CartUpdateView(generics.RetrieveUpdateAPIView):
#     # queryset = CartItem.objects.all()
#     serializer_class = CartItemSerializer
#
#     def get_object(self, pk):
#         try:
#             return CartItem.objects.get(pk=pk)
#         except:
#             raise ValidationError("objects dosen't exist")
#
#     def patch(self, request, pk):
#         cart = self.get_object(pk=pk)
#         print(cart)
#         serializer = self.serializer_class(cart, data=request.data)
#         if serializer.is_valid():
#             serializer.update(cart, serializer.validated_data)
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_200_OK)
#
class CartUpdateQuantityView(generics.UpdateAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartUpdateSerializer
    permission_classes = [AllowAny]

    def put(self, request, *args, **kwargs):
        cart_item = CartItem.objects.get(pk=self.kwargs['pk'])
        product_price = cart_item.product.product_price
        data = request.data
        cart_item.quantity = data['quantity']
        cart_item.price = product_price * data['quantity']

        cart_item.save()
        serializer = CartUpdateSerializer(cart_item)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CartRetrieveView(generics.RetrieveAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartRetrieveSerializer

    def get(self, request, pk):
        cart = CartItem.objects.get(pk=pk)
        serializer = CartRetrieveSerializer(cart)
        return Response(serializer.data)


class CartDeleteView(generics.DestroyAPIView):
    queryset = CartItem.objects.all()
    permission_classes = [AllowAny]

    def delete(self, request, pk):
        cart = CartItem.objects.get(pk=pk)
        cart.delete()
        return Response(status=status.HTTP_200_OK, data={'detail': 'cart-item deleted'})

# def validate(self, attrs):
#
#     if current_item.count() > 0:
#         raise NotAcceptable("You already have this cart")
#     try:
#         quantity = int(request.data['quantity'])
#     except Exception as e:
#         raise ValidationError("enter valid quantity")
# cart_item = product_price * data['quantity']

#     if quantity > product.quantity:
#         raise NotAcceptable("Sorry")
#
#     cart_item = CartItem(cart=cart, product=product, quantity=quantity)
#     cart_item.save()
# serializer = CartItemSerializer(cart_item)
# total = float(product.product_price) * float(quantity)
# cart.save()
# return Response(serializer.data, status=status.HTTP_201_CREATED)
