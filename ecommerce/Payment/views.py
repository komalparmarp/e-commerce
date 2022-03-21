import stripe
import logging
from django.conf import settings
from django.http import JsonResponse
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .serializers import *
from rest_framework.views import APIView
from order.models import Order

stripe.api_key = settings.STRIPE_SECRET_KEY
endpoint_secret = settings.STRIPE_WEBHOOK_SECRET


class PaymentGateWayView(APIView):
    def get(self, request):
        payment = PaymentGateway.objects.all()
        serializer = PaymentCreateSerializer(payment, many=True)
        return Response(serializer.data)

    def post(self, request):
        data = request.data
        print(data, "======================================")
        order = Order.objects.get(pk=data['order_id'])
        YOUR_DOMAIN = "http://127.0.0.1:8000/"
        if PaymentGateway.objects.filter(order_id=order).exists():
            return Response({'Your Payment is Already Done'})
        else:
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[
                    {

                        'price_data': {'currency': 'inr',
                                       'unit_amount': int(order.total_amount),
                                       'product_data': {'name': order.user.username}},
                        # {'name': order.product.product_name,},

                        'quantity': 1,
                    },
                ],
                metadata={"order_id": order.id},
                mode='payment',
                success_url=YOUR_DOMAIN + 'payment_success',
                cancel_url=YOUR_DOMAIN + 'payment_cancel',
            )
            pay = PaymentGateway.objects.create(user=request.user,
                                                payment_type=data['payment_type'],
                                                order_id=order,
                                                status='Done'
                                                # transection_id=checkout_session['payment_intent'],
                                                )

            return JsonResponse({'url': checkout_session.url})


@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']

    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
        logging.info("message 1 %s", event)

    except ValueError as e:
        '''
            Invalid Payment
        '''
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        '''
            Invalid signature
        '''
        return HttpResponse(status=400)
    logging.info("message 1 %s", event)

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']['metadata']['order_id']
        pay = PaymentGateway.objects.get(order_id=session)
        if pay:
            pay.transaction_id = event['data']['object']['payment_intent']
            pay.save()
    return HttpResponse(status=status.HTTP_200_OK)


class SuccessView(APIView):
    def get(self, request):
        return Response({"msg", "Your Payment Has been Success!!!"})


class CancelView(APIView):
    def get(self, request):
        return Response({"Sorry", "Payment Cancel!!! Please Try Again"})
