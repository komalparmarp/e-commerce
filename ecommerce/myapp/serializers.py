from rest_framework import serializers
from .models import *
from django.db import transaction
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from rest_framework.exceptions import AuthenticationFailed
from django.http import HttpResponsePermanentRedirect
import os


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

        return user


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'first_name', 'last_name', 'email', 'phone_number', 'is_customer',
                  'is_store_owner']


class ChangePasswordSerializer(serializers.Serializer):
    model = User

    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


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


class ResetPasswordEmailRequestSerializer(serializers.HyperlinkedModelSerializer):
    email = serializers.EmailField(min_length=2)

    redirect_url = serializers.CharField(max_length=500, required=False)

    class Meta:
        model = User
        fields = ['email', 'redirect_url', ]


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

        try:
            password = attrs.get('password')
            uidb64 = attrs.pop('uidb64', None)
            token = attrs.get('token', None)
            id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                raise AuthenticationFailed('The reset link is invalid', 401)

            else:
                user.set_password(password)
                user.save()

        except Exception as e:
            raise AuthenticationFailed('The reset link is invalid', 401)
        return super().validate(attrs)


class CustomerRetrieveSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Customer
        fields = "__all__"


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

        def create(self, validated_data):
            user = User.objects.create(
                username=validated_data['username'],
                first_name=validated_data['first_name'],
                last_name=validated_data['last_name'],
                email=validated_data['email'],
                phone_number=validated_data['phone_number'],

            )
            user.set_password(validated_data['password'])
            user.save()
            return user


class CustomerUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'first_name', 'last_name', 'email', 'phone_number']

    def update(self, instance, validated_data):
        # instance.user = validated_data.get('user', instance.user)
        instance.user.username = validated_data.get('username', instance.user.username)
        instance.user.password = validated_data.get('password', instance.user.password)
        instance.user.first_name = validated_data.get('first_name', instance.user.first_name)
        instance.user.last_name = validated_data.get('last_name', instance.user.last_name)
        instance.user.email = validated_data.get('email', instance.user.email)
        instance.user.phone_number = validated_data.get('phone_number', instance.user.phone_number)
        instance.user.save()
        return instance


class StoreOwnerSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = StoreOwner
        fields = '__all__'


class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

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


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'product_id', 'product_name', 'store_id', 'description', 'product_price', 'product_image',
                  ]

        def create(self, validated_data):
            print("===============================")

            product = Product.objects.create(

                product_id=validated_data['product_id'],
                product_name=validated_data['product_name'],
                description=validated_data['description'],
                product_price=validated_data['product_price'],
                store_id=validated_data['store_id'])
            product.save()
            return product
