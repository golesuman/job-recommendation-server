import csv
import os
from django.contrib.auth.models import User

from recommendation.models import Company

from django.core.management.base import BaseCommand, CommandError

from backend_api import settings


class Command(BaseCommand):
    help = "Seed company data into db"

    def handle(self, *args, **options):
        job_data_path = os.path.join(settings.BASE_DIR, "static/data/companies.csv")

        with open(job_data_path, "r") as file:
            reader = csv.DictReader(file)
            i = 0
            for row in reader:
                company_id = row.get("company_id")
                name = row.get("company_name")
                description = row.get("overview")

                url = row.get("logo_link")
                user = User.objects.get_or_create(username=name, password="12345678@")

                Company.objects.get_or_create(
                    user_id=user[0].id,
                    id=i,
                    name=name,
                    description=description,
                    website=url,
                )
                i += 1
                if i == 100:
                    break

            self.stdout.write(self.style.SUCCESS("Successfully written to db"))
