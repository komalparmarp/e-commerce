from django.urls import path, include
from .views import OrderCreateView

urlpatterns = [

    path('order', OrderCreateView.as_view(), name='create-order')
]
