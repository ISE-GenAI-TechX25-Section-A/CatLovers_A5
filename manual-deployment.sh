

gcloud config set project brianrivera26techx25

if [ $? != 0 ]; then
    echo "'gcloud config set project' failed!"
    exit 1
fi

gcloud services enable vision.googleapis.com
read -p "Please enter your techX email: " USER_ID
gcloud projects add-iam-policy-binding brianrivera26techx25 --member="user:$USER_ID" --role=roles/storage.objectViewer
PROJECT_ID=brianrivera26techx25  
SERVICE_NAME=catlovers-app 

# run the below command exactly (do not change anything!) the bash variables set above will get populated here
gcloud builds submit --tag gcr.io/${PROJECT_ID}/${SERVICE_NAME}

if [ $? != 0 ]; then
    echo "'gcloud builds' failed!"
    exit 1
fi

# run this command exactly (do not change anything!)
gcloud run deploy ${SERVICE_NAME} \
    --image gcr.io/${PROJECT_ID}/${SERVICE_NAME}:latest \
    --region us-central1 \
    --allow-unauthenticated

if [ $? != 0 ]; then
    echo "'gcloud run deploy' failed!"
fi