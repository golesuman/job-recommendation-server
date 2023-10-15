from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework import response
from recommendation.services.job_interaction_service import (
    create_interaction,
    get_job_details,
)

from recommendation.serializers import JobDetailsSerializer


# Create your views here.


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
        serializer = JobDetailsSerializer(job_details)
        return response.Response(serializer.data)
        # pass
