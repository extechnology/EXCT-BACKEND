from django.contrib import admin
from django.utils.html import mark_safe
from .models import ConnectUS, CarrerEnquiry, BannerVideo

@admin.register(ConnectUS)
class ConnectUSAdmin(admin.ModelAdmin):
    list_display = ('name', 'contact', 'subject')
    search_fields = ('name', 'contact', 'subject', 'idea')

@admin.register(CarrerEnquiry)
class CarrerEnquiryAdmin(admin.ModelAdmin):
    list_display = ('name', 'contact', 'job_profile')
    search_fields = ('name', 'contact', 'job_profile', 'education', 'skills')

@admin.register(BannerVideo)
class BannerVideoAdmin(admin.ModelAdmin):
    list_display = ('id', 'video_preview')
    readonly_fields = ('video_preview',)

    def video_preview(self, obj):
        if obj.video:
            return mark_safe(f'<video width="320" height="240" controls><source src="{obj.video.url}" type="video/mp4">Your browser does not support the video tag.</video>')
        return "No video uploaded"
    video_preview.short_description = 'Video Preview'