#!/bin/sh

set -e
set -x

DIR="$(dirname "$0")"
ENV=${1:?"Usage: $0 ENVIRONMENT"}
if [ "$ENV" = "production" ]; then
  PROJECT_ID="workbenchdata-production"
else
  PROJECT_ID="workbench-staging"
fi

# rbac.yaml has a "k8s-snapshots" Kubernetes service account
kubectl apply -f "$DIR"/rbac.yaml

# Using workload identity [https://cloud.google.com/kubernetes-engine/docs/how-to/workload-identity],
# we'll also create an iam service account with the same name
gcloud iam service-accounts create k8s-snapshots

gcloud iam service-accounts add-iam-policy-binding \
  --role roles/iam.workloadIdentityUser \
  --member "serviceAccount:$PROJECT_ID.svc.id.goog[kube-system/k8s-snapshots]" \
  k8s-snapshots@$PROJECT_ID.iam.gserviceaccount.com

kubectl -n kube-system annotate serviceaccount k8s-snapshots \
  iam.gke.io/gcp-service-account=k8s-snapshots@$PROJECT_ID.iam.gserviceaccount.com

# And give the gcloud account permission
# List of roles is from
# https://github.com/miracle2k/k8s-snapshots#configure-access-permissions-to-google-cloud
gcloud iam roles create k8s_snapshots \
  --project $PROJECT_ID \
  --title "k8s-snapshots" \
  --description "k8s-snapshots Kubernetes ServiceAccount" \
  --stage ALPHA \
  --permissions compute.disks.createSnapshot,compute.snapshots.create,compute.snapshots.delete,compute.snapshots.get,compute.snapshots.list,compute.snapshots.setLabels,compute.zoneOperations.get

gcloud projects add-iam-policy-binding \
  $PROJECT_ID \
  --role projects/$PROJECT_ID/roles/k8s_snapshots \
  --member "serviceAccount:k8s-snapshots@$PROJECT_ID.iam.gserviceaccount.com"

kubectl apply -f k8s-snapshots.yaml

PATCH='{"metadata":{"annotations":{"backup.kubernetes.io/deltas":"PT12H P14D P366D"}}}'

kubectl patch pvc dbdata-pvc -p "$PATCH"
