from django.db import models
from django.core.exceptions import ValidationError
from accounts.models import CustomUser
from profiles.models import Developer


# Create your models here.

class Watchlist(models.Model):
    recruiter = models.ForeignKey(
        CustomUser, 
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'recruiter'},
        related_name='watchlisted_developers'
    )
    developer = models.ForeignKey(
        Developer, 
        on_delete=models.CASCADE,
        related_name='watchlisted_by'
    )
    saved_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('recruiter', 'developer')  # prevents duplicate entries
        indexes = [
            models.Index(fields=['recruiter', 'saved_at']),
            models.Index(fields=['developer']),
        ]

    def clean(self):
        super().clean()
        if self.recruiter and self.recruiter.role != 'recruiter':
            raise ValidationError({'recruiter': 'Only recruiters can create watchlist entries.'})
        
        if self.recruiter and self.developer and self.recruiter == self.developer.user:
            raise ValidationError('A user cannot add themselves to their own watchlist.')

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.recruiter.username} - {self.developer.user.username} Watchlist"
