from django.urls import path, include
from .views import *

urlpatterns = [
    path('cart/', CartCreateView.as_view(), name='cart_create'),
    path('cart-view/', CartGetView.as_view(), name='cart-get'),

    # path('cart-update/<int:pk>/', CartUpdateView.as_view(), name='cart-update'),
    path('cart-delete/<int:pk>/', CartDeleteView.as_view(), name='cart-delete'),
    path('cart-update/<int:pk>/', CartUpdateQuantityView.as_view(), name='cart')
]
