import json
import os 
from google.cloud import storage
import joblib
import pandas as pd

# LOAD ENVIRONMENT VARIABLES
BUCKET_NAME = os.environ.get("BUCKET_NAME", "Missing environment variable: BUCKET_NAME")
MODEL_FILE_PATH = os.environ.get("MODEL_FILE_PATH", "Missing environment variable: MODEL_FILE_PATH")

features = []

# PROCESSES
def parse_data(request):
    return json.loads(request.json)

def download_model():
    client = storage.Client()
    bucket = client.bucket(BUCKET_NAME)
    blob = bucket.blob(MODEL_FILE_PATH)
    blob.download_to_filename('/tmp'+MODEL_FILE_PATH)
    return joblib.load('/tmp'+MODEL_FILE_PATH)

def process_data(data):
    # TODO: insert additional data processing (feature engineering, etc.) here
    return pd.DataFrame.from_dict(data, orient='index').T[features]

def predict(model, model_input):
    run_prb = model.predict_proba(model_input)[0][1]
    return json.dumps({
        'playType': 'Run' if run_prb > 0.5 else 'Pass',
        'confidence': run_prb
    })

# ENTRY POINT
def handle_request(request):
    data = parse_data(request)
    if not data:
        return 'No data provided', 400
    model = download_model()
    model_input = process_data(data)
    predictions = predict(model, model_input)
    return predictions, 200, { 'Content-Type': 'application/json' }