# tests/factories.py

import factory
from django.contrib.auth.models import User
from account.models import UserProfile, Interaction
from recommendation.models import Company, Job
from django.contrib.auth.models import User


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f"user{n}")
    email = factory.LazyAttribute(lambda o: f"{o.username}@example.com")
    password = factory.PostGenerationMethodCall("set_password", "password")


class UserProfileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = UserProfile

    user = factory.SubFactory(UserFactory)
    skills = factory.Faker("words", nb=5)
    experience = factory.Faker("random_int", min=1, max=20)
    education = factory.Faker("sentence")
    location = factory.Faker("city")
    preferred_industry = factory.Faker("word")


class CompanyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Company

    user = factory.SubFactory(UserFactory)
    name = factory.Faker("company")
    description = factory.Faker("text")
    website = factory.Faker("url")


class JobFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Job

    company = factory.SubFactory(CompanyFactory)
    title = factory.Faker("job")
    description = factory.Faker("paragraph")
    location = factory.Faker("city")
    job_type = factory.Faker(
        "random_element", elements=["Full-Time", "Part-Time", "Contract", "Freelance"]
    )
    industry = factory.Faker("word")
    experience = factory.Faker("sentence")
    skills = factory.Faker("words", nb=5)
    role = factory.Faker("sentence")
    category = factory.Faker(
        "random_element", elements=["Entry-Level", "Mid-Level", "Senior-Level"]
    )
    salary = factory.Faker("random_element", elements=[None, "1000-2000", "2000-3000"])
    expires_at = factory.Faker("future_datetime", end_date="+30d")


class InteractionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Interaction

    user = factory.SubFactory(UserFactory)
    job = factory.SubFactory(JobFactory)
    interaction_type = factory.Faker("random_element", elements=["click", "apply"])


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f"user{n}")
    email = factory.LazyAttribute(lambda o: f"{o.username}@example.com")
    password = factory.PostGenerationMethodCall("set_password", "password")
