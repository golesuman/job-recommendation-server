from django.urls import path

from recommendation.views import JobDetailsView

urlpatterns = [path("job/<int:job_id>/", JobDetailsView.as_view(), name="job_details")]
