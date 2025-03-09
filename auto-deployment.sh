# set another 4 bash variables
PROJECT_ID=brianrivera26techx25
SERVICE_NAME=catlovers-app
OIDC_NAME=project-repo  # do not change this line
GITHUB_ORG=ISE-GenAI-TechX25-Section-A
# set another 4 bash variables
WORKLOAD_IDENTITY_POOL_ID=projects/732301616375/locations/global/workloadIdentityPools/github
WORKLOAD_IDENTITY_PROVIDER=projects/732301616375/locations/global/workloadIdentityPools/github/providers/project-repo
PROJECT_NUMBER=732301616375
GITHUB_REPO_NAME=CatLovers_A5

gcloud config set project brianrivera26techx25

# run this command exactly
gcloud iam workload-identity-pools create "github" \
    --project="${PROJECT_ID}" \
    --location="global" \
    --display-name="GitHub Actions Pool"

if [ $? != 0 ]; then
    echo "'workload-identity-pools create' failed!"
    exit 1
fi

# run this command exactly
gcloud iam workload-identity-pools providers create-oidc "${OIDC_NAME}" \
    --project="${PROJECT_ID}" \
    --location="global" \
    --workload-identity-pool="github" \
    --display-name="My GitHub repo Provider" \
    --attribute-mapping="google.subject=assertion.sub,attribute.actor=assertion.actor,attribute.repository=assertion.repository,attribute.repository_owner=assertion.repository_owner" \
    --attribute-condition="assertion.repository_owner == '${GITHUB_ORG}'" \
    --issuer-uri="https://token.actions.githubusercontent.com"

if [ $? != 0 ]; then
    echo "'workload-identity-pools providers create-oidc' failed!"
    exit 1
fi

# run this command exactly
gcloud iam service-accounts add-iam-policy-binding "${PROJECT_NUMBER}-compute@developer.gserviceaccount.com" \
  --project="${PROJECT_ID}" \
  --role="roles/iam.workloadIdentityUser" \
  --member="principalSet://iam.googleapis.com/${WORKLOAD_IDENTITY_POOL_ID}/attribute.repository/${GITHUB_ORG}/${GITHUB_REPO_NAME}"


if [ $? != 0 ]; then
    echo "'service-accounts add-iam-policy-binding' failed!"
    exit 1
fi