from django.db import models
from django.contrib.auth.models import AbstractUser
from PIL import Image
from django.utils import timezone
from django.conf import settings
from taggit.managers import TaggableManager


class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = [
        ('individual', 'Individual'),
        ('organization', 'Organization'),
    ]
    
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='individual')

    def __str__(self):
        return self.username


def profile_image_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/profile_images/<filename>
    return f"profile_images/{filename}"

def background_image_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/background_images/<filename>
    return f"background_images/{filename}"

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    background = models.ImageField(default="default.jpg", upload_to="profile_background")
    avatar = models.ImageField(default='default.jpg', upload_to='profile_images')
    phone = models.CharField(max_length=50, blank=True)
    email = models.EmailField(max_length=75, blank=True)
    bio = models.TextField()
    grade = models.TextField(default='N/A')
    school = models.TextField(default='N/A')
    skills = TaggableManager()
    has_applied = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    # resizing images
    def save(self, *args, **kwargs):
        super().save()

        img = Image.open(self.avatar.path)

        if img.height > 100 or img.width > 100:
            new_img = (100, 100)
            img.thumbnail(new_img)
            img.save(self.avatar.path)

class OrganizationProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    organization_name = models.CharField(max_length=50, default="N/A")
    background = models.ImageField(default="default.jpg", upload_to="profile_background")
    avatar = models.ImageField(default='default.jpg', upload_to='profile_images')
    phone = models.CharField(max_length=50, blank=True)
    email = models.EmailField(max_length=75, blank=True)
    about = models.TextField()
    full_address = models.TextField(default='N/A')
    website = models.URLField(blank=True)
    domain = models.CharField(max_length=70, default="N/A")
    keywords = TaggableManager()

    def __str__(self):
        return self.organization_name

    # resizing images
    def save(self, *args, **kwargs):
        super().save()

        img = Image.open(self.avatar.path)

        if img.height > 100 or img.width > 100:
            new_img = (100, 100)
            img.thumbnail(new_img)
            img.save(self.avatar.path)
class Experience(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    title = models.CharField(max_length=10)
    org = models.CharField(max_length=25)
    time_period = models.CharField(max_length=10)
    description = models.TextField(max_length=200)

    def __str__(self):
        return self.title
    
class Education(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    title = models.CharField(max_length=10)
    inst = models.CharField(max_length=25)
    time_period = models.CharField(max_length=10)
    description = models.TextField(max_length=200)

    def __str__(self):
        return self.title

class ContactRequest(models.Model):
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='sent_contact_requests')
    receiver = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='received_contact_requests')
    email = models.CharField(max_length=50)
    message = models.TextField()
    send_date =  models.DateTimeField(auto_now_add=True)

class Exp(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    location = models.CharField(max_length=50, default="New York, NY")
    length = models.CharField(max_length=50, default='less_than_a_week')
    slug = models.SlugField(unique=True, max_length=100)
    num_applications = models.IntegerField(default=0)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

class Edu(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    location = models.CharField(max_length=50, default="New York, NY")
    length = models.CharField(max_length=50, default='less_than_a_week')
    slug = models.SlugField(unique=True, max_length=100)
    num_applications = models.IntegerField(default=0)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
