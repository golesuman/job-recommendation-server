from django.contrib import admin

from .models import UserProfile, Interaction, InteractionSummary
from django.db.models import Count, Sum

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Interaction)


@admin.register(InteractionSummary)
class InteractionSummaryAdmin(admin.ModelAdmin):
    change_list_template = "admin/change_list.html"
    date_hierarchy = "timestamp"

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(
            request,
            extra_context=extra_context,
        )
        try:
            qs = response.context_data["cl"].queryset
        except (AttributeError, KeyError):
            return response

        metrics = {
            "total": Count("id"),
            # "total_sales": Sum("price"),
        }
        response.context_data["summary"] = list(
            qs.values("interaction_type").annotate(**metrics).order_by("-timestamp")
        )
        # tp
        return response
