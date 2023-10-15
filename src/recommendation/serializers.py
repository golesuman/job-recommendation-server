from rest_framework import serializers

from recommendation.models import Job


class CompanySerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    description = serializers.CharField()
    website = serializers.URLField()
    logo = serializers.CharField()


class JobDetailsSerializer(serializers.Serializer):
    title = serializers.CharField()
    description = serializers.CharField()
    company = CompanySerializer()
    location = serializers.CharField()
    job_type = serializers.CharField()
    category = serializers.CharField()
    salary = serializers.FloatField()
    posted_at = serializers.DateTimeField()
    expires_at = serializers.DateTimeField()


class JobPostSerializer(serializers.Serializer):
    title = serializers.CharField()
    description = serializers.CharField()
    company_id = serializers.IntegerField()
    location = serializers.CharField()
    job_type = serializers.CharField()
    category = serializers.CharField()
