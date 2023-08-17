#!/bin/bash

echo "Starting translation extraction process..."

# Disable path conversion for MSYS (for Windows Git Bash compatibility)
export MSYS_NO_PATHCONV=1

# Step 1: Get the pod name and copy the master.pot file from the pod
echo "Step 1: Fetching master.pot from the pod..."
podName=$(kubectl get pods -l app.kubernetes.io/name=invent-frontend -o jsonpath='{.items[0].metadata.name}')
kubectl cp ${podName}:/tmp/master.pot ./master.pot -c invent-frontend

# Step 2: Move the master.pot to the desired location on the local machine
echo "Step 2: Moving master.pot to the django/translations directory..."
cp ./master.pot django/translations/master.pot

echo "Master.pot has been successfully extracted and copied to src/django/translations/"
