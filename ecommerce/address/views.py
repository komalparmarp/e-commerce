from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from .models import *
from .serializers import *
from rest_framework import status


class AddressView(generics.ListAPIView):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer

    def get(self, request, *args, **kwargs):
        address = Address.objects.all()
        serializer_class = AddressSerializer(address, many=True)
        return Response(serializer_class.data)


class AddressCreateView(generics.CreateAPIView):
    queryset = Address.objects.all()
    serializer_class = AddressCreateSerializer


class AddressUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer

    def put(self, request, *args, **kwargs):
        address = Address.objects.get(pk=self.kwargs['pk'])
        serializer_class = AddressSerializer(address, data=request.data)
        if serializer_class.is_valid():
            serializer_class.save()
            return Response(serializer_class.data, status=status.HTTP_200_OK)
        return Response(serializer_class.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        address = Address.objects.get(pk=pk)
        address.delete()
        return Response(status=status.HTTP_200_OK, data={'detail': 'address deleted'})
