import requests
import json
import os
from google.cloud import storage

# LOAD ENVIRONMENT VARIABLES
BASE_URI = os.environ.get("BASE_URI", "Missing environment variable: BASE_URI")
BUCKET_NAME = os.environ.get("BUCKET_NAME", "Missing environment variable: BUCKET_NAME")
DATA_FILE_PATH = os.environ.get("DATA_FILE_PATH", "Missing environment variable: DATA_FILE_PATH")

# HELPER FUNCTIONS
def find_scoring_split(data):
    return data["name"] == "overall"

def find_points_for(data):
    return data["name"] == "pointsFor"

def find_points_against(data):
    return data["name"] == "pointsAgainst"

# PROCESSES
def get_scoring_stats():
    team_list_req = requests.get(BASE_URI)
    team_list = team_list_req.json()

    response = {}

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

        response[team_data["abbreviation"]] = {
            "points_for": points_for,
            "points_against": points_against,
        }

    return response 

def upload_data(data):
    client = storage.Client()
    bucket = client.bucket(BUCKET_NAME)
    blob = bucket.blob(DATA_FILE_PATH)
    blob.upload_from_string(json.dumps(data), content_type="application/json")

# ENTRY POINT
def handle_request():
    data = get_scoring_stats()
    upload_data(data)
