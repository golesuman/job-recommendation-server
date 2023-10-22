from collections.abc import Iterable
import os
from django.db import models
import uuid
# Create your models here.
from django.db import models
from django.contrib.auth.models import User

# from src.recommendation.models import Job
from recommendation.models import Job


INTERACTION_TYPE = (("click", "click"), ("apply", "apply"))


def get_file_path(self, instance, filename):
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return os.path.join('profile', filename)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True, null=True)
    profile_picture = models.ImageField(upload_to=get_file_path, blank=True, null=True)
    skills = models.CharField(max_length=255, blank=True, null=True)
    experience = models.PositiveIntegerField(blank=True, null=True)
    education = models.CharField(max_length=255, blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    preferred_industry = models.CharField(max_length=100, blank=True, null=True)
    resume = models.FileField(upload_to="resumes/", blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.user.username


class Interaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    interaction_type = models.CharField(max_length=20, choices=INTERACTION_TYPE)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "job", "interaction_type")

    def __str__(self) -> str:
        return f"{str(self.user.username)}-{str(self.job.title)}-{str(self.interaction_type)}"
