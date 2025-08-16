from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError



def validate_project_image_size(value):
    filesize = value.size
    if filesize > 5 * 1024 * 1024:
        raise ValidationError("Project image size must be under 5MB")
    return value





# Create your models here.

class Project(models.Model):
    title = models.CharField(max_length=255)
    github_url = models.URLField(blank=True, null=True)
    live_url = models.URLField(blank=True, null=True)
    description = models.TextField()
    technologies = models.JSONField(default=list, blank=True)
    owner = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE, related_name='projects')
    project_image = models.ImageField(upload_to='project_images/', blank=True, 
                                      null=True, validators=[validate_project_image_size], help_text="Upload a project image (max 5MB)")
    
    def __str__(self):
        return self.title

    @property
    def project_image_url(self):
        """Returns the URL of the project image if it exists."""
        if self.project_image:
            return self.project_image.url
        return None
