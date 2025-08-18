from django import forms
from .models import Project

class ProjectForm(forms.ModelForm):
    # Define common technology choices
    TECHNOLOGY_CHOICES = [
        ('Python', 'Python'),
        ('JavaScript', 'JavaScript'),
        ('Java', 'Java'),
        ('C#', 'C#'),
        ('C++', 'C++'),
        ('PHP', 'PHP'),
        ('Ruby', 'Ruby'),
        ('Go', 'Go'),
        ('Rust', 'Rust'),
        ('Swift', 'Swift'),
        ('Kotlin', 'Kotlin'),
        ('TypeScript', 'TypeScript'),
        ('Django', 'Django'),
        ('Flask', 'Flask'),
        ('React', 'React'),
        ('Vue.js', 'Vue.js'),
        ('Angular', 'Angular'),
        ('Node.js', 'Node.js'),
        ('Express.js', 'Express.js'),
        ('Spring Boot', 'Spring Boot'),
        ('Laravel', 'Laravel'),
        ('Ruby on Rails', 'Ruby on Rails'),
        ('ASP.NET', 'ASP.NET'),
        ('PostgreSQL', 'PostgreSQL'),
        ('MySQL', 'MySQL'),
        ('MongoDB', 'MongoDB'),
        ('SQLite', 'SQLite'),
        ('Redis', 'Redis'),
        ('HTML', 'HTML'),
        ('CSS', 'CSS'),
        ('Bootstrap', 'Bootstrap'),
        ('Tailwind CSS', 'Tailwind CSS'),
        ('SCSS', 'SCSS'),
        ('Docker', 'Docker'),
        ('AWS', 'AWS'),
        ('Google Cloud', 'Google Cloud'),
        ('Azure', 'Azure'),
        ('Heroku', 'Heroku'),
        ('Git', 'Git'),
        ('GitHub', 'GitHub'),
        ('GitLab', 'GitLab'),
    ]
    
    selected_technologies = forms.MultipleChoiceField(
        choices=TECHNOLOGY_CHOICES,
        widget=forms.CheckboxSelectMultiple(attrs={
            'class': 'form-check-input me-2'
        }),
        required=False,
        label='Select Technologies'
    )
    
    custom_technology = forms.CharField(
        max_length=200,
        required=False,
        label='Additional Technologies',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Add custom technologies separated by commas'
        })
    )
    
    class Meta:
        model = Project
        fields = ['title', 'description', 'github_url', 'live_url', 'selected_technologies', 'custom_technology', 'project_image']
        
        labels = {
            'title': 'Project Title',
            'description': 'Project Description',
            'github_url': 'GitHub Repository URL',
            'live_url': 'Live Demo URL',
            'project_image': 'Project Screenshot/Image',
        }
        
        help_texts = {
            'title': 'Enter a descriptive title for your project',
            'description': 'Describe what this project does and its key features',
            'github_url': 'Link to your GitHub repository (optional)',
            'live_url': 'Link to the live demo or deployed version (optional)',
            'project_image': 'Upload a screenshot or image of your project (max 5MB)',
        }
        
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., E-commerce Website'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Describe your project, its features, and what makes it special...'
            }),
            'github_url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://github.com/username/project'
            }),
            'live_url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://your-project.herokuapp.com'
            }),
            'project_image': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
        }

    def clean(self):
        cleaned_data = super().clean()
        selected_technologies = cleaned_data.get('selected_technologies', [])
        custom_technology = cleaned_data.get('custom_technology', '')
        
        # Combine selected and custom technologies
        technologies = list(selected_technologies)
        
        if custom_technology:
            custom_tech_list = [tech.strip() for tech in custom_technology.split(',') if tech.strip()]
            technologies.extend(custom_tech_list)
        
        # Store in the technologies field
        cleaned_data['technologies'] = technologies
        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        
        # Get the combined technologies from cleaned_data
        technologies = self.cleaned_data.get('technologies', [])
        instance.technologies = technologies
        
        if commit:
            instance.save()
        return instance

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Populate form fields when editing
        if self.instance and self.instance.technologies:
            existing_techs = self.instance.technologies
            predefined_choices = [choice[0] for choice in self.TECHNOLOGY_CHOICES]
            
            # Separate predefined and custom technologies
            selected = [tech for tech in existing_techs if tech in predefined_choices]
            custom = [tech for tech in existing_techs if tech not in predefined_choices]
            
            self.fields['selected_technologies'].initial = selected
            if custom:
                self.fields['custom_technology'].initial = ', '.join(custom)
