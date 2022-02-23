from django.urls import path
from .views import *

urlpatterns = [
    path('address-view/', AddressView.as_view(), name='view-address'),

    path('address-create/', AddressCreateView.as_view(), name='create-address'),
    path('add-update/<int:pk>/', AddressUpdateView.as_view(), name='update-address')
]
