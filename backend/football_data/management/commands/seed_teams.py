from django.core.management.base import BaseCommand
from utils.api_football.app import APIFootballClient

from football_data.models import Team, League, Country

import pandas as pd


class Command(BaseCommand):    

    help = "Seed Team database table with API-Football data"

    # Optional argument to specify league IDs
    def add_arguments(self, parser):
        parser.add_argument(
        '--league_ids',
        nargs='+',  # allows multiple space-separated values
        help='List of league ids to seed (e.g. 39 135 140)',
    )

    def handle(self, *args, **options):
        
        client = APIFootballClient()

        options_league_ids = options.get('league_ids', None)
        league_ids = options_league_ids if options_league_ids is not None else client.league_ids

        self.stdout.write(self.style.NOTICE(f"Seeding teams for league IDs: {league_ids}"))

        teams_data_api = client.request_teams(league_ids=league_ids) # uses default league_ids and season
        teams_df = client.normalize_teams(teams_data_api)

        for _, row in teams_df.iterrows():
            country_name = row['country']
            _league_id = row['league_id']

            # Fetch related Country and League instances
            country = Country.objects.filter(name=country_name).first()
            if not country:
                self.stdout.write(self.style.ERROR(f"Country '{country_name}' does not exist. Skipping team {row['name']}."))
                continue

            try:
                league = League.objects.get(id=_league_id)
            except League.DoesNotExist:
                self.stdout.write(self.style.ERROR(f"League with ID {_league_id} does not exist. Skipping team {row['team.name']}."))
                continue
            
            # TODO: Add Try Except for get_or_create
            team, created = Team.objects.get_or_create(
                id=row['id'],                
                defaults={
                    'country': country,
                    'league': league,
                    'name': row['name'],
                    'code': row.get('code', None),
                    'founded': row.get('founded', None),
                    'national': row.get('national', False),
                    'logo': row.get('logo', None),
                    'venue_id': row.get('venue.id', None),
                    'venue_name': row.get('venue_name', None),
                    'venue_address': row.get('venue_address', None),
                    'venue_city': row.get('venue_city', None),
                    'venue_capacity': row.get('venue_capacity', None),
                    'venue_surface': row.get('venue_surface', None),
                    'venue_image': row.get('venue_image', None),
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"Created team: {team}"))
            else:
                self.stdout.write(f"Team already exists: {team}")