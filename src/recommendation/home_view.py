from rest_framework import views, status
from rest_framework.response import Response
from .models import Job
from account.models import Interaction, UserProfile

from .serializers import JobDetailsSerializer, JobPostSerializer
from .algorithms_v2 import get_recommendations
from django.core.cache import cache

INTERACTION_LIMIT = 10
THRESHOLD = 0.3


class RecommendationView(views.APIView):
    def get(self, request, format=None):
        user_id = request.user.id

        if not user_id:
            return Response({"data": None}, status=status.HTTP_200_OK)

        interactions = Interaction.objects.filter(user_id=user_id)
        user_profile = UserProfile.objects.filter(user_id=user_id).first()

        job_listings_dict = cache.get("job_listings_dict")

        if job_listings_dict is None:
            job_listings = Job.objects.all()
            job_listings_dict = {
                str(job.id): job.title + "," + job.description for job in job_listings
            }
            cache.set("job_listings_dict", job_listings_dict)

        if interactions.count() > INTERACTION_LIMIT:
            interaction_history = [
                interaction.job.title + "," + interaction.job.description
                for interaction in interactions
            ]
            job_ids = self.get_results(
                model="cosine",
                job_listings_dict=job_listings_dict,
                data=interaction_history,
            )

        else:
            if user_profile.skills:
                skills = user_profile.skills
                job_ids = self.get_results(
                    model="cosine", job_listings_dict=job_listings_dict, data=skills
                )
            else:
                job_ids = []

        jobs = Job.objects.filter(id__in=list(set(job_ids)))
        serializer = JobDetailsSerializer(jobs, many=True)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)

    def recommendation_service(self, interaction, job_listings_dict, model, job_ids):
        recommendation = get_recommendations(
            interaction, job_listings_dict, model=model
        )
        for doc, similarity in recommendation:
            if similarity > THRESHOLD:
                job_ids.append(doc)

    def get_results(self, model, data, job_listings_dict):
        job_ids = []
        if isinstance(data, list):
            for interaction in data:
                self.recommendation_service(
                    interaction, job_listings_dict, model=model, job_ids=job_ids
                )
        else:
            self.recommendation_service(
                data, job_listings_dict, model=model, job_ids=job_ids
            )
        return job_ids
