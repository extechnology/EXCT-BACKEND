from rest_framework import serializers
from .models import (
    ConnectUS,
    CarrerEnquiry,
    BannerVideo
)


class ConnectUSSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConnectUS
        fields = '__all__'

class CarrerEnquirySerializer(serializers.ModelSerializer):
    class Meta:
        model = CarrerEnquiry
        fields = '__all__'

class BannerVideoSerizlizer(serializers.ModelSerializer):
    class Meta:
        model = BannerVideo
        fields = ['video']