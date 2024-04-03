from datetime import datetime, timedelta
from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.views import APIView
from rest_framework import response
from rest_framework import status
from recommendation.services.job_interaction_service import (
    create_interaction,
    get_job_details,
)
from django.db.models import Q, Count, Sum
from .algorithms_v2 import TextAnalyzer

from recommendation.serializers import CompanySerializer, JobDetailsSerializer
from recommendation.models import Company, Job
from recommendation.utils.preprocess import remove_special_characters


from recommendation.services.job_recommendation_service import get_top_jobs

analyzer = TextAnalyzer()

CACHE = {}
CACHE_EXPIRATION_TIME = timedelta(seconds=30)  # Cache expiration time (30 secs)


class JobDetailsView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        try:
            user_id = request.user.id
            job_id = self.kwargs.get("job_id")

            if user_id is not None:
                create_interaction(
                    user_id=user_id, job_id=job_id, interaction_type="click"
                )

            # Check if the data is cached and not expired
            cached_data = CACHE.get(job_id)
            if cached_data and not self.is_cache_expired(job_id):
                return response.Response(
                    {"data": cached_data.get("data")},
                    status=status.HTTP_200_OK,
                )

            # Fetch details for the original job
            job_details = get_job_details(job_id)

            if not job_details:
                return response.Response(
                    {"data": "Job Doesn't Exist"}, status=status.HTTP_404_NOT_FOUND
                )

            serializer = JobDetailsSerializer(job_details)

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
                recommendation_with_scores = []
                for sim, job in unique_recommendations:
                    job_serializer = JobDetailsSerializer(job, context=sim)

                    recommendation_with_scores.append(job_serializer.data)
                # put the top jobs in the cache if there are any
                CACHE[job_id] = {
                    "data": {
                        "job_details": serializer.data,
                        "recommendations": recommendation_with_scores,
                    },
                    "timestamp": datetime.now(),  # Update timestamp
                }

                return response.Response(
                    {"data": CACHE.get(job_id, {}).get("data")},
                    status=status.HTTP_200_OK,
                )

            elif len(unique_recommendations) == 0:
                return response.Response(
                    {"data": serializer.data}, status=status.HTTP_200_OK
                )

        except Exception as e:
            return response.Response(
                {"data": f"Internal Server Error {e}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def is_cache_expired(self, job_id):
        """
        Method to check if the cache for a job_id is expired.

        Args:
            job_id (int): Job identifier

        Returns:
            Bool: Returns True if the cache is expired otherwise False
        """
        cached_data = CACHE.get(job_id)
        if cached_data:
            timestamp = cached_data.get("timestamp")
            if timestamp:
                return datetime.now() - timestamp > CACHE_EXPIRATION_TIME
        return True


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
            print(e)
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


class JobSummaryView(APIView):
    # IsAdminUser
    permission_classes = [
        AllowAny,
    ]

    def get(self, request, *args, **kwargs):
        filter_by = request.query_params.get("filter-by")

        job_data = Job.objects.values(filter_by).annotate(count=Count(filter_by))
        data = {entry[filter_by]: entry["count"] for entry in job_data}
        return JsonResponse(data)
