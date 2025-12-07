from django.core.management.base import BaseCommand
from utils.api_football.app import APIFootballClient

from football_data.models import Team, League, Team, Player

import pandas as pd

class Command(BaseCommand):

    help = "Seed Player database table with API-Football data"

    # Optional arguement to specify league IDs
    def add_arguments(self, parser):
        parser.add_argument(
            '--league_ids',
            nargs='+',  # allows multiple space-separated values
            help='List of league ids to seed (e.g. 39 135 140)',
        )

        parser.add_argument(
        '--season',
        type=int,
        default=2023, # Set a default value if not provided
        help='The specific year/season to fetch data for (e.g. 2023)',
        )

        parser.add_argument(
        '--max_page',
        type=int,
        default=2, # Set a default value if not provided
        help='The max page to get from paginated API call',
    )

    def handle(self, *args, **options):

        client = APIFootballClient()
        
        options_league_ids = options.get('league_ids', None)
        options_season = options.get('season', None)
        options_max_page = options.get('max_page', None)
        
        league_ids = options_league_ids if options_league_ids is not None else client.league_ids
        season = options_season if options_season is not None else client.default_season
        max_page = options_max_page if options_max_page is not None else client.default_max_page

        self.stdout.write(self.style.NOTICE(f"Seeding players for league IDs: {league_ids}")) 
        
        # Dataframe to store all players
        combine_players_df_api = pd.DataFrame()

        # retrieve players for each league ID
        for league_id in league_ids:
            
            players_data_api = client.request_players(league_id=league_id, season=season, max_pages=max_page)
            players_df_api = client.normalize_players(players_data_api)
            combine_players_df_api = pd.concat([combine_players_df_api, players_df_api], ignore_index=True) # combine all players into one df

        # iterate through dataframe rows and create Player 
        for _, row in combine_players_df_api.iterrows():
            team_id = row['team_id']
            _league_id = row['league_id']

            try:
                team = Team.objects.get(pk=team_id)
                league = League.objects.get(pk=_league_id)
            except Team.DoesNotExist:
                self.stdout.write(self.style.ERROR(f"Player {row['name']} with Team ID {team_id} does not exist. Skipping team..."))
                continue
            except League.DoesNotExist:
                self.stdout.write(self.style.ERROR(f"Player {row['name']} with League ID {_league_id} does not exist. Skipping league..."))
                continue

            # Get or create player instance

            player, created = Player.objects.get_or_create(
                id=row['id'],
                defaults={
                    'name': row['name'],
                    'firstname': row.get('firstname', None),
                    'lastname': row.get('lastname', None),
                    'age': row.get('age', None),
                    'nationality': row.get('nationality', None),
                    'birth_place': row.get('birth_place', None),
                    'birth_country': row.get('birth_country', None),
                    'height': row.get('height', None),
                    'weight': row.get('weight', None),
                    'birth_date': row.get('birth_date', None),
                    'photo': row.get('photo', None),
                    'postion': row.get('position', None),
                    'injured': row.get('injured', False),
                    'team': team,
                    'league': league,
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"{_}. Created Player: {player}"))
            else:
                self.stdout.write(f"{_}.Player already exists: {player}")