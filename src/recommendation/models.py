from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify


class Company(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    website = models.URLField()
    logo = models.ImageField(upload_to="images/", blank=True, null=True)

    def __str__(self):
        return self.name


class Job(models.Model):
    company = models.ForeignKey(to=Company, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, null=True)
    description = models.TextField(null=True)
    location = models.CharField(max_length=255, null=True)
    job_type = models.CharField(
        max_length=255,
        choices=[
            ("Full-Time", "Full-Time"),
            ("Part-Time", "Part-Time"),
            ("Contract", "Contract"),
            ("Freelance", "Freelance"),
        ],
        default="Full-Time",
    )
    industry = models.CharField(max_length=255, null=True)
    experience = models.CharField(max_length=1000)
    skills = models.CharField(max_length=1000)
    role = models.CharField(max_length=255)
    category = models.CharField(max_length=255, default="Entry-Level")
    salary = models.CharField(null=True, blank=True, max_length=255)
    posted_at = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(blank=True, null=True, max_length=255)
    expires_at = models.DateTimeField(null=True)
    is_active = models.BooleanField(default=True)

    # def save(self, *args, **kwargs):
    #     # Generate a slug from the job title
    #     self.slug = slugify(self.title)
    #     super(Job, self).save(*args, **kwargs)

    def __str__(self):
        return self.title
