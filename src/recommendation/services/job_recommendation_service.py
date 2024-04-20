from recommendation.models import Job
from recommendation.utils.preprocess import remove_special_characters
from ..algorithms_v2 import TextAnalyzer
from ..utils.constants import DEFAULT_THRESHOLD
from django.db.models import Q

analyzer = TextAnalyzer()


def populate_job_ids(interaction, job_listings_dict, model, job_ids):
    """
    Populates the the job_ids by getting it from the algorithm

    Args:
        interaction (list | string)
        job_listings_dict (dict)
        model (string): type of model to use. It can be either cosine or pearson
        job_ids [list]: list of job identifiers
    """
    vector, recommendation = analyzer.get_recommendations(
        interaction, job_listings_dict, model=model
    )
    for doc, similarity in recommendation:
        if similarity > DEFAULT_THRESHOLD:
            job_ids.append((similarity, doc, vector))


def get_top_job_ids(data, job_listings_dict, model):
    """
    Gets the top 5 job ids

    Args:
        data (list | string): data can be jobs that the user has interacted with or user skills
        job_listings_dict (dict): dictionary with job id as key and job title and description as value
        model (string): algorithm to apply. Can be either cosine or pearson

    Returns:
        list: returns the top 5 job ids
    """
    job_ids = []
    if isinstance(data, list):
        for interaction in data:
            populate_job_ids(interaction, job_listings_dict, model, job_ids)
    else:
        populate_job_ids(data, job_listings_dict, model, job_ids)

    result = []
    for sim, value, vector in sorted(job_ids, key=lambda x: x[0], reverse=True)[:5]:
        result.append((sim, value, vector))
    # return [
    #     (sim, value, vector)
    #     for sim, value, vector in sorted(job_ids, key=lambda x: x[0], reverse=True)[:5]
    # ]
    return result


def get_top_jobs(filtered_jobs, data, job_listings_dict, model):
    # returns the top 5 jobs given by algorithm
    jobs = []
    jobs_ids = get_top_job_ids(data, job_listings_dict, model)
    if jobs_ids:
        for sim, id, vector in jobs_ids:
            job = filtered_jobs.filter(id=id).first()
            if job is not None:
                jobs.append((sim, job))
        return jobs
    return [(0, job) for job in filtered_jobs]


def get_jobs_by_skills(document, job_id, job_listings_dict):
    job_skills = analyzer.preprocess_document(document)
    for skill in [skill for skill in job_skills if skill != ""]:
        skill = remove_special_characters(skill)
        # Exclude the current job and filter jobs containing the skill
        jobs = Job.objects.exclude(id=job_id).filter(
            Q(title__icontains=skill) | Q(description__icontains=skill)
        )

        if jobs.count() > 0:
            for job in jobs:
                job_listings_dict[str(job.id)] = job.title + "," + job.description

    return job_listings_dict


def get_recommendations(model, jobs, job_listings_dict, job_details):
    recommendations = []
    document = ""
    job_id = ""
    job_listings = get_jobs_by_skills(document, job_id, job_listings_dict)
    recommendations.extend(
        get_top_jobs(
            filtered_jobs=jobs,
            data=job_details.title,
            # + job_details.skills for more accurate results
            job_listings_dict=job_listings,
            model=model,
        )
    )
    return recommendations
