#!/usr/bin/env bash

set -o nounset

CLUSTER_NAME=$(terraform output ecs_example_cluster_name)
SERVICE_NAME=$(terraform output ecs_example_service_name)

# Force service deployment
aws ecs update-service \
  --cluster "$CLUSTER_NAME" \
  --service "$SERVICE_NAME" \
  --force-new-deployment \
  --profile platform