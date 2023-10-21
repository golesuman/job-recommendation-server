from ..models import Interaction, UserProfile


def get_user_profile(user_id):
    profile_details = UserProfile.objects.filter(
        user_id=user_id, is_active=True
    ).first()
    return profile_details


def get_latest_user_interactions(user_id):
    interactions = Interaction.objects.filter(user_id=user_id).order_by("-timestamp")
    return interactions
