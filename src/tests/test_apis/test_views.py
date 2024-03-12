import pytest
from rest_framework import status
from rest_framework.test import APIRequestFactory, force_authenticate
from django.urls import reverse
from ..factories import UserProfileFactory, InteractionFactory, JobFactory
from recommendation.home_view import RecommendationView


@pytest.mark.django_db
class TestRecommendationView:
    def test_recommendation_view_with_interactions(self):
        factory = APIRequestFactory()
        view = RecommendationView.as_view()

        user_profile = UserProfileFactory()
        job1 = JobFactory()
        job2 = JobFactory()
        interaction1 = InteractionFactory(
            user=user_profile.user, job=job1, interaction_type="click"
        )
        interaction2 = InteractionFactory(
            user=user_profile.user, job=job2, interaction_type="click"
        )
        request = factory.get(reverse("home_page"))
        force_authenticate(request, user=user_profile.user)
        response = view(request)

        assert response.status_code == status.HTTP_200_OK

    def test_recommendation_view_no_interactions(self):
        factory = APIRequestFactory()
        view = RecommendationView.as_view()
        user_profile = UserProfileFactory()

        request = factory.get(reverse("home_page"))
        force_authenticate(request, user=user_profile.user)
        response = view(request)

        assert response.status_code == status.HTTP_200_OK

    def test_recommendation_view_no_user(self):
        factory = APIRequestFactory()
        view = RecommendationView.as_view()

        request = factory.get(reverse("home_page"))
        response = view(request)

        assert response.status_code == 401
