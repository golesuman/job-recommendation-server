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


class UserSignUpSerializer(serializers.Serializer):
    username = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    password = serializers.CharField()
    confirmation_password = serializers.CharField()
    email = serializers.EmailField()
    skills = serializers.CharField()
    experience = serializers.IntegerField()
    education = serializers.CharField()
    location = serializers.CharField()
    preferred_industry = serializers.CharField()

    @transaction.atomic
    def save(self):
        try:
            user = User.objects.create(
                username=self.validated_data["username"],
                first_name=self.validated_data["first_name"],
                last_name=self.validated_data["last_name"],
                password=self.validated_data["password"],
                email=self.validated_data["email"],
            )
            UserProfile.objects.create(
                user=user,
                skills=self.validated_data["skills"],
                experience=self.validated_data["experience"],
                education=self.validated_data["education"],
                location=self.validated_data["location"],
                preferred_industry=self.validated_data["preferred_industry"],
                is_active=True,
            )
        except Exception as e:
            raise e
