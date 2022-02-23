from django.urls import path, include
from .views import CheckoutCreateView,CheckoutView

urlpatterns = [
    path('checkout-view', CheckoutView.as_view(), name='view-checkout'),

    path('checkout-create', CheckoutCreateView.as_view(), name='create-checkout')

]
