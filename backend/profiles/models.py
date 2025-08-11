from django.db import models
from accounts.models import CustomUser

# Create your models here.
class Developer(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='developer_profile')
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    skills = models.JSONField(default=list, blank=True)
    resume = models.FileField(upload_to='resumes/', blank=True, null=True)
    video_intro = models.FileField(upload_to='video_intros/', blank=True, null=True)
    github_url = models.URLField(blank=True, null=True)
    experience = models.IntegerField(help_text="Years of experience", default=0)
    portfolio_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - Developer Profile"
    

class Recruiter(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='recruiter_profile')
    company_name = models.CharField(max_length=255, blank=True, null=True)
    company_website = models.URLField(blank=True, null=True)
    company_description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - Recruiter Profile"
