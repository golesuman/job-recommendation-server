from django.urls import path

from recommendation.views import JobDetailsView, JobApplyView

urlpatterns = [
    path("job/<int:job_id>/", JobDetailsView.as_view(), name="job_details"),
    path("job", JobApplyView.as_view(), name="apply_job"),
]
