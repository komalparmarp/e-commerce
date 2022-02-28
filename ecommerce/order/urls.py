from django.urls import path, include
# from .views import OrderCreateView, OrderRetrieveView, OrderDeleteView, OrderUpdateView, OrderView
from .views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('order', OrderViewSet)

urlpatterns = [
    path('', include(router.urls)),


    # path('order-view', OrderView.as_view(),)
    # path('order-create', OrderCreateView.as_view(), name='create-order'),
    # path('order-update/<int:pk>', OrderUpdateView.as_view(), name='update-order'),
    # path('order-Retrieve/<int:pk>', OrderRetrieveView.as_view(), name='retrieve-order'),
    # path('order-delete/<int:pk>', OrderDeleteView.as_view(), name='create-order')

]
