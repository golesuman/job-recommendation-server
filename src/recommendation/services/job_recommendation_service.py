from ..algorithms_v2 import TextAnalyzer
from ..utils.constants import DEFAULT_THRESHOLD

analyzer = TextAnalyzer()


def populate_job_ids(interaction, job_listings_dict, model, job_ids):
    recommendation = analyzer.get_recommendations(
        interaction, job_listings_dict, model=model
    )
    for doc, similarity in recommendation:
        if similarity > DEFAULT_THRESHOLD:
            job_ids.append((similarity, doc))


def get_top_job_ids(data, job_listings_dict, model):
    job_ids = []
    if isinstance(data, list):
        for interaction in data:
            populate_job_ids(interaction, job_listings_dict, model, job_ids)
    else:
        populate_job_ids(data, job_listings_dict, model, job_ids)

    return [value for _, value in sorted(job_ids, key=lambda x: x[0], reverse=True)[:5]]


def get_top_jobs(filtered_jobs, data, job_listings_dict, model):
    jobs_ids = get_top_job_ids(data, job_listings_dict, model)
    if jobs_ids:
        jobs = filtered_jobs.filter(id__in=jobs_ids)
        return jobs
    return None
