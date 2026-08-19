from django.db import models

# Create your models here.

class ExCompanies(models.Model):
    logo = models.ImageField(upload_to='companies-logos/')
    name = models.CharField(max_length=200)
    
    def __str__(self):
        return self.name


class ExCareers(models.Model):
    company = models.ForeignKey(ExCompanies, on_delete=models.CASCADE, related_name="companies")
    title = models.CharField(max_length=200)
    description = models.TextField()
    location  = models.TextField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    status = models.CharField(max_length=100,
        choices=[
            ('hiring', 'Hiring'),
            ('closed', 'Closed'),
            ('hold', 'Hold'),
            ('completed', 'Completed'),
        ],
        default='hiring'
    )

    is_active  = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class ConnectUS(models.Model):
    name  = models.CharField(max_length=200)
    contact = models.CharField(max_length=400)
    idea = models.CharField(max_length=400)
    subject = models.TextField()
    reference = models.FileField(upload_to='references/', blank=True, null=True)

    def __str__(self):
        return self.name


class CarrerEnquiry(models.Model):
    carrer = models.ForeignKey(ExCareers, on_delete=models.CASCADE, null=True, blank=True, related_name="carrer_enquirys")
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

class ExShop(models.Model):
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to='shop-images/')
    description = models.TextField()
    price = models.FloatField()
    
    def __str__(self):
        return self.name