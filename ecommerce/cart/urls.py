from django.urls import path, include
from .views import *

urlpatterns = [
    path('cart_create/', CartListCreateView.as_view(), name='cart_list_create'),
    path('cart_update_delete/<int:pk>', CartRetrieveUpdateDeleteView.as_view(), name='cart_update_delete'),

    path('cartitem_create/', CartItemCreateView.as_view(), name='cart_create'),
    path('cartitem-view/', CartItemGetView.as_view(), name='cart-get'),
    path('cartitem-retrieve/<int:pk>/', CartItemRetrieveView.as_view(), name='cart'),
    path('cartitem-delete/<int:pk>/', CartItemDeleteView.as_view(), name='cart-delete'),
    path('cartitem-update/<int:pk>/', CartItemUpdateQuantityView.as_view(), name='cart')
]
