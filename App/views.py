from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from .models import (
    ConnectUS,
    CarrerEnquiry,
    BannerVideo
)

from .serializers import (
    ConnectUSSerializer,
    CarrerEnquirySerializer,
    BannerVideoSerizlizer
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
            contact_us_notification_mail(
                instance.name,
                instance.contact,
                instance.idea,
                instance.subject,
                instance.reference
            )
            if '@' in str(contact):
                contact_replay_mail(
                    instance.name,
                    instance.contact,
                    instance.idea,
                    instance.subject,
                    instance.reference
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

            get_career_enquiry_mail(
                instance.name,
                instance.contact,
                instance.job_profile,
                instance.education,
                instance.skills,
                instance.resume
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
                    instance.resume
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
        serializer = BannerVideoSerizlizer(video)
        return Response(serializer.data)