import stripe
from rest_framework.views import View
import logging
from rest_framework import viewsets
from django.conf import settings
from django.http import JsonResponse
from .models import *
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from rest_framework import serializers
from .serializers import *
from rest_framework.decorators import api_view
from cart.views import CartRetrieveView
from cart.models import CartItem
from cart.serializers import CartRetrieveSerializer
from rest_framework import generics
from django.views.generic import TemplateView
from order.models import Order

stripe.api_key = settings.STRIPE_SECRET_KEY

#
#
print("=========================================Stripe Payment========================================")


class SuccessView(TemplateView):
    template_name = "success.html"


class ProductLandingPagView(generics.RetrieveAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartRetrieveSerializer

    def get_context_data(self, **kwargs):
        order = CartItem.objects.get(pk=self.kwargs['pk'])

        context = super(ProductLandingPagView, self).get_context_data(**kwargs)
        context.update({"order": order,
                        "STRIPE_PUBLISHABLE_KEY": settings.STRIPE_PUBLISHABLE_KEY
                        })
        return context


@api_view(['POST'])
def create_checkout_session(request, pk):
    order = CartItem.objects.get(pk=pk)
    # ord = Order.objects.get(pk=pk)
    print(ord)
    print(order)
    print(order.product)
    print(order.product.product_name)
    amount = int(order.total_price * 100)

    YOUR_DOMAIN = "http://127.0.0.1:8000"
    checkout_session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[
            {
                # Provide the exact Price ID (for example, pr_1234) of the product you want to sell
                'price_data': {'currency': 'inr',
                               'unit_amount': amount,
                               'product_data': {'name': order.product.product_name}},
                # 'price': product.price,
                'quantity': 1,
            },
        ],
        metadata={"product_id": order.id},
        mode='payment',
        success_url=YOUR_DOMAIN + '/success',
        cancel_url=YOUR_DOMAIN + '/cancel',
    )
    # pay = PaymentGateway.objects.create(transection_id=checkout_session['payment_intent'], order_id=order,
    #                                     status='Onhold')

    return JsonResponse({'url': checkout_session.url})


#

@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    print("++++++++++++++++++++++++++payload+++++++++++++++++", payload)
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    print("==============================================")
    print(sig_header)
    print("==============================================")

    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
        logging.info("mssage 1 %s", event)

    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)
    logging.info("mssage 1 %s", event)

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']

        customer_email = session["customer_details"]["email"]
        product_id = session["metadata"]["product_id"]
        print(product_id)
        order = CartItem.objects.get(id=product_id)
        logging.info("mssage 2 %s", order)
        logging.info("mssage 1 %s", session)

        print(order)
        # send_mail(
        #     subject="Here Is Your Order",
        #     message=f"ThankYou for Buy a Product.",
        #     recipient_list=[customer_email],
        #     from_email="komal.parmar@plutustec.com"
        # )
        logging.info("mssage 1 %s", event)

        print("========================================================================")

        # Fulfill the purchase...
        print(session)
    # Passed signature verification
    return HttpResponse(status=200)


class StripeIntentView(View):
    def post(self, request, *args, **kwargs):
        print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
        try:
            order = CartItem.objects.get(id=self.kwargs["pk"])
            # data = json.loads(request.data)
            # Create a PaymentIntent with the order amount and currency
            intent = order.PaymentIntent.create(
                amount=order.total_price,
                currency='inr',
                automatic_payment_methods={
                    'enabled': True,
                },

            )
            logging.info("mssage 10010010101010 %s", intent)

            return JsonResponse({
                'clientSecret': intent['client_secret']
            })
        except Exception as e:
            return JsonResponse({'error': str(e)})

#
# print("=============================RAZORPAY INTREGRETATION================================")
# import json
# import razorpay
# import environ
# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from django.http import JsonResponse
# from .models import *
# from .serializers import *
#
# client = razorpay.Client(auth=('rzp_test_gPZuypzwFWKOha', 'qJUix0M9wcajMXDnRNHNueWp'))
#
# #
# @api_view(['POST'])
# def start_payment(request):
#     context = {}
#     print("============Create payment==============")
#
#     amount = 5000
#     currency = 'INR'
#
#     payment = client.order.create(
#         {'amount': amount, 'currency': currency, 'payment_capture': '1', 'receipt': 'order_rcptid_11'})
#     order = PaymentGateway.objects.create(
#         price=amount,
#         # status=status
#         status=payment['status'],
#         transection_id=payment['id'],
#
#     )
#     serializer = PaymentCreateSerializer(order)
#
#     data = {
#         "payment": payment,
#         "order": serializer.data
#     }
#
#     return Response(data)
#
#
# @api_view(['POST'])
# def handle_payment_success(request):
#     response = request.data
#     print("===========================================================================")
#     print(request.data)
#     params_dict = {
#         'razorpay_payment_id': response['razorpay_payment_id'],
#         'razorpay_order_id': response['razorpay_order_id'],
#         'razorpay_signature': response['razorpay_signature']
#     }
#     check = client.utility.verify_payment_signature(params_dict)
#
#     if check is not None:
#         print("Redirect to error url or error page")
#         return Response({'error': 'Something went wrong'})
#
#     # if payment is successful that means check is None then we will turn isPaid=True
#
#     res_data = {
#         'message': 'payment successfully received!'
#     }
#
#     return Response(res_data)
# try:
#     status = client.utility.verify_payment_signature(params_dict)
#     return JsonResponse({'status': status['successfully created']})
# except:
#     pass
# # print(res)
# ord_id = ""
# raz_pay_id = ""
# raz_signature = ""

# @api_view(['POST'])
# def handle_payment_success(request):
#     res = json.loads(request.data["response"])
#     ord_id = ""
#     raz_pay_id = ""
#     raz_signature = ""
#     for key in res.keys():
#         if key == 'razorpay_order_id':
#             ord_id = res[key]
#         elif key == 'razorpay_payment_id':
#             raz_pay_id = res[key]
#         elif key == 'razorpay_signature':
#             raz_signature = res[key]
#
#     order = PaymentGateway.objects.get(transection_id=ord_id)
#     data = {
#         'razorpay_order_id': ord_id,
#         'razorpay_payment_id': raz_pay_id,
#         'razorpay_signature': raz_signature
#     }
#     client = razorpay.Client(auth=('rzp_test_b6a7ETby0KRMYF', '9noeqtgFNOAQAoQfl9qKNTWr'))
#     check = client.utility.verify_payment_signature(data)
#     if check is not None:
#         print("Redirect to error url or error page")
#         return Response({'error': 'Something went wrong'})
#     order.status = True
#     order.save()
#
#     res_data = {
#         'message': 'payment successfully received!'
#     }
#
#     return Response(res_data)
