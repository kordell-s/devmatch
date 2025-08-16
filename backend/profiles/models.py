from django.db import models
from django.core.exceptions import ValidationError
from django.core.files.storage import default_storage
from accounts.models import CustomUser


#functions to validate files in

def validate_file_size(value):
    filesize = value.size
    if filesize > 5 * 1024 * 1024:  # 5 MB limit
        raise ValidationError("File size must be under 5 MB")
    return value

def validate_video_size(value):
    filesize = value.size
    if filesize > 50 * 1024 * 1024:  # 50 MB limit
        raise ValidationError("Video size must be under 50 MB")

def validate_pdf_file(value):
    if not value.name.lower().endswith('.pdf'):
        raise ValidationError("Only PDF files are allowed.")
    return value

# Create your models here.
class Developer(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='developer_profile')
    profile_picture = models.ImageField(
        upload_to='profile_pictures/', 
        blank=True, 
        null=True,
        validators=[validate_file_size], 
        help_text="Upload a profile picture (max 5MB). Files stored on AWS S3."
    )
    bio = models.TextField(blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    linkedin_url = models.URLField(blank=True, null=True)
    skills = models.JSONField(default=list, blank=True)
    resume = models.FileField(
        upload_to='resumes/', 
        blank=True, 
        null=True,
        validators=[validate_pdf_file, validate_file_size], 
        help_text="Upload your resume in PDF format (max 5 MB). Files stored on AWS S3."
    )
    video_intro = models.FileField(
        upload_to='video_intros/', 
        blank=True, 
        null=True,
        validators=[validate_video_size],
        help_text="Upload a video introduction (max 50MB). Files stored on AWS S3."
    )
    github_url = models.URLField(blank=True, null=True)
    experience = models.IntegerField(help_text="Years of experience", default=0)
    portfolio_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - Developer Profile"
    

    @property
    def profile_picture_url(self):
        """Returns the URL of the profile picture if it exists."""
        if self.profile_picture:
            return self.profile_picture.url
        return None

    @property
    def resume_url(self):
        """Returns the URL of the resume if it exists."""
        if self.resume:
            return self.resume.url
        return None

    @property
    def video_intro_url(self):
        """Returns the URL of the video introduction if it exists."""
        if self.video_intro:
            return self.video_intro.url
        return None

class Recruiter(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='recruiter_profile')
    company_name = models.CharField(max_length=255, blank=True, null=True)
    company_website = models.URLField(blank=True, null=True)
    company_description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - Recruiter Profile"




