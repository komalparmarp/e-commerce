from django.shortcuts import render
from myapp.models import Product, User
from cart.models import Cart, CartItem
from .models import *
from address.models import Address
from rest_framework import generics
from .serializers import *
from rest_framework.response import Response
from rest_framework import status


# Create your views here.
class CheckoutView(generics.ListAPIView):
    queryset = CheckOut.objects.all()
    serializer_class = CheckoutSerializer

    def get(self, request, *args, **kwargs):
        checkout = CheckOut.objects.all()
        serializer_class = CheckoutViewSerializer(checkout, many=True)
        return Response(serializer_class.data)


class CheckoutCreateView(generics.CreateAPIView):
    queryset = CheckOut.objects.all()
    serializer_class = CheckoutSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid(raise_exception=True):
            # serializer.save()
            # customer = serializer.create(request.data)
            serializer.save()
            # Address.objects.create(user=customer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
