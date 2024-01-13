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
    help = "Closes the specified poll for voting"

    def extract_and_calculate_average(self, salary_string):
        if re.search("[a-zA-Z]", salary_string):
            return random.choice([50000, 100000, 350000, 45000, 150000])

        # Use regular expression to extract numerical values
        matches = re.findall(r"\d{1,3},\d{1,3}", salary_string)

        if len(matches) == 2:
            salary_range = [int(match.replace(",", "")) for match in matches]
            average_salary = sum(salary_range) / 2
            return int(average_salary)
        else:
            # If not in the specified format, return a default value
            return random.choice([50000, 100000, 350000, 45000, 150000])

    def handle(self, *args, **options):
        ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
        print(settings.BASE_DIR)
        job_data_path = os.path.join(
            settings.BASE_DIR, "static/data/job_data_naukri.csv"
        )
        with open(job_data_path, "r") as file:
            reader = csv.DictReader(file)
            i = 0
            for row in reader:
                job_id = row.get("job_id")
                company_ids = [company.id for company in Company.objects.all()]
                company_id = random.choice(company_ids)

                title = row.get("Job Title")
                salary = self.extract_and_calculate_average(row.get("Job Salary"))
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
