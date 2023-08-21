#!/bin/bash

echo "Starting migrations extraction process..."

# Disable path conversion for MSYS (for Windows Git Bash compatibility)
export MSYS_NO_PATHCONV=1

# Step 1: Run makemigrations inside the pod
kubectl exec deployment/invent-django -- python manage.py makemigrations

# Step 2: Archive migration directories inside the pod
kubectl exec deployment/invent-django -- sh -c "find /src -type d -name 'migrations' -print0 | xargs -0 tar -cf /tmp/migrations.tar"

# Step 3: Retrieve the tar archive from the pod
POD_NAME=$(kubectl get pods -l app.kubernetes.io/instance=invent-django -o jsonpath='{.items[0].metadata.name}')
kubectl cp $POD_NAME:/tmp/migrations.tar migrations.tar

# Step 4: Extract the tar archive and move migration files
tar -xf migrations.tar
cp -r src/. django/
rm -r src/ migrations.tar

echo "Migration files have been extracted and copied to the django/ directory."
