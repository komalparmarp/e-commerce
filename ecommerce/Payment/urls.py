from django.urls import path
from .views import *

# from django.conf.urls import url
# from .views import test_payment, save_stripe_info, create_checkout_session
# stripe_list = ProductLandingPagView.as_view({
#     'get': 'list',
#     # 'post': 'create'
#     })

urlpatterns = [
    path('create-checkout-session/<int:pk>', create_checkout_session, name='create-checkout-session'),
    path('stripe/<int:pk>', ProductLandingPagView.as_view(), name='product-template'),
    path('create-payment-intent/<pk>', StripeIntentView.as_view(), name='stripe-intent'),

    path('webhook/stripe', stripe_webhook, name='webhook-stripe'),
    path('success', SuccessView.as_view(), name='success-view'),

    # path('create-payment-intent/<pk>', StripeIntentView.as_view(), name='stripe-intent'),
    # path('webhook/stripe', stripe_webhook, name='webhook-stripe'),
    # path('stripe/<int:pk>', stripe_list, name="stripe-list")

]

# ====================== Razorpay ======================
from django.urls import path

from .views import *

# urlpatterns = [
# path('pay/', start_payment, name="payment"),
# path('payment/success/', handle_payment_success, name="payment_success")
# ]
