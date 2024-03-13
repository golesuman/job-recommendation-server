from rest_framework import views, status
from rest_framework.response import Response
from .models import Job
from account.models import Interaction, UserProfile

from .serializers import JobDetailsSerializer, JobPostSerializer
from .algorithms_v2 import get_recommendations


INTERACTION_LIMIT = 10


class RecommendationView(views.APIView):
    def get(self, request, format=None):
        user_id = request.user.id

        if not user_id:
            return Response({"data": None}, status=status.HTTP_200_OK)

        interactions = Interaction.objects.filter(user_id=user_id)
        user_profile = UserProfile.objects.filter(user_id=user_id).first()

        job_listings = Job.objects.all()

        job_listings_dict = {
            str(job.id): f"{job.title, job.description}" for job in job_listings
        }

        if interactions.count() > INTERACTION_LIMIT:
            user_search_history = [
                interaction.job.title for interaction in interactions
            ]
            job_ids = self.get_results(
                model="cosine",
                job_listings_dict=job_listings_dict,
                data=user_search_history,
            )

        else:
            skills = user_profile.skills.split(",") if user_profile.skills else []
            bio = user_profile.bio if user_profile.bio else []
            profile_ = bio + skills
            job_ids = self.get_results(
                model="cosine", job_listings_dict=job_listings_dict, data=profile_
            )

        jobs = job_listings.filter(id__in=list(set(job_ids)))
        serializer = JobDetailsSerializer(jobs, many=True)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)

    def get_results(self, model, data, job_listings_dict):
        job_ids = []
        for interaction in data:
            recommendation = get_recommendations(
                interaction, job_listings_dict, model=model
            )
            for doc, similarity in recommendation:
                if similarity > 0.5:
                    job_ids.append(doc)
        return job_ids
