# Hive
To update the server run the following commands from the server folder
gcloud builds submit --tag gcr.io/hive-5914/hive
gcloud beta run deploy --image gcr.io/hive-5914/hive
For server based:
firebase deploy
For local based:
firebase serve
