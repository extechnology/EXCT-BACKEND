from django.db import models

# Create your models here.

class ConnectUS(models.Model):
    name  = models.CharField(max_length=200)
    contact = models.CharField(max_length=400)
    idea = models.CharField(max_length=400)
    subject = models.TextField()
    reference = models.FileField(upload_to='references/', blank=True, null=True)

    def __str__(self):
        return self.name


class CarrerEnquiry(models.Model):
    name = models.CharField(max_length=200)
    contact = models.CharField(max_length=400)
    job_profile = models.CharField(max_length=200)
    education = models.TextField()
    skills = models.TextField()
    resume = models.FileField(upload_to='resumes/', blank=True, null=True)

    def __str__(self):
        return self.name


class BannerVideo(models.Model):
    video = models.FileField(upload_to='banner_video/')

    