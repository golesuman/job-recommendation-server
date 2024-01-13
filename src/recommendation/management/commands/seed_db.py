import csv
import os
from django.contrib.auth.models import User

from recommendation.models import Company

from django.core.management.base import BaseCommand, CommandError

from backend_api import settings


class Command(BaseCommand):
    help = "Closes the specified poll for voting"

    # def add_arguments(self, parser):
    #     parser.add_argument("poll_ids", nargs="+", type=int)

    def handle(self, *args, **options):
        job_data_path = os.path.join(settings.BASE_DIR, "static/data/company_data.csv")

        with open(job_data_path, "r") as file:
            reader = csv.DictReader(file)
            i = 0
            for row in reader:
                company_id = row.get("company_id")
                name = row.get("name")
                description = row.get("description")
                # si= row.get("company_size")
                # row.get("state")
                # row.get("country")
                # row.get("ciy")
                address = row.get("address")
                url = row.get("url")
                user = User.objects.get_or_create(username=name, password="12345678@")

                company = Company.objects.get_or_create(
                    user_id=user[0].id,
                    id=company_id,
                    name=name,
                    description=description,
                    website=url,
                )
                i += 1
                if i == 100:
                    break

            self.stdout.write(self.style.SUCCESS("Successfully written to db"))
