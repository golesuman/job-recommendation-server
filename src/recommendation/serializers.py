from rest_framework import serializers

from recommendation.models import Job


class CompanySerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    description = serializers.CharField()
    website = serializers.URLField()
    logo = serializers.CharField()


class JobDetailsSerializer(serializers.Serializer):
    id = serializers.CharField()
    title = serializers.CharField()
    description = serializers.CharField()
    company = CompanySerializer()
    location = serializers.CharField()
    job_type = serializers.CharField()
    category = serializers.CharField()
    salary = serializers.FloatField()
    posted_at = serializers.DateTimeField()
    expires_at = serializers.DateTimeField()

    def to_representation(self, instance):
        return {
            "id": instance.id,
            "title": instance.title,
            "description": instance.description,
            "company_name": instance.company.name,
            "company_description": instance.company.description,
            "company_website": instance.company.website,
            "logo": str(instance.company.logo),
            "location": instance.location,
            "job_type": instance.job_type,
            "category": instance.category,
            "salary": instance.salary,
            "posted_at": instance.posted_at,
            "expires_at": instance.expires_at,
            "similarity_score": self.context,
        }


class JobPostSerializer(serializers.Serializer):
    title = serializers.CharField()
    description = serializers.CharField()
    company_id = serializers.IntegerField()
    location = serializers.CharField()
    job_type = serializers.CharField()
    category = serializers.CharField()
