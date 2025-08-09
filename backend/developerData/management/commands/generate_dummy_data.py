from django.core.management.base import BaseCommand
from faker import Faker
import random
from profiles.models import Developer
from accounts.models import CustomUser
from projects.models import Project

class Command(BaseCommand):
    help = "Generate dummy developers and projects"

    def handle(self, *args, **kwargs):
        fake = Faker()

        # Skills list for JSONField
        skills_list = ["Python", "Django", "JavaScript", "React", "HTML", "CSS", "PostgreSQL", "AWS", "Docker", "Node.js", "Vue.js", "MongoDB"]
        
        # Technologies list for projects
        tech_list = ["Python", "Django", "React", "JavaScript", "HTML", "CSS", "PostgreSQL", "MongoDB", "AWS", "Docker", "Git"]

        # Create developers and projects
        for _ in range(10):  # 10 developers
            user = CustomUser.objects.create_user(
                username=fake.user_name(),
                email=fake.email(),
                password="password123",
                role='developer',
                first_name=fake.first_name(),
                last_name=fake.last_name()
            )
            
            developer = Developer.objects.create(
                user=user,
                bio=fake.paragraph(nb_sentences=5),
                location=fake.city(),
                skills=random.sample(skills_list, k=random.randint(3, 7)),
                github_url=f"https://github.com/{fake.user_name()}",
                experience=random.randint(0, 10),
                portfolio_url=f"https://{fake.user_name()}.dev"
            )

            # Create projects for each developer
            for _ in range(random.randint(1, 4)):
                Project.objects.create(
                    owner=user,
                    title=fake.sentence(nb_words=3).replace('.', ''),
                    description=fake.paragraph(nb_sentences=4),
                    github_url=f"https://github.com/{user.username}/{fake.slug()}",
                    live_url=f"https://{fake.slug()}.herokuapp.com" if random.choice([True, False]) else None,
                    technologies=random.sample(tech_list, k=random.randint(2, 5))
                )

        self.stdout.write(self.style.SUCCESS("Dummy developers and projects created successfully!"))
