from datetime import datetime, timedelta
from rest_framework import views, status
from rest_framework.response import Response
from .models import Job
from account.models import Interaction, UserProfile

from .serializers import JobDetailsSerializer, JobPostSerializer
from .algorithms_v2 import get_recommendations
from django.core.cache import cache

INTERACTION_LIMIT = 4
THRESHOLD = 0.3


CACHE = {}


class JobDetailsView(views.APIView):
    def get(self, request, format=None):
        user_id = request.user.id

        if not user_id:
            return Response({"data": None}, status=status.HTTP_200_OK)

        cached_data = CACHE.get(user_id)
        if cached_data is None or self.is_cache_expired(user_id):
            interactions = Interaction.objects.filter(user_id=user_id)
            user_profile = UserProfile.objects.filter(user_id=user_id).first()
            job_listings = Job.objects.all()
            job_listings_dict = {
                str(job.id): job.title + "," + job.description for job in job_listings
            }

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

            jobs = job_listings.filter(id__in=list(set(job_ids)))
            CACHE[user_id] = {
                "data": jobs,
                "timestamp": datetime.now(),  # Update timestamp
            }

        serializer = JobDetailsSerializer(CACHE.get(user_id)["data"], many=True)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)

    def is_cache_expired(self, user_id):
        cached_data = CACHE.get(user_id)
        if cached_data:
            timestamp = cached_data.get("timestamp")
            if timestamp:
                # Check if the timestamp is older than 1 hour
                return datetime.now() - timestamp > timedelta(seconds=10)
        return True

    def recommendation_service(self, interaction, job_listings_dict, model, job_ids):
        recommendation = get_recommendations(
            interaction, job_listings_dict, model=model
        )
        for doc, similarity in recommendation:
            if similarity > THRESHOLD:
                job_ids.append((similarity, doc))

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
        job_lists = sorted(job_ids, key=lambda x: x[0])[:5]
        return [value for _, value in job_lists]
