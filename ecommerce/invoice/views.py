from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from order.models import Order, OrderItem
from Payment.models import PaymentGateway

from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.core.mail import EmailMessage
from django.conf import settings


def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return result.getvalue()
    return None



class GenerateInvoice(APIView):

    def post(self, request, *args, **kwargs):
        template = get_template('pdf.html')
        data = request.data
        order_id = data['order_id']
        order = Order.objects.get(id=order_id)
        pay = PaymentGateway.objects.get(order_id=order)
        user = order.user
        order_items = OrderItem.objects.filter(order=order)
        pdf = render_to_pdf('pdf.html', {'order_item': order_items, 'payment': pay, 'user': user, 'order': order})
        return HttpResponse(pdf, content_type='application/pdf')


class DownloadInvoice(APIView):
    def post(self, request):
        # template = get_template('pdf.html')
        data = request.data
        order_id = data['order_id']
        order = Order.objects.get(id=order_id)
        payment = PaymentGateway.objects.get(order_id=order)
        user = order.user
        invoice = Invoice(user=user, order_id=order_id, payment_method=payment.payment_type,
                          payment_status=payment.status, total_amount=payment.payment_price)
        invoice.save()
        order_items = OrderItem.objects.filter(order=order)
        for i in order_items:
            InvoiceItem.objects.create(invoice=invoice, product=i.product, product_amount=i.price)

        pdf = render_to_pdf('pdf.html',
                            {'invoice': invoice, 'order_item': order_items, 'payment': payment, 'user': user,
                             'order': order})

        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = "Invoice_%s.pdf" % (data['order_id'])
            # content = "inline; filename = '%s'" % (filename)
            content = "attachment; filename = '%s'" % (filename)
            response['Content-Disposition'] = content
            return response
        return HttpResponse("not found")


class ShareInvoice(APIView):
    def post(self, request):
        template = get_template('pdf.html')
        data = request.data
        order_id = data['order_id']
        order = Order.objects.get(id=order_id)
        payment = PaymentGateway.objects.get(order_id=order)
        user = order.user
        invoice = Invoice(user=user, order_id=order_id, payment_method=payment.payment_type,
                          payment_status=payment.status, total_amount=payment.payment_price)
        invoice.save()
        order_items = OrderItem.objects.filter(order=order)
        for i in order_items:
            InvoiceItem.objects.create(invoice=invoice, product=i.product, product_amount=i.price)

        pdf = render_to_pdf('pdf.html',
                            {'invoice': invoice, 'order_item': order_items, 'payment': payment, 'user': user,
                             'order': order})

        if pdf:
            mail_subject = "Recent Order Details"
            email = EmailMessage(mail_subject, 'this is a message', settings.EMAIL_HOST_USER, [user.email])
            email.attach('new.pdf', pdf, "application/pdf")
            email.send()
        return Response({'msg': 'Invoice generated!'})

#
# from wkhtmltopdf.views import PDFTemplateView
#
#
# class MyPDF(PDFTemplateView):
#
#
#     order = Order.objects.get(id=order_id)
#     pay = PaymentGateway.objects.get(order_id=order)
#     user = order.user
#     order_items = OrderItem.objects.filter(order=order)
#
#     # cmd_options = {
#     #     'margin-top': 3,
#     # # }
#     # extra_context = {'users': Invoice.objects.all(), 'payment': PaymentGateway.objects.all(),
#     #                  'order': Order.objects.all(), 'item': OrderItem.objects.all()}
