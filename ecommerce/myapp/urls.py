from django.urls import path
from .views import UserView, UserUpdate, ChangePasswordView, ResetPasswordView, ResetPasswordRequestEmail, \
    PasswordTokenCheckAPI, \
    CustomerView, CustomerUpdate, CustomerList, CustomerDeleteView, StoreView, StoreOwnerView, StoreUpdate, \
    StoreDeleteView, ProductView, \
    ProductUpdateDeleteView, ProductCreateView, \
    SetPasswordAPIView

from rest_framework.authtoken import views

user_list = UserView.as_view({
    'get': 'list',
    'post': 'create'
})

user_update = UserUpdate.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

urlpatterns = [
    path('users/', user_list, name='user-list'),
    path('user_update/<int:pk>/', user_update, name='user-list'),

    path('change_password/', ChangePasswordView.as_view(), name='change-password'),

    path('resetPassword/', ResetPasswordView.as_view(), name='reset-password'),

    path('password-reset-email/', ResetPasswordRequestEmail.as_view(), name='password-reset-email'),
    path('password-reset/<uidb64>/<token>/',
         PasswordTokenCheckAPI.as_view(), name='password-reset-confirm'),
    path('password-reset-complete/', SetPasswordAPIView.as_view(), name='password-reset-complete'),

    path('auth-token/', views.obtain_auth_token, name='auth-token'),

    path('customer/', CustomerView.as_view(), name='customer-create'),
    path('customer/<int:pk>', CustomerList.as_view(), name='customer-list'),
    path('customer_update/<int:pk>', CustomerUpdate.as_view(), name='customer-update'),
    path('customer_delete/<int:pk>', CustomerDeleteView.as_view(), name='customer-delete'),

    path('storeowner/', StoreOwnerView.as_view(), name='store-create'),
    path('storelist/', StoreView.as_view(), name='store-list'),
    path('store_update/<int:pk>', StoreUpdate.as_view(), name='store-update'),
    path('store_delete/<int:pk>', StoreDeleteView.as_view(), name='store-delete'),

    path('product-get/', ProductView.as_view(), name='product-view'),
    path('product-create/', ProductCreateView.as_view(), name='product-create'),
    path('product-update_delete/<int:pk>', ProductUpdateDeleteView.as_view(), name='product-update'),

]
