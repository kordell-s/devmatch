from django import forms
from profiles.models import Developer

class DeveloperForm(forms.ModelForm):
    class Meta:
        model = Developer
        fields = [
            'profile_picture', 
            'bio', 
            'location',
            'phone',
            'email',
            'linkedin_url',
            'skills',
            'resume', 
            'video_intro',
            'github_url', 
            'portfolio_url',
            'experience'
        ]
        
        widgets = {
            'profile_picture': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'bio': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4, 
                'placeholder': 'Tell us a little about yourself...'
            }),
            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., London, UK'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., +1 (555) 123-4567'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'your.email@example.com'
            }),
            'linkedin_url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://linkedin.com/in/username'
            }),
            'skills': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Python, Django, React'
            }),
            'resume': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf,application/pdf'
            }),
            'video_intro': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'video/*'
            }),
            'github_url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://github.com/username'
            }),
            'portfolio_url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://yourportfolio.com'
            }),
            'experience': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Years of professional experience'
            }),
        }

    def clean_skills(self):
        skills = self.cleaned_data.get('skills')
        if isinstance(skills, str):
            skills_list = [skill.strip() for skill in skills.split(',') if skill.strip()]
            return skills_list
        return skills if skills else []


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #converting skills list back to comma-separated strings
        if self.instance and self.instance.skills:
            self.fields['skills'].initial = ', '.join(self.instance.skills)


