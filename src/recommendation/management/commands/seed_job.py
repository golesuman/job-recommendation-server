import csv
import os
import random
import time
from django.contrib.auth.models import User
import re
from recommendation.models import Company, Job
from django.utils import timezone
from backend_api import settings
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Seed the jobs data into the database"

    def extract_and_calculate_average(self):
        # If not in the specified format, return a default value
        return random.choice([50000, 100000, 350000, 45000, 150000])

    def handle(self, *args, **options):
        job_data_path = os.path.join(settings.BASE_DIR, "static/data/jobs.csv")
        with open(job_data_path, "r") as file:
            reader = csv.DictReader(file)
            i = 0
            for row in reader:
                company_ids = [company.id for company in Company.objects.all()]
                company_id = random.choice(company_ids)

                title = row.get("job_name")
                salary = self.extract_and_calculate_average()
                skills = row.get("three_reasons")
                job_exp = "Mid Level"
                category = row.get("taglist")
                industry = "IT"
                role_category = "IT"
                role = ""
                if company_id != " " and company_id is not None:
                    company = Company.objects.filter(id=int(float(company_id))).first()
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
                if i == 200:
                    break

                i += 1
        self.stdout.write(self.style.SUCCESS("Successfully written to db"))
