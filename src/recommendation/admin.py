from django.contrib import admin
from django.http import HttpRequest
from django.template.response import TemplateResponse

from recommendation.models import Company, Job, JobSummary

# Register your models here.
admin.site.register(Company)
admin.site.register(Job)


@admin.register(JobSummary)
class JobSummaryAdmin(admin.ModelAdmin):
    change_list_template = "admin/job_changelist.html"
    date_hierarchy = "posted_at"

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(
            request,
            extra_context=extra_context,
        )
        # try:
        #     qs = response.context_data["cl"].queryset
        # except (AttributeError, KeyError):
        #     return response
        return response
