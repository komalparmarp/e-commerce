from django.shortcuts import render
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from .models import *
from .serializers import *
from rest_framework import viewsets


# Create your views here.
class OrderView(generics.ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderViewSerializer


class OrderCreateView(generics.CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderCreateSerializer

    # def create(self, request, *args, **kwargs):


class OrderRetrieveView(generics.RetrieveAPIView):
    def get_object(self, pk):
        return Order.objects.get(pk=pk)

    def get(self, request, pk):
        coupon = self.get_object(pk)
        serializer_class = OrderRetrieveSerializer(coupon)

        return Response(serializer_class.data)


class OrderUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderUpdateSerializer

    def put(self, request, pk):
        coupon = Order.objects.get(pk=pk)
        serializer = OrderUpdateSerializer(coupon, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrderDeleteView(generics.RetrieveDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderUpdateSerializer

    def delete(self, request, *args, **kwargs):
        coupon = Order.objects.get(pk=self.kwargs['pk'])
        coupon.delete()

        return Response("Coupon Success-fully Delete", status=status.HTTP_400_BAD_REQUEST)

# class OrderViewSet(viewsets.ModelViewSet):
#     """
#         This viewset automatically provides `list`, `create`, `retrieve`,
#         update` and `destroy` actions for Coupon model.
#     """
#     queryset = Order.objects.all()
#     serializer_class = OrderCreateSerializer
#     # permission_classes = [IsAuthenticatedOrReadOnly]
#     # authentication_classes = [TokenAuthentication]
