from rest_framework import serializers
from .models import *


class CouponViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coupon
        fields = '__all__'


class CouponCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coupon
        fields = ['created_by', 'promo_code', 'start_date', 'expire_date', 'max_limit', 'per_user', 'discount_type',
                  'discount_amount', 'created_on']


class CouponRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coupon
        fields = '__all__'


class CouponUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coupon
        fields = ['updated_by', 'promo_code', 'start_date', 'expire_date', 'max_limit', 'per_user', 'discount_type',
                  'discount_amount', 'updated_on']


class CouponDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coupon
        fields = ['promo_code', 'start_date', 'expire_date']
