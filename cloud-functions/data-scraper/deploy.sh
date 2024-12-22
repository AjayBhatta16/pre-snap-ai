# read environment variables
echo "Enter value for BASE_URI:"
read BASE_URI

echo "Enter value for BUCKET_NAME:"
read BUCKET_NAME

echo "Enter value for DATA_FILE_PATH:"
read DATA_FILE_PATH

# run GCloud command
gcloud functions deploy update-scoring-stats \
    --runtime python39 \
    --trigger-topic update-stats \
    --entry-point handle_request \
    --source . \
    --set-env-vars BASE_URI=$BASE_URI, BUCKET_NAME=$BUCKET_NAME, DATA_FILE_PATH=$DATA_FILE_PATH