import requests
import json

BASE_URI = "https://sports.core.api.espn.com/v2/sports/football/leagues/nfl/teams?limit=32"

# HELPER FUNCTIONS
def find_scoring_split(data):
    return data["name"] == "overall"

def find_points_for(data):
    return data["name"] == "pointsFor"

def find_points_against(data):
    return data["name"] == "pointsAgainst"

# ENTRY POINT
def update_scoring_stats():
    team_list_req = requests.get(BASE_URI)
    team_list = team_list_req.json()

    response = []

    for team in team_list["items"]:
        team_data_req = requests.get(team["$ref"])
        team_data = team_data_req.json()

        team_stats_req = requests.get(team_data["record"]["$ref"])
        team_stats = team_stats_req.json()

        scoring_split = list(
            filter(find_scoring_split, team_stats["items"])
        )[0]

        points_for = list(
            filter(find_points_for, scoring_split["stats"])
        )[0]["value"]

        points_against = list(
            filter(find_points_against, scoring_split["stats"])
        )[0]["value"]

        response.append({
            "team": team_data["abbreviation"],
            "points_for": points_for,
            "points_against": points_against,
        })

    return response 

print(update_scoring_stats())