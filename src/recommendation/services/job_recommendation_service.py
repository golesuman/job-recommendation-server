from ..algorithms_v2 import TextAnalyzer
from ..utils.constants import DEFAULT_THRESHOLD

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
    recommendation = analyzer.get_recommendations(
        interaction, job_listings_dict, model=model
    )
    for doc, similarity in recommendation:
        if similarity > DEFAULT_THRESHOLD:
            job_ids.append((similarity, doc))


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

    return [value for _, value in sorted(job_ids, key=lambda x: x[0], reverse=True)[:5]]


def get_top_jobs(filtered_jobs, data, job_listings_dict, model):
    # returns the top 5 jobs given by algorithm
    jobs_ids = get_top_job_ids(data, job_listings_dict, model)
    if jobs_ids:
        jobs = filtered_jobs.filter(id__in=jobs_ids)
        return jobs
    return filtered_jobs
