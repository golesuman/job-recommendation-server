from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify


class Company(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    website = models.URLField()
    logo = models.ImageField(upload_to="images/", blank=True, null=True)

    def __str__(self):
        return self.name


class Job(models.Model):
    company = models.ForeignKey(to=Company, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    location = models.CharField(max_length=100)
    job_type = models.CharField(
        max_length=20,
        choices=[
            ("Full-Time", "Full-Time"),
            ("Part-Time", "Part-Time"),
            ("Contract", "Contract"),
            ("Freelance", "Freelance"),
        ],
    )
    category = models.CharField(max_length=50)
    salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    posted_at = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True, blank=True, max_length=100)
    expires_at = models.DateTimeField()
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        # Generate a slug from the job title
        self.slug = slugify(self.title)
        super(Job, self).save(*args, **kwargs)

    def __str__(self):
        return self.title
