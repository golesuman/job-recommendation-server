import re
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
from account.models import Interaction, UserProfile
from recommendation.utils.preprocess import remove_special_characters


INTERACTION_LIMIT = 10


class HomePageAPI(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        user_id = request.user.id
        jobs = Job.objects.all()
        if user_id is not None:
            recommendations = []
            jobs = Job.objects.all()
            # Fetch jobs based on user profile skills
            interaction_data = Interaction.objects.filter(user=request.user)

            if interaction_data.count() > INTERACTION_LIMIT:
                recommendation_service = JobRecommendationServices(
                    documents=jobs, user_id=user_id, interaction=interaction_data
                )
                recommendations.extend(
                    recommendation_service.get_recommendations(n=5, model="pearson")
                )
            else:
                user_profile = UserProfile.objects.get(user_id=user_id)

                user_skills = (
                    user_profile.skills.split(",") if user_profile.skills else []
                )
                for skill in user_skills:
                    skill = remove_special_characters(skill)

                    if jobs.count() > 0:
                        # Apply recommendation algorithm on the filtered jobs
                        recommendation_service = JobRecommendationServices(
                            documents=jobs, user_id=user_id, interaction=None
                        )
                        recommendations.extend(
                            recommendation_service.get_recommendations(n=5)
                        )

            unique_recommendations = list(set(recommendations))

            if unique_recommendations:
                recommended_serializer = JobDetailsSerializer(
                    unique_recommendations, many=True
                )
                return response.Response(
                    {"data": recommended_serializer.data}, status=status.HTTP_200_OK
                )
        return response.Response({"data": None}, status=status.HTTP_200_OK)


class JobDetailsView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        try:
            user_id = request.user.id
            job_id = self.kwargs.get("job_id")
            # Fetch details for the original job
            job_details = get_job_details(job_id)

            if job_details:
                serializer = JobDetailsSerializer(job_details)
            if user_id is None:
                return response.Response(
                    {"data": serializer.data}, status=status.HTTP_200_OK
                )

            create_interaction(user_id=user_id, job_id=job_id, interaction_type="click")

            # Initialize an empty list to store recommendations
            recommendations = []

            # Fetch jobs based on user profile skills

            # Fetch user profile skills
            job_skills = (
                re.split(r"[\s,|]+", job_details.skills) if job_details.skills else []
            )
            # jobs = Job.objects.exclude(id=job_)
            for skill in [skill for skill in job_skills if skill != ""]:
                skill = remove_special_characters(skill)
                # Exclude the current job and filter jobs containing the skill
                jobs = Job.objects.exclude(id=job_id).filter(
                    title__icontains=skill.strip()
                )
                if jobs.count() > 0:
                    # Apply recommendation algorithm on the filtered jobs
                    recommendation_service = JobRecommendationServices(
                        documents=jobs,
                        job_details=job_details,
                        interaction=None,
                    )
                    recommendations.extend(
                        recommendation_service.get_recommendations(n=3)
                    )

            unique_recommendations = list(set(recommendations))

            if unique_recommendations:
                recommended_serializer = JobDetailsSerializer(
                    unique_recommendations, many=True
                )
                detail_response = {
                    "job_details": serializer.data,
                    "recommendations": recommended_serializer.data,
                }
                return response.Response({"data": detail_response})

            elif len(unique_recommendations) == 0:
                return response.Response(
                    {"data": serializer.data}, status=status.HTTP_200_OK
                )

            return response.Response(
                {"data": "Job Doesn't Exist"}, status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return response.Response(
                {"data": f"Internal Server Error {e}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
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


class JobsPageAPI(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        user_id = request.user.id
        jobs = Job.objects.all()
        if user_id is not None:
            recommendation_service = JobRecommendationServices(
                documents=jobs, user_id=user_id, interaction=None
            )
            results = recommendation_service.get_recommendations(n=20)
            recommended_serializer = JobDetailsSerializer(results, many=True)
            return response.Response(
                {"data": recommended_serializer.data}, status=status.HTTP_200_OK
            )
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
