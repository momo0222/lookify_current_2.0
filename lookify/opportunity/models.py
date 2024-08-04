from django.db import models
from django.conf import settings
from django.utils import timezone
# Create your models here.
from taggit.managers import TaggableManager
from PIL import Image
class Opportunity(models.Model):
    CATEGORY_CHOICES = [
        ('academic_enrichment', 'Academic Enrichment'),
        ('extracurricular_activities', 'Extracurricular Activities'),
        ('stem', 'STEM'),
        ('internships_work_experience', 'Internships and Work Experience'),
        ('community_service_volunteering', 'Community Service and Volunteering'),
        ('leadership_development', 'Leadership Development'),
        ('college_career_readiness', 'College and Career Readiness'),
        ('personal_development', 'Personal Development'),
        ('cultural_global_awareness', 'Cultural and Global Awareness'),
        ('health_wellness', 'Health and Wellness'),
        ('arts_creativity', 'The Arts and Creativity'),
    ]
    LENGTH_CHOICES = [
        ('less_than_a_week', 'Less than a week'),
        ('one_week_to_four', '1-4 weeks'),
        ('one_month_to_three', '1-3 months'),
        ('three_month_to_six', '3-6 months'),
        ('six_month_plus', '6+ months'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    location = models.CharField(max_length=50, default="New York, NY")
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='academic_enrichment')
    background = models.ImageField(default='default.jpg', upload_to='background_images')
    responsibilities = models.TextField(default="Add responsibilities for this responsibility")
    application_type = models.URLField(blank=True, null=True) 
    grade = models.CharField(max_length=35, default="10th Grade")
    length = models.CharField(max_length=50, choices=LENGTH_CHOICES, default='less_than_a_week')
    pub_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    like = models.BooleanField(default=False)
    slug = models.SlugField(unique=True, max_length=100)
    num_applications = models.IntegerField(default=0)
    tags = TaggableManager()
    visits = models.IntegerField(default = 0)

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        self.updated_date = timezone.now()
        super().save(*args, **kwargs)


class Experience(models.Model):
    experience1 = models.CharField(max_length=50, default="mcd")
    experience2 = models.CharField(max_length=50, default="tagerty")

    def __str__(self):
        return (self.experience1 + " " + self.experience2)

class Application(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending' ),
        ('ACCEPTED', 'Accepted'),
        ('REJECTED', 'Rejected')
        ]
    opportunity = models.ForeignKey(Opportunity, on_delete=models.CASCADE)
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField()
    send_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=25, choices = STATUS_CHOICES, default='PENDING')
    contact = models.TextField()

