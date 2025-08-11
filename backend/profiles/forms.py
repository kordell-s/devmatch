from django import forms
from profiles.models import Developer

class DeveloperForm(forms.ModelForm):
    class Meta:
        model = Developer
        fields = [
            'profile_picture', 
            'bio', 
            'location', 
            'skills',
            'resume', 
            'video_intro',
            'github_url', 
            'portfolio_url',
            'experience'
        ]
        
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Tell us a little about yourself...'}),
            'location': forms.TextInput(attrs={'placeholder': 'e.g., London, UK'}),
            'github_url': forms.URLInput(attrs={'placeholder': 'https://github.com/username'}),
            'portfolio_url': forms.URLInput(attrs={'placeholder': 'https://yourportfolio.com'}),
            'experience': forms.NumberInput(attrs={'placeholder': 'Years of professional experience'}),
            'skills': forms.TextInput(attrs={'placeholder': 'e.g., Python, Django, React'})
        }

