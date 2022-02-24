from django.urls import path, include
from .views import *

urlpatterns = [
    path('coupon-view', CouponViewSerializer.as_view(), name='view-coupon'),
    path('coupon-create', CouponCreateView.as_view(), name='create-coupon'),
    path('coupon-retrieve/<int:pk>', CouponRetrieveView.as_view(), name='retrieve-coupon'),
    path('coupon-update/<int:pk>', CouponUpdateView.as_view(), name='coupon-update'),
    path('coupon-delete/<int:pk>', CouponDeleteView.as_view(), name='coupon-delete')
]
