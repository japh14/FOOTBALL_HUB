from pathlib import Path
import json
import pandas as pd

from backend.utils.api_football.app import APIFootballClient


dir_path = Path(__file__).parent

data_path = dir_path.parent / 'data'

countries_file = data_path / 'countries.json'
leagues_file = data_path / 'leagues.json'


# File Seeding

# with open(countries_file, 'r') as f:
#     countries_data = json.load(f)

# countries_data_list = countries_data.get('response', [])
# countries_df = pd.json_normalize(countries_data_list)


# with open(leagues_file, 'r') as f:
#     leagues_data = json.load(f)

# leagues_data_list = leagues_data.get('response', [])
# response_leagues = []
# for item in leagues_data_list:
#     league_info = item.get('league', {})
#     country_info = item.get('country', {})
#     combined_info = {**league_info, **country_info}
#     response_leagues.append(combined_info)

# leagues_df = pd.json_normalize(response_leagues)
# print(f'{leagues_df.head()}')


# API Seeding

url = 'https://v3.football.api-sports.io/'

if __name__ == '__main__':
    client = APIFootballClient()
    
    # countries_data_api = client.request(endpoint='countries')
    # countries_df_api = client.normalize_countries(countries_data_api)
    # print(f'Countries from API:\n{countries_df_api.head()}')
    
    # leagues_data_api = client.request(endpoint='leagues')
    # leagues_df_api = client.normalize_leagues(leagues_data_api)
    # print(f'Leagues from API:\n{leagues_df_api.head()}')

    league_ids = [39,71,140,218,61]

    # teams_data_api = client.request_teams(league_ids=league_ids, season=2023)
    # teams_df_api = client.normalize_teams(teams_data_api)
    # teams_df_api.to_csv(dir_path / 'teams_api.csv', index=False)
    # print(f'Teams from API:\n{teams_df_api.head()}')