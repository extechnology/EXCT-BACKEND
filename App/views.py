from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from .models import (
    ConnectUS,
    CarrerEnquiry,
    BannerVideo,
    ExShop
)

from .serializers import (
    ConnectUSSerializer,
    CarrerEnquirySerializer,
    BannerVideoSerizlizer,
    ExShopSerializer
)

from .emails import (
    contact_us_notification_mail,
    contact_replay_mail,
    get_career_enquiry_mail,
    career_replay_mail
)


from .mail_finder import find_email_from_resume


class ConnectUSView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = ConnectUSSerializer(data=request.data)
        if serializer.is_valid():
            instance = serializer.save()
            contact = instance.contact
            reference_path = instance.reference.path if instance.reference else None
            
            contact_us_notification_mail(
                instance.name,
                instance.contact,
                instance.idea,
                instance.subject,
                reference_path
            )
            if '@' in str(contact):
                contact_replay_mail(
                    instance.name,
                    instance.contact,
                    instance.idea,
                    instance.subject,
                    reference_path
                )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CarrerEnquiryView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = CarrerEnquirySerializer(data=request.data)
        if serializer.is_valid():
            instance = serializer.save()
            contact = instance.contact
            resume = instance.resume
            resume_path = instance.resume.path if instance.resume else None

            get_career_enquiry_mail(
                instance.name,
                instance.contact,
                instance.job_profile,
                instance.education,
                instance.skills,
                resume_path
            )
            
            emails = find_email_from_resume(resume) if resume else []
            to_email = emails[0] if emails else (contact if '@' in str(contact) else None)

            if to_email:
                career_replay_mail(
                    instance.name,
                    to_email,
                    instance.job_profile,
                    instance.education,
                    instance.skills,
                    resume_path
                )
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BannerVideoAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        videos = BannerVideo.objects.all()
        if not videos:
            return Response({"message": "No video found"}, status=status.HTTP_404_NOT_FOUND)
        video = videos[0]
        serializer = BannerVideoSerizlizer(video, context={'request': request})
        return Response(serializer.data)


class ExShopView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        shops = ExShop.objects.all().order_by('-id')
        serializer = ExShopSerializer(shops, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = ExShopSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ExShopDetailView(APIView):
    permission_classes = [AllowAny]

    def get_object(self, pk):
        try:
            return ExShop.objects.get(pk=pk)
        except ExShop.DoesNotExist:
            return None

    def get(self, request, pk):
        shop = self.get_object(pk)
        if not shop:
            return Response({"error": "Item not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = ExShopSerializer(shop, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        shop = self.get_object(pk)
        if not shop:
            return Response({"error": "Item not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = ExShopSerializer(shop, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        shop = self.get_object(pk)
        if not shop:
            return Response({"error": "Item not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = ExShopSerializer(shop, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        shop = self.get_object(pk)
        if not shop:
            return Response({"error": "Item not found"}, status=status.HTTP_404_NOT_FOUND)
        shop.delete()
        return Response({"message": "Item deleted successfully"}, status=status.HTTP_204_NO_CONTENT)