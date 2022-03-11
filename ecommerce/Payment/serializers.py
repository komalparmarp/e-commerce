from rest_framework import serializers
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError
from .models import *
from cart.serializers import CartRetrieveSerializer



# from cart.serializers import CartViewSerializer


class PaymentCreateSerializer(serializers.ModelSerializer):
    # order_date = serializers.DateTimeField(format="%d %B %Y %I:%M %p")

    class Meta:
        model = PaymentGateway
        fields = "__all__"
        # depth = 2
#     #
#     # def create(self, validated_data):
#     #     # print(validated_data)
#     #     # order_id = validated_data['order_id']
#     #     # status = validated_data['status']
#     #     # print(order_id)
#     #     # print(status)
#     #     # s = PaymentGetway.objects.create(order_id=order_id, status=status)
#     #     return PaymentGetway.objects.create(**validated_data)
#
# # class PaymentGetSerializer(serializers.ModelSerializer):
# #     cart = CartViewSerializer()
# #
# #     class Meta:
# #         model = PaymentGetway
# #         fields = '__all__'
# #
# #
# # class PaySerializer(serializers.ModelSerializer):
# #     class Meta:
# #         model = PaymentGetway
# #         fields = '__all__'
