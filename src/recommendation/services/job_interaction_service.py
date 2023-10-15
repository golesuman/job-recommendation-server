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


def is_interaction_present_for_user(user_id):
    return Interaction.objects.filter(user_id=user_id).exists()


def get_jobs_by_interaction(user_id):
    if user_id is not None:
        if is_interaction_present_for_user(user_id=user_id):
            interactions = Interaction.objects.filter(user_id=user_id)
            job_ids = set([interaction.job_id for interaction in interactions])
        jobs = Job.objects.filter(id__in=job_ids)
    else:
        jobs = Job.objects.all()

    return jobs
