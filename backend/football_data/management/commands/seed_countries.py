from django.core.management.base import BaseCommand
from utils.api_football.app import APIFootballClient
from football_data.models import Country


class Command(BaseCommand):
    help = "Seed Country database table with API-Football data"

    def handle(self, *args, **options):
        client = APIFootballClient()
        countries_data = client.request(endpoint='countries')
        countries_df = client.normalize_countries(countries_data)

        for _, row in countries_df.iterrows():
            country, created = Country.objects.get_or_create(
                code=row['code'],
                defaults={
                    'name': row['name'],
                    'flag': row.get('flag', None)
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"Created country: {country}"))
            else:
                self.stdout.write(f"Country already exists: {country}")