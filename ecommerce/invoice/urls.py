from django.urls import path, include
from .views import *

urlpatterns = [
    # path('invoice', InvoiceView.as_view(), name='invoice_create')
    path('invoice/', GenerateInvoice.as_view(), name='generate_invoice'),
    path('invoice_download/', DownloadInvoice.as_view(), name="download_invoice"),
    path('share_invoice/', ShareInvoice.as_view(), name="share_invoice")
]
