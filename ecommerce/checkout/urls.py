from django.urls import path, include
from .views import CheckoutCreateView

urlpatterns = [
    path('checkout-create', CheckoutCreateView.as_view(), name='create-checkout')

]
