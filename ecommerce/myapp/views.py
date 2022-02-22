from django.shortcuts import render
from .models import *
from .serializers import *
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny, IsAdminUser
from rest_framework import generics
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.views import APIView
from rest_framework.decorators import action
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from .utils import Util
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError, PermissionDenied, NotAcceptable
import os
from django.http import HttpResponsePermanentRedirect
from .permissions import *
from rest_framework import permissions


# from rest_framework_simplejwt.views import TokenObtainPairView


# class MyObtainTokenPairView(TokenObtainPairView):
#     permission_classes = [IsAuthenticated]
#     serializer_class = MyTokenObtainPairSerializer
class UserView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [AllowAny]


class ChangePasswordView(generics.UpdateAPIView):
    """
    an end point for changing password
    """
    queryset = User.objects.all()
    serializer_class = ChangePasswordSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    lookup_field = 'pk'


def get_object(self):
    obj = User.objects.get(pk=self.kwargs['id'])
    return obj


def put(self, request, *args, **kwargs):
    instance = self.get_object()
    serializer = self.serializer_class(data=request.data)
    # print("----------------------------------------")
    # print("============================")
    if serializer.is_valid():
        # print(request.data)
        if not request.data['old_password']:
            return Response({"old_password": ['Wrong Password']}, status=status.HTTP_400_BAD_REQUEST)
        else:
            resp = serializer.update(instance, request.data)
        response = {'status': 'success',
                    'code': status.HTTP_200_OK,
                    'message': 'password update succesfully',
                    'data': []
                    }
        return Response(response)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


###### TOKEN BASED PASSWORDRESET
# class ResetPasswordView(generics.CreateAPIView):
#     queryset = User.objects.all()
#     serializer_class = ResetPasswordSerializer()
#
#     def get_object(self):
#         obj = User.objects.get(pk=self.kwargs['pk'], email=self.kwargs['email'])
#         return obj
#
#     def post(self, request, *args, **kwargs):
#         instance=self.get_object()
#

# ----- reset password by username


class ResetPasswordView(APIView):
    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        alldata = {}
        if serializer.is_valid(raise_exception=True):
            serializer.save()

            alldata['data'] = 'successfully register'
            print(alldata)
            return Response(alldata)
        return Response('failed')


#

# reset password by email
class ResetPasswordRequestEmail(generics.GenericAPIView):
    serializer_class = ResetPasswordEmailRequestSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        email = request.data.get('email')
        print(User.objects.filter(email=email).exists())
        if User.objects.filter(email=email).exists():
            user = User.objects.filter(email=email).first()
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            print(uidb64)
            token = PasswordResetTokenGenerator().make_token(user)
            print(token)
            current_site = get_current_site(request=request).domain
            relativeLink = reverse('password-reset-confirm', kwargs={'uidb64': uidb64, 'token': token})
            redirect_url = request.data.get('redirect_url', '')
            absurl = 'http://' + current_site + redirect_url + uidb64 + token
            email_body = 'Hello, \n Use llink below to reset your password \n' + \
                         "?redirect_url=" + absurl
            data = {'email_body': email_body, 'to_email': user.email,
                    'email_subject': 'Reset your password'}

            Util.send_email(data)
        return Response({'success': 'send a link to reset a password'}, status=status.HTTP_201_CREATED)


class PasswordTokenCheckAPI(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer
    permission_classes = [AllowAny]
    authentication_classes = [TokenAuthentication]

    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={"request": request})

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response("True")
        return Response("False")


class CustomerView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [AllowAny]

    def get(self, request):
        customer = User.objects.all()
        serializer = CustomerSerializer(customer, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            customer = serializer.create(request.data)
            customer.is_customer = True
            customer.save()
            Customer.objects.create(user=customer)
            return Response("Created Successfully", status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StoreOwnerView(generics.CreateAPIView):
    queryset = StoreOwner.objects.all()
    serializer_class = StoreSerializer
    permission_classes = [AllowAny]

    def get(self, request):
        stores = User.objects.all()
        serializer_class = StoreSerializer(stores, many=True)
        return Response(serializer_class.data)

    def post(self, request):
        data = request.data
        store_name = data.pop('store_name')
        store_id = data.pop('store_id', )
        address = data.pop('address', )
        city = data.pop('city', )
        print(type(data))
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            stores = serializer.create(request.data)
            stores.is_store_owner = True
            stores.save()
            StoreOwner.objects.create(user=stores, store_name=store_name, store_id=store_id,
                                      address=address, city=city)
            return Response("Store Successfully Create", status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DiscountView(generics.ListCreateAPIView):
    queryset = Discount.objects.all()
    serializer_class = DiscountSerializer
    permission_classes = [AllowAny]

    # def get(self, request):
    #     product = Product.objects.all()
    #     serializer = DiscountSerializer(product, many=True)
    #     return Response(serializer.data)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return serializers.ValidationError("Sorry,You Can't Get Discount Right now")


from django.conf import settings


class ProductView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]

    def get(self, request):

        product = Product.objects.all()
        page = self.paginate_queryset(product)
        if page is not None:
            serializer_class = ProductSerializer(page, many=True)
            return self.get_paginated_response(serializer_class.data)

        serializer_class = ProductSerializer(product, many=True)
        return Response(serializer_class.data)

    @property
    def paginator(self):
        if not hasattr(self, '_paginator'):

            if self.pagination_class is None:
                self._paginator = None
            else:
                self._paginator = self.pagination_class()

        return self._paginator

    def paginate_queryset(self, queryset):

        if self.paginator is None:
            return None
        return self.paginator.paginate_queryset(queryset, self.request, view=self)

    def get_paginated_response(self, data):
        assert self.paginator is not None
        return self.paginator.get_paginated_response(data)


class ProductCreateView(generics.CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response("Create SuccessFull", status=status.HTTP_201_CREATED)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProductUpdateDeleteView(generics.RetrieveUpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsStoreOwner, IsAdmin]

    def put(self, request, pk):
        product = Product.objects.get(pk=pk)
        serializer_class = ProductSerializer(product, data=request.data)
        if serializer_class.is_valid():
            serializer_class.save()
            return Response("Create SuccessFull", status=status.HTTP_200_OK)
        return Response(serializer_class.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        product = Product.objects.get(pk=pk)
        product.delete()
        return Response(status=status.HTTP_400_BAD_REQUEST)

# class CartCreateView(generics.ListCreateAPIView):
#     # queryset = Cart.objects.all()
#     serializer_class = CartSerializer
#
#     # permissions = [AllowAny]
#
#     def get_queryset(self):
#         user = self.request.user
#         queryset = Cart.objects.filter(user__cart=user)
#         return queryset
#
#     def post(self, request, *args, **kwargs):
#         user = request.user
#         cart = get_object_or_404(Cart, user=user)
#         item = get_object_or_404(Product, pk=request.data['product'])
#         current_item = Cart.objects.filter(cart=cart, item=item)
#
#         if user == item.user:
#             raise PermissionDenied("This is your product")
#
#         if current_item.count > 0:
#             raise NotAcceptable("This item is already in your Cart")
#
#         try:
#             quantity = int(request.data['quantity'])
#
#         except Exception as e:
#             raise ValidationError("Please Enter your Quantity")
#
#         cart_item = Cart(cart=cart, item=item, quantity=quantity)
#         cart_item.save()
#         serializer = CartItemSerializer(cart_item)
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
#
#
# class CartUpdateView(generics.RetrieveUpdateDestroyAPIView):
#     serializer_class = CartSerializer
#     queryset = Cart.objects.all()
#
#     def retrieve(self, request, *args, **kwargs):
#         cart_item = self.get_object()
#         if cart_item.cart.user != request.user:
#             raise PermissionDenied("Sorry")
#
#         serializer = self.get_serializer(cart_item)
#
#         return Response(serializer.data)
#
#     def update(self, request, *args, **kwargs):
#         cart_item = self.get_object()
#         print(request.data)
#         item = get_object_or_404(Product, pk=request.data['product'])
#
#         if cart_item.cart.user != request.user:
#             raise PermissionDenied("Sorry")
#
#         try:
#             quantity = int(request.data['quantity'])
#         except Exception as e:
#             raise ValidationError("Enter valid Quantity")
#         # if quantity > product.quantity:
#         #     raise NotAcceptable("Your order quantity more than the se")
#         serializer = CartUpdateSerializer(cart_item, data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)
#
#     def destroy(self, request, *args, **kwargs):
#         cart_item = self.get_object()
#         if cart_item.cart.user != request.user:
#             raise PermissionDenied("Sorry")
#         cart_item.delete()
#         return Response("Your Item has been Deleted", status=status.HTTP_204_NO_CONTENT)
# #
# # class CartUpdateView(generics.RetrieveUpdateAPIView):
# #     queryset = Cart.objects.all()
# #     serializer_class = CartSerializer
# #     permissions = [AllowAny]
# #
# #     def put(self, request, pk):
# #         cart = Cart.objects.get(pk=pk)
# #         serializer_class = CartSerializer(cart, data=request.data)
# #         if serializer_class.is_valid():
# #             serializer_class.save()
# #             return Response(serializer_class.data, status=status.HTTP_201_CREATED)
# #         return Response(serializer_class.data, status=status.HTTP_400_BAD_REQUEST)
# #
# #     def delete(self, request, pk):
# #         cart = Cart.objects.get(pk=pk)
# #         cart.delete()
# #         return Response("Object Delete Successfully")
