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
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from .utils import Util
from .permissions import *


class UserView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # authentication_classes = [TokenAuthentication]
    permission_classes = [AllowAny]


class UserUpdate(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserUpdateSerializer


class ChangePasswordView(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = [IsAuthenticated]

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {'status': 'success',
                        'code': status.HTTP_200_OK,
                        'message': 'password update successfully',
                        'data': []}

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
            absurl = 'http://' + current_site + relativeLink
            # redirect_url + uidb64 + token
            email_body = 'Hello, \n Use llink below to reset your password \n' + \
                         "?redirect_url=" + absurl
            data = {'email_body': email_body, 'to_email': user.email,
                    'email_subject': 'Reset your password'}

            Util.send_email(data)
        return Response({'success': 'send a link to reset a password'}, status=status.HTTP_201_CREATED)


class PasswordTokenCheckAPI(generics.GenericAPIView):
    def get(self, request, uidb64, token):
        try:
            id = smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response({'error': 'Token is not valid, please request a new one'},
                                status=status.HTTP_401_UNAUTHORIZED)
            else:
                return Response({'success': True, 'message': 'Credentials Valid', 'uidb64': uidb64, 'token': token},
                                status=status.HTTP_200_OK)

        except DjangoUnicodeDecodeError as identifier:
            return Response({'error': 'Token is not valid, please request a new one'},
                            status=status.HTTP_401_UNAUTHORIZED)


class SetPasswordAPIView(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'success': True, 'message': 'Password reset successfully.'}, status=status.HTTP_200_OK)


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
            customer = Customer.objects.create(user=customer)
            data = CustomerRetrieveSerializer(customer).data
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomerList(generics.RetrieveAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerRetrieveSerializer

    def get(self, request, pk):
        customer = Customer.objects.get(pk=pk)
        serializer = CustomerRetrieveSerializer(customer)
        return Response(serializer.data)


class CustomerUpdate(generics.UpdateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerUpdateSerializer

    def put(self, request, *args, **kwargs):
        cust = Customer.objects.get(pk=self.kwargs['pk'])
        serializer = CustomerUpdateSerializer(cust, data=request.data)
        # serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            customer = serializer.update(cust, request.data)

            data = CustomerRetrieveSerializer(customer).data
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomerDeleteView(generics.DestroyAPIView):
    queryset = Customer.objects.all()
    permission_classes = [AllowAny]

    def delete(self, request, pk):
        cust = Customer.objects.get(pk=pk)
        cust.delete()
        return Response(status=status.HTTP_200_OK, data={'detail': 'customer deleted'})


class StoreView(generics.ListAPIView):
    queryset = StoreOwner.objects.all()
    serializer_class = StoreOwnerSerializer


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
            data = StoreOwner.objects.create(user=stores, store_name=store_name, store_id=store_id,
                                             address=address, city=city)
            data = StoreOwnerSerializer(data).data
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StoreUpdate(generics.UpdateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerUpdateSerializer

    def put(self, request, *args, **kwargs):
        store = StoreOwner.objects.get(pk=self.kwargs['pk'])
        serializer = CustomerUpdateSerializer(store, data=request.data)
        if serializer.is_valid():
            s = serializer.update(store, request.data)

            data = StoreOwnerSerializer(s).data
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StoreDeleteView(generics.DestroyAPIView):
    queryset = StoreOwner.objects.all()
    permission_classes = [AllowAny]

    def delete(self, request, pk):
        s = StoreOwner.objects.get(pk=pk)
        s.delete()
        return Response(status=status.HTTP_200_OK, data={'detail': 'store deleted'})


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
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductUpdateDeleteView(generics.RetrieveUpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    # permission_classes = [IsAuthenticatedOrReadOnly, IsStoreOwner, IsAdmin]

    def put(self, request, pk):
        product = Product.objects.get(pk=pk)
        serializer_class = ProductSerializer(product, data=request.data)
        if serializer_class.is_valid():
            serializer_class.save()
            return Response(serializer_class.data, status=status.HTTP_200_OK)
        return Response(serializer_class.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        product = Product.objects.get(pk=pk)
        product.delete()
        return Response(status=status.HTTP_400_BAD_REQUEST)
