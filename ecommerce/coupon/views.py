from django.shortcuts import render
from .serializers import *
from .models import *
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status


# Create your views here.
class CouponViewSerializer(generics.ListAPIView):
    queryset = Coupon.objects.all()
    serializer_class = CouponViewSerializer


class CouponCreateView(generics.CreateAPIView):
    queryset = Coupon.objects.all()
    serializer_class = CouponCreateSerializer


class CouponRetrieveView(generics.RetrieveAPIView):
    def get_object(self, pk):
        return Coupon.objects.get(pk=pk)

    def get(self, request, pk):
        coupon = self.get_object(pk)
        serializer_class = CouponRetrieveSerializer(coupon)

        return Response(serializer_class.data)


class CouponUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Coupon.objects.all()
    serializer_class = CouponUpdateSerializer

    def put(self, request, pk):
        coupon = Coupon.objects.get(pk=pk)
        serializer = CouponUpdateSerializer(coupon, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CouponDeleteView(generics.RetrieveDestroyAPIView):
    queryset = Coupon.objects.all()
    serializer_class = CouponUpdateSerializer

    def delete(self, request, *args, **kwargs):
        coupon = Coupon.objects.get(pk=self.kwargs['pk'])
        coupon.delete()

        return Response("Coupon Success-fully Delete", status=status.HTTP_400_BAD_REQUEST)
