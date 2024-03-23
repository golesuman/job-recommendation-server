from rest_framework import views, status
from rest_framework.response import Response
from .models import Job
from account.models import Interaction, UserProfile

from .utils.constants import INTERACTION_LIMIT, INTERACTION_THRESHOLD
from .serializers import JobDetailsSerializer
from .algorithms_v2 import TextAnalyzer
from datetime import datetime, timedelta
from django.db.models import Q
from recommendation.services.job_recommendation_service import get_top_jobs

text_analyzer = TextAnalyzer()

CACHE = {}


class RecommendationView(views.APIView):
    def get(self, request, format=None):
        try:
            user_id = request.user.id

            if not user_id:
                return Response({"data": None}, status=status.HTTP_200_OK)

            cached_data = CACHE.get(user_id)
            if cached_data is None or self.is_cache_expired(user_id):
                # take the top 3 interactions that are recently recorded
                interactions = Interaction.objects.filter(user_id=user_id).order_by(
                    "-timestamp"
                )[:INTERACTION_THRESHOLD]
                user_profile = UserProfile.objects.filter(user_id=user_id).first()
                job_listings = Job.objects.all()
                job_listings_dict = {}

                # Filter jobs based on each interaction title and add them to job_listings_dict

                if interactions.count() > INTERACTION_LIMIT:
                    interaction_history = [
                        interaction.job.title + "," + interaction.job.description
                        for interaction in interactions
                    ]
                    for interaction in interaction_history:
                        titles = text_analyzer.preprocess_document(interaction)
                        for title in titles:
                            similar_jobs = job_listings.filter(
                                Q(title__icontains=title)
                                | Q(description__icontains=title)
                            )[:10]
                            for job in similar_jobs:
                                job_listings_dict[str(job.id)] = (
                                    job.title + "," + job.description
                                )

                    top_jobs = get_top_jobs(
                        model="pearson",
                        filtered_jobs=job_listings,
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
                        top_jobs = get_top_jobs(
                            filtered_jobs=job_listings,
                            model="cosine",
                            job_listings_dict=job_listings_dict,
                            data=user_profile.skills,
                        )

                    else:
                        # If neither interactions nor skills are available, return empty response
                        return Response({"data": []}, status=status.HTTP_200_OK)

                if top_jobs:
                    # put the top jobs in the cache if there are any
                    CACHE[user_id] = {
                        "data": top_jobs,
                        "timestamp": datetime.now(),  # Update timestamp
                    }
            # give the response from the cache

            serializer = JobDetailsSerializer(CACHE.get(user_id).get("data"), many=True)
            return Response({"data": serializer.data}, status=status.HTTP_200_OK)

        except Exception as e:
            print(e)
            return Response({"data": "Internal Server Error"})

    def is_cache_expired(self, user_id):
        """
        Method to check if the cache is expired. If cache is older than 10 seconds then it is considered expired

        Args:
            user_id (int): user identifier

        Returns:
            Bool: Returns True if the cache is expired otherwise False
        """
        cached_data = CACHE.get(user_id)
        if cached_data:
            timestamp = cached_data.get("timestamp")
            if timestamp:
                return datetime.now() - timestamp > timedelta(seconds=10)
        return True
