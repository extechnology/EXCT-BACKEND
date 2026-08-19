from django.contrib import admin
from django.utils.html import mark_safe
from .models import ConnectUS, CarrerEnquiry, BannerVideo, ExShop

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

@admin.register(ExShop)
class ExShopAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'image_preview')
    search_fields = ('name', 'description')
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="60" height="60" style="object-fit:cover;border-radius:4px;" />')
        return "No image"
    image_preview.short_description = 'Image Preview'