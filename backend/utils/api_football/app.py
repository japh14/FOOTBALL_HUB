import requests
import os
import pandas as pd
import numpy as np

from typing import Any
from dotenv import load_dotenv
from datetime import datetime


class APIFootballClient:
    """_summary_
    This class handles requests to the API-Football service. 
    It retrieves and normalizes data for countries, leagues, teams, and players.


    Returns:
        _type_: _description_
    """
    load_dotenv()

    base_url = "https://v3.football.api-sports.io/"
    
    league_ids = os.getenv("LEAGUE_IDS", "39").split(",")    
    league_ids = list(map(lambda x: int(x.strip()), league_ids)) # convert to list of ints

    default_season = int(os.getenv("DEFAULT_SEASON", "2023"))
    default_max_page = int(os.getenv("DEFAULT_MAX_PAGE", 5))

    __api_key = os.getenv("API_KEY") 
    __headers = {
            "x-apisports-key": __api_key,
            "x-rapidapi-host": "v3.football.api-sports.io"
    }

    def __init__(self):
        """Initialize the APIFootballClient"""
        pass

    def __str__(self):
        """String representation of the APIFootballClient"""
        return f"APIFootballClient(url={self.base_url})\n Default League IDs: {self.league_ids}, Default Season: {self.default_season}"
    
    def __repr__(self):
        """Official string representation of the APIFootballClient"""
        pass

    @classmethod
    def request(cls, endpoint: str='status', params: Any=None)-> dict[str, Any]:
        """_summary_

        Args:
            endpoint (str, optional): _description_. Defaults to 'status'.
            params (Any, optional): _description_. Defaults to None.

        Returns:
            dict[str,Any]: _description_
        """
        url = f"{cls.base_url}{endpoint}"
        try:
            response = requests.get(url, headers=cls.__headers, params=params)
            if response.status_code != 200:
                print(f"Error: Received status code {response.status_code} for URL: {url}")
                return {}
        except requests.RequestException as e:
            print(f"Error during request to {url}: {e}")
            return {}
        
        return response.json()
    
    def request_country(self, country_name: [str,Any]=None) -> dict[str, Any]: # type: ignore
        endpoint = "countries"
        params = {"name": country_name}
        return self.request(endpoint, params=params)
    
    def normalize_countries(self, countries_data: dict[str, Any]) -> pd.DataFrame:
        countries_data_list = countries_data.get('response', [])
        countries_df = pd.json_normalize(countries_data_list)
        # TODO: Clean up data frame columns if necessary
        countries_df.replace({pd.NA: None}, inplace=True) # replace pandas NA with None
        countries_df.replace({np.nan: None}, inplace=True) # replace numpy nan with None
        return countries_df    
    
    def request_leagues(self, league_id: [int,Any]=None) -> dict[str, Any]: # type: ignore
        endpoint = "leagues"
        params = {}
        if league_id is not None:
            params["id"] = league_id
        return self.request(endpoint, params=params)
    
    def normalize_leagues(self, leagues_data: dict[str, Any]) -> pd.DataFrame:
        leagues_data_list = leagues_data.get('response', []) # get response list to normalize specific data instead of whole dict
        response_leagues = []
        for item in leagues_data_list:
            league_info = item.get('league', {})
            country_info = item.get('country', {})

            # revise country_info keys to avoid conflict
            country_info['country_name'] = country_info.pop('name', None)
            country_info['country_code'] = country_info.pop('code', None)
            country_info['country_flag'] = country_info.pop('flag', None)

            combined_info = {**league_info, **country_info}
            response_leagues.append(combined_info)
        
        leagues_df = pd.json_normalize(response_leagues)
        # TODO: Clean up data frame columns if necessary
        leagues_df.replace({pd.NA: None}, inplace=True) # replace pandas NA with None
        leagues_df.replace({np.nan: None}, inplace=True) # replace numpy nan with None
        return leagues_df
    
    def request_team(self, league_id: int, season: int=default_season) -> dict[str, Any]:
        endpoint = "teams"
        params = {
            "league": league_id,
            "season": season
        }
        return self.request(endpoint, params=params)
    
    def request_teams(self, league_ids: list[int]=league_ids, season: int=default_season) -> dict[str, Any]:
        all_teams = {}
        for league_id in league_ids:
            teams_data = self.request_team(league_id, season)
            all_teams[league_id] = teams_data
        return all_teams
    
    def normalize_teams(self, teams_data: dict[int, dict[str, Any]]) -> pd.DataFrame:
        all_teams_list = []
        for league_id, data in teams_data.items():
            teams_list = data.get('response', [])
            for team in teams_list:
                team_info = team.get('team', {})
                venue_info = team.get('venue', {})

                # revise venue_info keys to avoid conflict
                venue_info['venue_id'] = venue_info.pop('id', None)
                venue_info['venue_name'] = venue_info.pop('name', None)
                venue_info['venue_city'] = venue_info.pop('city', None)
                venue_info['venue_capacity'] = venue_info.pop('capacity', None)
                venue_info['venue_surface'] = venue_info.pop('surface', None)
                venue_info['venue_address'] = venue_info.pop('address', None)
                venue_info['venue_image'] = venue_info.pop('image', None)

                combined_info = {**team_info, **venue_info, "league_id": league_id}
                all_teams_list.append(combined_info)
        
        teams_df = pd.json_normalize(all_teams_list)
        # TODO: Clean up data frame columns if necessary
        teams_df.replace({pd.NA: None}, inplace=True) # replace pandas NA with None
        teams_df.replace({np.nan: None}, inplace=True) # replace numpy nan with None
        return teams_df
    

    def request_player(self, league_id: int, page: int=1, season: int=default_season) -> dict[str, Any]:
        endpoint = "players"
        params = {
            "league": league_id,
            "season": season,
            "page": page
        }
        return self.request(endpoint, params=params)
    
    def request_players(self, league_id: int, max_pages:int =3, season: int=default_season,) -> dict[int, dict[str, Any]]:
        all_players = {}

        first_page_data = self.request_player(league_id, page=1, season=season)
        total_pages = min(first_page_data.get('paging', {}).get('total', 1), max_pages) # Limit to max_pages for testing (and API call limits)

        print(f'total pages for league {league_id}: {total_pages}')
        
        all_players[f'{league_id}_{1}'] = first_page_data
        for page in range(2, total_pages + 1):
            players_data = self.request_player(league_id, page=page, season=season)
            all_players[f'{league_id}_{page}'] = players_data
        return all_players
    
    def normalize_players(self, players_data: dict[int, dict[str, Any]]) -> pd.DataFrame:
        all_players_list = []
        for _, data in players_data.items():
            players_list = data.get('response', [])
            for player in players_list:
                player_info = player.get('player', {})

                # revise player height & weight  from string to float (for example from 174 cm to 174.00
                # or 60 kg to 60.00)        
                # revise player_info keys to avoid conflict
                try:
                    player_info['height'] = float(player_info.get('height','').split(' ')[0])
                    player_info['weight'] = float(player_info.get('weight','').split(' ')[0])

                    birth_date = player_info.get('birth', {}).get('date', None)
                    if birth_date:
                        # Convert to date object
                        player_info['birth_date'] = datetime.strptime(birth_date, "%Y-%m-%d").date()
                    else:
                        player_info['birth_date'] = None
                except (ValueError , TypeError, AttributeError):
                    player_info['birth_date'] = None
                    player_info['height'] = None
                    player_info['weight'] = None

                player_info['birth_place'] = player_info.get('birth', {}).get('place', None)
                player_info['birth_country'] = player_info.get('birth', {}).get('country', None) # pop last item remove nested dict
                
                player_info.pop('birth', None)  # Remove the original 'birth' dict

                statistics_list = player.get('statistics', [])
                for stats in statistics_list:
                    team_info = {'team_id': stats.get('team', {}).get('id', None)}  # Simplify to only team_id
                    league_info = {'league_id': stats.get('league',{}).get('id', None)}  # Simplify to only league_id
                    stats_info = {'position': stats.get('games', {}).get('position', {})} # Simplify to only position

                combined_info = {**player_info, **team_info, **league_info, **stats_info}
                all_players_list.append(combined_info)
        
        players_df = pd.json_normalize(all_players_list)

        # TODO: Clean up data frame columns if necessary
        players_df.replace({pd.NA: None}, inplace=True) # replace pandas NA with None
        players_df.replace({np.nan: None}, inplace=True) # replace numpy nan with None
        return players_df

    def normalise_all_players(self):
        pass


if __name__ == '__main__':
    client = APIFootballClient()
    print(client)