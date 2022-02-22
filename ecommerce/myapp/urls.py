from django.urls import path, include
# from rest_framework.routers import DefaultRouter
from .views import UserView, ChangePasswordView, ResetPasswordView, ResetPasswordRequestEmail, PasswordTokenCheckAPI, \
    CustomerView, StoreOwnerView, ProductView, DiscountView, ProductUpdateDeleteView, ProductCreateView

from rest_framework.authtoken import views
from django.contrib.auth import views as auth_views

# router = DefaultRouter()
# router.register('customer', views.CustomerList)

user_list = UserView.as_view({
    'get': 'list',
    'post': 'create'
})

urlpatterns = [
    path('users/', user_list, name='user-list'),
    path('change_password/', ChangePasswordView.as_view(), name='change-password'),
    path('ResetPassword/', ResetPasswordView.as_view(), name='reset-password'),
    path('passwordresetemail/', ResetPasswordRequestEmail.as_view(), name='password-reset-email'),
    path('password-reset/<uidb64>/<token>/',
         PasswordTokenCheckAPI.as_view(), name='password-reset-confirm'),
    # path('reset_password', include('django_rest_passwordreset.urls', namespace='reset-password')),
    path('auth-token/', views.obtain_auth_token),

    path('customer/', CustomerView.as_view(), name='customer-view'),
    path('storeowner/', StoreOwnerView.as_view(), name='store-view'),

    path('discount/', DiscountView.as_view(), name='discount-view'),

    path('product-get/', ProductView.as_view(), name='product-view'),
    path('product-create/', ProductCreateView.as_view(), name='product-create'),
    path('product-update/<int:pk>', ProductUpdateDeleteView.as_view(), name='product-update'),

    # path('cart-create/', CartCreateView.as_view(), name='user__cart'),
    # path('cart-update/<int:pk>/', CartUpdateView.as_view(), name='cart-update')
]
