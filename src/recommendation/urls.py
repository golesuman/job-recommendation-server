from django.urls import path

from recommendation.views import (
    CompanyDetailsAPI,
    HomePageAPI,
    JobDetailsView,
    JobApplyView,
)

urlpatterns = [
    path("job/<int:job_id>/", JobDetailsView.as_view(), name="job_details"),
    path("job", JobApplyView.as_view(), name="apply_job"),
    path("jobs", HomePageAPI.as_view(), name="list_all_jobs"),
    path(
        "company/<int:company_id>", CompanyDetailsAPI.as_view(), name="company_details"
    ),
]
