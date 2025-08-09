from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

class CustomUser(AbstractUser):
    USER_ROLES= (
        ('developer', 'Developer'),
        ('recruiter', 'Recruiter'),
    )
    role = models.CharField(max_length=20, choices=USER_ROLES, default='developer')
    profile_photo = models.ImageField(upload_to='profile_photos/', blank=True, null=True)