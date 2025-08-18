from django import forms
from profiles.models import Developer

# Predefined skills list
SKILL_CHOICES = [
    ('Python', 'Python'),
    ('JavaScript', 'JavaScript'),
    ('Java', 'Java'),
    ('C++', 'C++'),
    ('C#', 'C#'),
    ('PHP', 'PHP'),
    ('Ruby', 'Ruby'),
    ('Go', 'Go'),
    ('Rust', 'Rust'),
    ('Swift', 'Swift'),
    ('Kotlin', 'Kotlin'),
    ('TypeScript', 'TypeScript'),
    ('React', 'React'),
    ('Angular', 'Angular'),
    ('Vue.js', 'Vue.js'),
    ('Node.js', 'Node.js'),
    ('Django', 'Django'),
    ('Flask', 'Flask'),
    ('Express.js', 'Express.js'),
    ('Spring', 'Spring'),
    ('Laravel', 'Laravel'),
    ('Ruby on Rails', 'Ruby on Rails'),
    ('ASP.NET', 'ASP.NET'),
    ('HTML', 'HTML'),
    ('CSS', 'CSS'),
    ('SCSS/Sass', 'SCSS/Sass'),
    ('Bootstrap', 'Bootstrap'),
    ('Tailwind CSS', 'Tailwind CSS'),
    ('jQuery', 'jQuery'),
    ('PostgreSQL', 'PostgreSQL'),
    ('MySQL', 'MySQL'),
    ('MongoDB', 'MongoDB'),
    ('SQLite', 'SQLite'),
    ('Redis', 'Redis'),
    ('Oracle', 'Oracle'),
    ('AWS', 'AWS'),
    ('Azure', 'Azure'),
    ('Google Cloud', 'Google Cloud'),
    ('Docker', 'Docker'),
    ('Kubernetes', 'Kubernetes'),
    ('Git', 'Git'),
    ('Linux', 'Linux'),
    ('DevOps', 'DevOps'),
    ('CI/CD', 'CI/CD'),
    ('Machine Learning', 'Machine Learning'),
    ('Data Science', 'Data Science'),
    ('Mobile Development', 'Mobile Development'),
    ('UI/UX Design', 'UI/UX Design'),
    ('Testing', 'Testing'),
    ('Agile', 'Agile'),
]

class DeveloperForm(forms.ModelForm):
    skills = forms.MultipleChoiceField(
        choices=SKILL_CHOICES,
        widget=forms.CheckboxSelectMultiple(attrs={
            'class': 'form-check-input'
        }),
        required=False,
        help_text='Select all skills that apply to you'
    )

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
        
        labels = {
            'profile_picture': 'Profile Picture',
            'bio': 'About You',
            'location': 'Location',
            'phone': 'Phone Number',
            'email': 'Contact Email',
            'linkedin_url': 'LinkedIn Profile',
            'skills': 'Skills',
            'resume': 'Resume (PDF)',
            'video_intro': 'Video Introduction',
            'github_url': 'GitHub Profile',
            'portfolio_url': 'Portfolio Website',
            'experience': 'Years of Experience',
        }
        
        help_texts = {
            'profile_picture': 'Upload a professional photo (max 5MB)',
            'bio': 'Tell recruiters about your background and interests',
            'skills': 'Select all skills that apply to you',
            'resume': 'Upload your resume in PDF format (max 5MB)',
            'video_intro': 'Optional: Upload a brief video introduction (max 50MB)',
            'experience': 'Enter your years of professional development experience',
        }
        
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
                'placeholder': 'Years of professional experience',
                'min': '0'
            }),
        }

    def clean_skills(self):
        skills = self.cleaned_data.get('skills')
        # Convert tuple/list to list for JSONField storage
        return list(skills) if skills else []

    def __init__(self, *args, **kwargs):
        self.is_first_time = kwargs.pop('is_first_time', False)
        super().__init__(*args, **kwargs)
        
        # Set initial values for skills if editing existing profile
        if self.instance and self.instance.skills:
            self.fields['skills'].initial = self.instance.skills
        
        # Make certain fields required for first-time profile completion
        if self.is_first_time:
            self.fields['bio'].required = True
            self.fields['skills'].required = True
            self.fields['location'].required = True


