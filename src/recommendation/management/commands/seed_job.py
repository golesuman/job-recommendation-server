import csv
import random
import time
from django.contrib.auth.models import User

from recommendation.models import Company, Job
from django.utils import timezone

from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Closes the specified poll for voting"

    # def add_arguments(self, parser):
    #     parser.add_argument("poll_ids", nargs="+", type=int)

    def handle(self, *args, **options):
        csv_file_path = "/home/suman/Downloads/College-projects/job-recommendation-server/data/job_data_naukri.csv"
        with open(csv_file_path, "r") as file:
            reader = csv.DictReader(file)
            i = 0
            for row in reader:
                job_id = row.get("job_id")
                company_ids = [company.id for company in Company.objects.all()]
                company_id = random.choice(company_ids)

                title = row.get("Job Title")
                salary = row.get("Job Salary")
                description = row.get("description")
                skills = row.get("Key Skills")
                job_exp = row.get("Job Experience Required")
                category = row.get("Functional Area").split(",")[0]
                industry = row.get("Industry")
                role_category = row.get("Role Category")
                location = row.get("Location")
                role = row.get("Role")
                if company_id != " " and company_id is not None:
                    company = Company.objects.filter(id=int(float(company_id))).first()
                    print(company)
                    job = Job.objects.create(
                        title=title,
                        company=company,
                        description=role_category,
                        category=category,
                        job_type=category,
                        salary=salary,
                        is_active=True,
                        role=role,
                        skills=skills,
                        experience=job_exp,
                        industry=industry,
                    )
                    # print(company)
                if i == 200:
                    break

                i += 1
            self.stdout.write(self.style.SUCCESS("Successfully written to db"))
