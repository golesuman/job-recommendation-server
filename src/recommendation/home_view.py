from rest_framework import views, status
from rest_framework.response import Response
from .models import Job
from account.models import Interaction, UserProfile

from .serializers import JobDetailsSerializer, JobPostSerializer
from .algorithms_v2 import get_recommendations
from django.core.cache import cache
from datetime import datetime, timedelta
from django.db.models import Q

INTERACTION_LIMIT = 3
THRESHOLD = 0.1


CACHE = {}


class RecommendationView(views.APIView):
    def get(self, request, format=None):
        try:
            user_id = request.user.id

            if not user_id:
                return Response({"data": None}, status=status.HTTP_200_OK)

            cached_data = CACHE.get(user_id)
            if cached_data is None or self.is_cache_expired(user_id):
                interactions = Interaction.objects.filter(user_id=user_id)
                user_profile = UserProfile.objects.filter(user_id=user_id).first()
                job_listings = Job.objects.all()
                job_listings_dict = {}

                # Filter jobs based on each interaction title and add them to job_listings_dict

                if interactions.count() > INTERACTION_LIMIT:
                    interaction_history = [
                        interaction.job.title + "," + interaction.job.description
                        for interaction in interactions
                    ]

                    for interaction in interactions:
                        similar_jobs = job_listings.filter(
                            Q(title__icontains=interaction.job.title)
                        )
                        for job in similar_jobs:
                            job_listings_dict[str(job.id)] = (
                                job.title + "," + job.description
                            )

                    job_ids = self.get_results(
                        model="cosine",
                        job_listings_dict=job_listings_dict,
                        data=interaction_history,
                    )

                # If no interactions found or job_listings_dict is empty, filter based on user skills
                if not job_listings_dict:
                    if user_profile.skills:
                        user_skills = user_profile.skills.split(",")
                        for skill in user_skills:
                            similar_jobs = job_listings.filter(
                                Q(title__icontains=skill)
                                | Q(description__icontains=skill)
                            )
                            for job in similar_jobs:
                                job_listings_dict[str(job.id)] = (
                                    job.title + "," + job.description
                                )
                        job_ids = self.get_results(
                            model="cosine",
                            job_listings_dict=job_listings_dict,
                            data=user_profile.skills,
                        )

                    else:
                        # If neither interactions nor skills are available, return empty response
                        return Response({"data": []}, status=status.HTTP_200_OK)

                job_recommendations = job_listings.filter(id__in=set(list(job_ids)))
                if job_recommendations:
                    CACHE[user_id] = {
                        "data": job_recommendations,
                        "timestamp": datetime.now(),  # Update timestamp
                    }

            serializer = JobDetailsSerializer(CACHE.get(user_id).get("data"), many=True)
            return Response({"data": serializer.data}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"data": "Internal Server Error"})

    def is_cache_expired(self, user_id):
        cached_data = CACHE.get(user_id)
        if cached_data:
            timestamp = cached_data.get("timestamp")
            if timestamp:
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
                    interaction,
                    job_listings_dict=job_listings_dict,
                    model=model,
                    job_ids=job_ids,
                )
        else:
            self.recommendation_service(
                interaction=data,
                job_listings_dict=job_listings_dict,
                model=model,
                job_ids=job_ids,
            )

        return [value for _, value in sorted(job_ids, key=lambda x: x[0])[:5]]
