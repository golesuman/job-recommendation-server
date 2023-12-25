from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework import response
from rest_framework import status
from recommendation.services.job_interaction_service import (
    create_interaction,
    get_job_details,
    get_jobs_by_interaction,
)

from recommendation.serializers import CompanySerializer, JobDetailsSerializer
from recommendation.models import Company, Job
from recommendation.services.job_recommendation_service import JobRecommendationServices



class JobDetailsView(APIView):
    permission_classes = [AllowAny]
    # authentication_classes = {}

    def get(self, request, *args, **kwargs):
        user_id = request.user.id
        results = []
        job_id = self.kwargs.get("job_id")
        if user_id:
            interaction_type = "click"
            create_interaction(
                user_id=user_id, interaction_type=interaction_type, job_id=job_id
            )
            jobs = Job.objects.exclude(id=job_id)
            recommendation_service = JobRecommendationServices(
                documents=jobs, user_id=user_id
            )
            results = recommendation_service.get_recommendations(n=5)

        job_details = get_job_details(job_id)
        if job_details:
            serializer = JobDetailsSerializer(job_details)
            if len(results) > 0:
                recommended_serializer = JobDetailsSerializer(results, many=True)
                detail_response = {
                    "job_details": serializer.data,
                    "recommendations": recommended_serializer.data,
                }
                return response.Response({"data": detail_response})
            return response.Response(
                {"data": serializer.data}, status=status.HTTP_200_OK
            )
        return response.Response(
            {"data": "Job Doesn't Exist"}, status=status.HTTP_404_NOT_FOUND
        )


class JobApplyView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user_id = request.user.id
        job_id = request.data.get("job_id")
        interaction_type = "apply"
        resp = create_interaction(
            user_id=user_id, interaction_type=interaction_type, job_id=job_id
        )
        if resp is not None:
            return response.Response(
                {"data": "Applied Successfully"}, status=status.HTTP_200_OK
            )
        return response.Response(
            {"data": "Already Exists"},
            status=status.HTTP_400_BAD_REQUEST,
        )


class HomePageAPI(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        user_id = request.user.id
        jobs = Job.objects.all()
        if request.user is not None:
            recommendation_service = JobRecommendationServices(
                documents=jobs, user_id=user_id
            )
            results = recommendation_service.get_recommendations(n=5)
            recommended_serializer = JobDetailsSerializer(results, many=True)
            return response.Response({"data" : recommended_serializer.data}, status=status.HTTP_200_OK)
        serializer = JobDetailsSerializer(instance=jobs, many=True)
        return response.Response({"data": serializer.data}, status=status.HTTP_200_OK)


class CompanyDetailsAPI(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        company_id = self.kwargs.get("company_id")
        company = Company.objects.filter(id=company_id).first()
        # jobs = Job.objects.filter(company_id=company_id)
        if company:
            serializer = CompanySerializer(instance=company)
            return response.Response(
                {"data": serializer.data}, status=status.HTTP_200_OK
            )
        return response.Response(
            {"data": "Company Doesn't Exist"}, status=status.HTTP_404_NOT_FOUND
        )
