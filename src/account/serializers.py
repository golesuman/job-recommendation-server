from rest_framework.serializers import ModelSerializer
from django.contrib.auth.models import User
from .models import UserProfile
from .models import UserProfile
from rest_framework import serializers
from recommendation.serializers import JobDetailsSerializer, CompanySerializer
from django.db import transaction


class InteractionSerializer(serializers.Serializer):
    job = JobDetailsSerializer()
    timestamp = serializers.CharField()


class UserProfileSerializer(serializers.Serializer):
    user = serializers.CharField()
    bio = serializers.CharField()
    skills = serializers.CharField()
    experience = serializers.IntegerField()
    education = serializers.CharField()
    location = serializers.CharField()
    preferred_industry = serializers.CharField()
    resume = serializers.CharField()
    is_active = serializers.BooleanField()


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "email")


class UserProfileSerializer(ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = UserProfile
        exclude = ("id",)


class UserInteractionSerializer:
    profile = UserProfileSerializer()
    interactions = InteractionSerializer(many=True)


class UserSignUpSerializer:
    username = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    password = serializers.CharField()
    confirmation_password = serializers.CharField()
    email = serializers.EmailField()
    skills = serializers.CharField()
    bio = serializers.CharField()
    profile_picture = serializers.ImageField(allow_null=True)
    skills = serializers.CharField(max_length=255, allow_blank=True, allow_null=True)
    experience = serializers.IntegerField(allow_null=True)
    education = serializers.CharField(max_length=255, allow_blank=True, allow_null=True)
    location = serializers.CharField(max_length=100, allow_blank=True, allow_null=True)
    preferred_industry = serializers.CharField(
        max_length=100, allow_blank=True, allow_null=True
    )
    resume = serializers.FileField(allow_null=True)

    @transaction.atomic
    def save(self):
        try:
            user = User.objects.create(
                username=self.username,
                first_name=self.first_name,
                last_name=self.last_name,
                password=self.password,
                email=self.email,
            )
            UserProfile.objects.create(
                user=user,
                bio=self.bio,
                profile_picture=self.profile_picture,
                skills=self.skills,
                experience=self.experience,
                education=self.education,
                location=self.location,
                preferred_industry=self.preferred_industry,
                resume=self.resume,
                is_active=True,
            )
        except Exception as e:
            raise e
