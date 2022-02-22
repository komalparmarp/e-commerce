from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import *
from django.db import transaction
from .helpers import send_forgot_password_email
import uuid
from rest_framework.response import Response
from django.utils.encoding import force_str, DjangoUnicodeDecodeError, smart_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from rest_framework.exceptions import AuthenticationFailed
from django.http import HttpResponsePermanentRedirect
import os
from rest_framework import status
from phonenumber_field import phonenumber
from .utils import Util
from django.urls import reverse


# class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
#     @classmethod
#     def get_token(cls, user):
#         token = super(MyTokenObtainPairSerializer, cls).get_token(user)
#         token['username'] = user.username
#         return token

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'first_name', 'last_name', 'email', 'phone_number', 'is_customer',
                  'is_store_owner']

        extra_kwargs = {'password': {'write_only': True}}

    @transaction.atomic
    def create(self, validated_data):
        user = User.objects.create(first_name=validated_data['first_name'],
                                   last_name=validated_data['last_name'],
                                   username=validated_data['username'],
                                   phone_number=validated_data['phone_number'],
                                   email=validated_data['email'],
                                   password=validated_data['password'])

        user.set_password(validated_data['password'])
        if validated_data['is_customer']:
            user.is_customer = True
        else:
            user.is_store_owner = True
        user.save()
        # customer = Customer.objects.create(user=user)
        return user


class ChangePasswordSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=True)
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('id', 'old_password', 'new_password',)

    def validate(self, data):
        if not data.get('new_password') or not data.get('old_password'):
            raise serializers.ValidationError("please enter a password and confirm it ")

        return data

    def update(self, user, data):
        password = data['new_password']
        user.set_password(password)
        user.save()


# password reset by username
class ResetPasswordSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=100)
    password = serializers.CharField(max_length=100)

    class Meta:
        model = User
        fields = ['username', 'password']

    def save(self):
        username = self.validated_data['username']
        password = self.validated_data['password']
        if User.objects.filter(username=username).exists():
            user = User.objects.get(username=username)
            user.set_password(password)
            user.save()
            return user
        else:
            raise serializers.ValidationError({'error': 'please enter a valid data'})


## TRING TO SENT EMAIL FOR  A RESET PASSWORD


# class Password(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         field = ['forgot_password_token']
#         read_only_token = ['forgot_password_token']
#
#     def changepassword(request, token):
#         context = {}
#         try:
#             profile_obj = User.objects.filter(forgot_password_token=token).first()
#             print(profile_obj)
#         except Exception as e:
#             pass
#         return Response("change password")
#
#
# class ResetPasswordSerializer(serializers.ModelSerializer):
#     username = serializers.CharField(max_length=100)
#     password = serializers.CharField(max_length=100)
#
#     # forgot_password_token = serializers.CharField(max_length=100)
#
#     class Meta:
#         model = User
#         fields = ['username', 'password', ]
#
#     def create(self, validated_data):
#         try:
#             username = self.validated_data['username']
#             if not User.objects.filter(username=username).first():
#                 raise serializers.ValidationError("no user found in this username")
#             user_obj = User.objects.get(username=username)
#             token = str(uuid.uuid4())
#             profile_obj=User.objects.get(user=user_obj)
#             profile_obj.forword_password_token=token
#             send_forgot_password_email(user_obj.email, token)
#             return Response("email send")
#
#         except Exception as e:
#             print(e)
#             return Response("successfully send a mail")

class ResetPasswordEmailRequestSerializer(serializers.HyperlinkedModelSerializer):
    email = serializers.EmailField(min_length=2)

    redirect_url = serializers.CharField(max_length=500, required=False)

    class Meta:
        fields = ['email', 'url', ]


# def validate_username(self, username):
#     existing = User.objects.filter(username=username).first()
#     if existing:
#         raise serializers.ValidationError("Someone with that username already exist")
#     return username
#
#
class CustomRedirect(HttpResponsePermanentRedirect):
    allowed_schemes = [os.environ.get('APP_SCHEME'), 'http', 'https']


class SetNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(
        min_length=6, max_length=68, write_only=True)
    token = serializers.CharField(
        min_length=1, write_only=True)
    uidb64 = serializers.CharField(
        min_length=1, write_only=True)

    class Meta:
        fields = ['password', 'token', 'uidb64']

    def validate(self, attrs):

        uidb64 = attrs.pop('uidb64', None)
        token = attrs.get('token', None)

        redirect_url = self.context['request'].GET.get('redirect_url')
        try:
            id = smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                if len(redirect_url) > 3:
                    return CustomRedirect(redirect_url + '?token_valid=False')
                else:
                    return CustomRedirect(os.environ.get('FRONTEND_URL', '') + '?token_valid=False')

            if redirect_url and len(redirect_url) > 3:
                return CustomRedirect(
                    redirect_url + '?token_valid=True&message=Credentials Valid&uidb64=' + uidb64 + '&token=' + token)
            else:
                return CustomRedirect(os.environ.get('FRONTEND_URL', '') + '?token_valid=False')

        except DjangoUnicodeDecodeError as identifier:
            try:
                if not PasswordResetTokenGenerator().check_token(user):
                    return CustomRedirect(redirect_url + '?token_valid=False')

            except UnboundLocalError as e:
                return Response({'error': 'Token is not valid, please request a new one'},
                                status=status.HTTP_400_BAD_REQUEST)

            raise AuthenticationFailed('The reset link is invalid', 401)
        return super().validate(attrs)


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

        def create(self, validated_data):
            print("===============================")

            user = User.objects.create(

                first_name=validated_data['first_name'],
                last_name=validated_data['last_name'],
                email=validated_data['email'],
                phone_number=validated_data['phone_number'],

            )
            user.set_password(validated_data['password'])
            user.save()
            return user


class StoreSerializer(serializers.ModelSerializer):
    # store_id = models.PositiveIntegerField()
    # store_name = serializers.CharField(max_length=100)
    # address = serializers.CharField(max_length=100)
    # city = serializers.CharField(max_length=20, )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', ]

        def create(self, validated_data):
            user = User.objects.create(

                first_name=validated_data['first_name'],
                last_name=validated_data['last_name'],
                email=validated_data['email'],
                phone_number=validated_data['phone_number'],

            )
            user.set_password(validated_data['password'])
            user.save()
            return user


class DiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discount
        fields = ['discount_id', 'discount_type', 'discount_price']

    def validate(self, attrs):
        disc = Discount.objects.get(discount_price='discount_price')
        product = Product.objects.get(product_price='product_price')

        if disc.discount_type == 'flat':
            discount = product.product_price - disc.discount_price

        else:
            amount = product.product_price * (disc.discount_price / 100)
            discount = product.product_price - amount

        return discount


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"

        def create(self, validated_data):
            print("===============================")

            product = Product.objects.create(

                product_id=validated_data['product_id'],
                product_name=validated_data['product_name'],
                description=validated_data['description'],
                product_price=validated_data['product_price'])
            product.save()
            return product


# class CartProductSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Product
#         fields = ['product_name', 'product_price', 'store_id']
#
#
# class CartSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Cart
#         fields = ['user', 'item', 'quantity']
#
#
# class CartItemSerializer(serializers.ModelSerializer):
#     item = CartProductSerializer(required=False)
#
#     class Meta:
#         model = Cart
#         fields = ['item', 'quantity']
#
#
# class CartUpdateSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Cart
#         fields = ['item', 'quantity']
#
#
