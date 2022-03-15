from rest_framework.response import Response
from .serializers import *
from rest_framework.decorators import APIView
from cart.models import Cart, CartItem


class OrderAPI(APIView):
    def get(self, request):
        queryset = Order.objects.all()
        serializer = OrderSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        user = request.user
        data = request.data
        print("====================================", data)
        cart = Cart.objects.get(user=request.user)
        print(cart)
        cart_items = CartItem.objects.filter(cart=cart)

        print(cart_items)
        if cart_items:
            order = Order(user=user, order_status=data['order_status'])
            order.save()
        else:
            return Response({'error': 'please add a product in cart'})

        for item in cart_items:
            OrderItem.objects.create(user=request.user, product=item.product, price=item.price,
                                     quantity=item.quantity, order=order, coupon=item.coupon,
                                     total_price=item.total_price)

        # for item in cart_items:
        #     item.delete()
        return Response({"order_id": order.id, "order_amount": order.total_amount, "order_status": order.order_status})
