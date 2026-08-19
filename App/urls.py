from django.urls import path
from .views import (
    ConnectUSView,
    CarrerEnquiryView,
    BannerVideoAPIView,
    ExShopView,
    ExShopDetailView
)

urlpatterns = [
    path('connect-us/', ConnectUSView.as_view(), name='connect-us'),
    path('career-enquiry/', CarrerEnquiryView.as_view(), name='career-enquiry'),
    path('banner-video/', BannerVideoAPIView.as_view(), name='banner-video'),
    path('shop/', ExShopView.as_view(), name='shop-list-create'),
    path('shop/<int:pk>/', ExShopDetailView.as_view(), name='shop-detail'),
]