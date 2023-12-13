import csv
from django.contrib.auth.models import User

from recommendation.models import Job

from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Closes the specified poll for voting"

    # def add_arguments(self, parser):
    #     parser.add_argument("poll_ids", nargs="+", type=int)

    def handle(self, *args, **options):
        csv_file_path = "/home/suman/Downloads/College-projects/job-recommendation-server/data/job_postings.csv"
        with open(csv_file_path, "r") as file:
            reader = csv.DictReader(file)
            i = 0
            for row in reader:
                print(row.get("location"))
                print(row.get("title"))
                print(row.get("description"))
                # print(row.get("posted"))
                job_id = row.get("job_id")
                company_id = row.get("company_id")
                title = row.get("title")
                description = row.get("description")
                med_salary = row.get("med_salary")
                min_salary = row.get("min_salary")
                expiry_date = row.get("expiry")
                skills_desc = row.get("skills_desc")
                work_type = row.get("work_type")
                location = row.get("location")
                category = row.get("formatted_experience_level")

                # si= row.get("company_size")
                # row.get("state")
                # row.get("country")
                # row.get("ciy")
                address = row.get("address")
                url = row.get("url")
                Job.objects.get_or_create(
                    id=job_id,
                    company_id=company_id,
                    title=title,
                    description=description,
                    location=location,
                    job_type="Full-Time",
                    category="IT",
                    salary=med_salary,
                    slug=f"{title}-{i}{i**2/3}",
                    expires_at=expiry_date,
                )

            i += 1
            self.stdout.write(self.style.SUCCESS("Successfully written to db"))


# from recommendation.models import Company, Job
# from account.models import User, UserProfile


# def create_company(data) -> Company:
#     return company


# def create_job(data):
#     user = User.objects.create()
#     company = Company.objects.create(
#         user=user,
#         name=data.get("name"),
#         description=data.get("description"),
#         website=data.get("website"),
#         logo=data.get("logo"),
#     )
#     job = Job.objects.create(
#         company=company,
#         title=data.get("name"),
#         description=data.get("description"),
#         location=data.get("location"),
#         job_type=data.get("type"),
#         category=data.get("category"),
#         salary=data.get("salary"),
#         posted_at=data.get("posted_at"),
#         expires_at=data.get("deadline"),
#         is_active=True,
#     )
#     return job


# def main():

#     pass


# if __name__ == "__main__":
# with open("train.csv", "r+") as fp:
#     data = fp.readlines()

# for line in data:
#     data = line.split(",")
#     # company_data = {
#     #     "name": data[0],
#     #     "description": data[1],

# for row in reader:
#     # print(row)
#     print(row.get("company_id"))
#     print(row.get("location"))
#     print(row.get("title"))
#     print(row.get("description"))
#     print(row.get("max_salary"))
#     print(row.get("min_salary"))
#     print(row.get("expiry"))
#     print(row.get("skills_desc"))
#     print(row.get("work_type"))  # job_type
#     print(row.get("category"))
#     # print(row.get("posted"))
#     print(f"Row-{i}")


# """'
# for company

# row.get("company_id")
# row.get("name")
# row.get("description")
# row.get("company_size")
# row.get("state")
# row.get("country")
# row.get("ciy")
# row.get("address")
# row.get("url)
# """
