from rest_framework.serializers import ModelSerializer
from django.contrib.auth.models import User
from .models import UserProfile
from .models import UserProfile
from rest_framework import serializers
from recommendation.serializers import JobDetailsSerializer, CompanySerializer


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
