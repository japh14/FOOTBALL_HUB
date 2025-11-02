from django.core.management.base import BaseCommand
from utils.api_football.app import APIFootballClient
from football_data.models import League, Country

class Command(BaseCommand):
    help = "Seed League database table with API-Football data"

    def handle(self, *args, **options):
        client = APIFootballClient()
        leagues_data = client.request(endpoint='leagues')
        leagues_df = client.normalize_leagues(leagues_data)

        for _, row in leagues_df.iterrows():
            
            country_code = row['country_code']
            if country_code is None:
                country = Country.objects.filter(name=row['country_name']).first()
            else:
                country, _ = Country.objects.get_or_create(
                    code=country_code,
                    defaults={
                        'name': row['country_name'],
                        'flag': row.get('country_flag', None)
                        }
                )

            league, created = League.objects.get_or_create(
                id=row['id'],
                defaults={
                    'name': row['name'],
                    'type': row['type'],
                    'logo': row.get('logo', None),
                    'country': country
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"Created league: {league}"))
            else:
                self.stdout.write(f"League already exists: {league}")