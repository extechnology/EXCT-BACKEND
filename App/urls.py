from django.urls import path
from .views import (
    ConnectUSView,
    CarrerEnquiryView,
    BannerVideoAPIView
)

urlpatterns = [
    path('connect-us/', ConnectUSView.as_view(), name='connect-us'),
    path('career-enquiry/', CarrerEnquiryView.as_view(), name='career-enquiry'),
    path('banner-video/', BannerVideoAPIView.as_view(), name='banner-video'),
]