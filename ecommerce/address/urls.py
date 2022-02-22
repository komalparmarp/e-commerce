from django.urls import path
from .views import *

urlpatterns = [
    path('address/', AddressCreateView.as_view(), name='create-address'),
    path('add-update/<int:pk>/', AddressUpdateView.as_view(), name='update-address')
]
