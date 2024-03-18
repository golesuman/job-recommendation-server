from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework import response
from rest_framework import status
from recommendation.services.job_interaction_service import (
    create_interaction,
    get_job_details,
)
from django.db.models import Q
from .algorithms_v2 import TextAnalyzer

from recommendation.serializers import CompanySerializer, JobDetailsSerializer
from recommendation.models import Company, Job
from recommendation.utils.preprocess import remove_special_characters


from recommendation.services.job_recommendation_service import get_top_jobs

analyzer = TextAnalyzer()


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

            recommendations = []

            job_listings_dict = {}

            document = job_details.title
            job_skills = analyzer.preprocess_document(document)

            for skill in [skill for skill in job_skills if skill != ""]:
                skill = remove_special_characters(skill)
                # Exclude the current job and filter jobs containing the skill
                jobs = Job.objects.exclude(id=job_id).filter(
                    Q(title__icontains=skill) | Q(description__icontains=skill)
                )

                if jobs.count() > 0:
                    for job in jobs:
                        job_listings_dict[str(job.id)] = (
                            job.title + "," + job.description
                        )

                    recommendations.extend(
                        get_top_jobs(
                            filtered_jobs=jobs,
                            data=job_details.title,
                            # + job_details.skills for more accurate results
                            job_listings_dict=job_listings_dict,
                            model="cosine",
                        )
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
        try:
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
        except Exception as e:
            return response.Response({"data": "Internal Server Error"})


class JobsPageAPI(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        try:
            jobs = Job.objects.all()
            serializer = JobDetailsSerializer(instance=jobs, many=True)
            return response.Response(
                {"data": serializer.data}, status=status.HTTP_200_OK
            )
        except Exception as e:
            print(str(e))
            return response.Response({"data": "Internal Server Error"})


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
