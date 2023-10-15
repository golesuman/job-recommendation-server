from account.models import Interaction

from recommendation.models import Job


def is_interaction_present(user_id, interaction_type, job_id):
    return Interaction.objects.filter(
        user_id=user_id, interaction_type=interaction_type, job_id=job_id
    ).exists()


def create_interaction(user_id, interaction_type, job_id):
    if not is_interaction_present(user_id, interaction_type, job_id):
        try:
            interaction = Interaction.objects.create(
                user_id=user_id, interaction_type=interaction_type, job_id=job_id
            )
            return interaction
        except Exception as e:
            print(e)
            return


def get_job_details(job_id):
    try:
        job = Job.objects.filter(id=job_id).first()
        return job
    except Job.DoesNotExist as e:
        print(e)
        return
