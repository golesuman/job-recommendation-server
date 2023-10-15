from account.models import Interaction

from recommendation.models import Job


def is_interaction_present(user_id, interaction_type, job_id):
    return Interaction.objects.filter(
        user_id=user_id, interaction_type=interaction_type, job_id=job_id
    ).exists()


def create_interaction(user_id, interaction_type, job_id):
    if not is_interaction_present(user_id, interaction_type, job_id):
        interaction = Interaction.objects.create(
            user_id=user_id, interaction_type=interaction_type, job_id=job_id
        )

        return interaction


def get_job_details(job_id):
    return Job.objects.filter(id=job_id).first()
