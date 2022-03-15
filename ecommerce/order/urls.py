from django.urls import path, include
from .views import *

urlpatterns = [
    path('order-view', OrderAPI.as_view(), name='view-order'),

]
