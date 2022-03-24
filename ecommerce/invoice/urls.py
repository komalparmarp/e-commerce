from django.urls import path, include
from .views import *

# from wkhtmltopdf.views import PDFTemplateView

urlpatterns = [
    path('invoice/', GenerateInvoice.as_view(), name='generate_invoice'),
    path('invoice_download/', DownloadInvoice.as_view(), name="download_invoice"),
    path('share_invoice/', ShareInvoice.as_view(), name="share_invoice"),
    # path('wk/', MyPDF.as_view(template_name='pdf.html', filename='my_pdf.pdf'), name='pdf')
]
