from django.urls import path
# from views import test_payment
# from django.conf.urls import url
from .views import test_payment, save_stripe_info, create_checkout_session

urlpatterns = [
    # path('payment-create', PaymentCraeteView.as_view(), name='payment-create'),
    # path('payment-view', PaymentListView.as_view(), name='payment-view')
    path('test-payment', test_payment),
    path('save-stripe-info', save_stripe_info),
    path('create_checkout_session', create_checkout_session)
]
