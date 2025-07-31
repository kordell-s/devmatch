from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class Project(models.Model):
    title = models.CharField(max_length=255)
    github_url = models.URLField(blank=True, null=True)
    live_url = models.URLField(blank=True, null=True)
    description = models.TextField()
    technologies = models.JSONField(default=list, blank=True)
    project_image = models.ImageField(upload_to='project_images/', blank=True, null=True)
    owner = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE, related_name='projects')

    def __str__(self):
        return self.title
