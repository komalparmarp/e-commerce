from django.shortcuts import render
from rest_framework import generics
from .models import *
from .serializers import *
import stripe
from rest_framework import views
from rest_framework.decorators import api_view
from rest_framework import status

# # Create your views here.
# class PaymentListView(generics.ListAPIView):
#     queryset = PaymentGetway.objects.all()
#     serializer_class = PaymentGetSerializer
#
#
# class PaymentCraeteView(generics.CreateAPIView):
#     queryset = PaymentGetway.objects.all()
#     serializer_class = PaymentCraeteSerializer
#
#
stripe.api_key = "sk_test_51KYQVuSCUKV9rHL1UH7HC5lEkCZAW9KMwhgwaw9npCjxws0eEzn2h14ByjqknLJpnEROVtdRIpWlP9kG4Ql55vZ000KXyZI5yr"


@api_view(['GET', 'POST'])
def test_payment(request):
    test_payment_intent = stripe.PaymentIntent.create(amount=1000, currency='pln',
                                                      payment_method_types=['card'],
                                                      receipt_email='komal612412@gmail.com')
    return Response(status=status.HTTP_200_OK, data=test_payment_intent)


@api_view(['GET', 'POST'])
def save_stripe_info(request):
    data = request.data
    email = data['email']
    payment_method_id = data['payment_method_id']

    # creating customer
    customer = stripe.Customer.create(
        email=email,
        payment_method=payment_method_id)
    print(email)
    print(payment_method_id)

    return Response(status=status.HTTP_200_OK,
                    data={
                        'message': 'Success',
                        'data': {'customer_id': customer.id}})


YOUR_DOMAIN = 'http://localhost:8000'


@api_view(['POST'])
def create_checkout_session(request):
    try:
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    # Provide the exact Price ID (for example, pr_1234) of the product you want to sell
                    'price': '{{PRICE_ID}}',
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url=YOUR_DOMAIN,
            # + '/success.html',
            cancel_url=YOUR_DOMAIN,
            # + '/cancel.html',
        )
    except Exception as e:
        return str(e)

    return Response(checkout_session.url, status=status.HTTP_200_OK)

# if __name__ == '__main__':
#     app.run(port=4242)

