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

from recommendation.serializers import JobDetailsSerializer
from recommendation.models import Job


class JobDetailsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user_id = request.user.id

        job_id = self.kwargs.get("job_id")
        interaction_type = "click"
        create_interaction(
            user_id=user_id, interaction_type=interaction_type, job_id=job_id
        )

        job_details = get_job_details(job_id)
        if job_details:
            serializer = JobDetailsSerializer(job_details)
            return response.Response({"data": serializer.data})
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
        jobs = get_jobs_by_interaction(user_id=request.user.id)
        serializer = JobDetailsSerializer(instance=jobs, many=True)
        return response.Response({"data": serializer.data}, status=status.HTTP_200_OK)
