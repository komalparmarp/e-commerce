from django.urls import path
from .views import *

urlpatterns = [
    path('payment/', PaymentGateWayView.as_view(), name='payment'),
    path('webhook/stripe/', stripe_webhook, name='webhook-stripe'),
    path('payment_success/', SuccessView.as_view(), name='payment_success'),
    path('payment_cancel/', CancelView.as_view(), name='payment_cancel')
]
