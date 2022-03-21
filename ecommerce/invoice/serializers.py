from rest_framework import serializers
from .models import *
from myapp.serializers import UserSerializer


class InvoiceSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Invoice
        fields = "__all__"
        # fields = ['id', 'payment_method', 'payment_status', 'order_id', 'total_amount', 'user']
