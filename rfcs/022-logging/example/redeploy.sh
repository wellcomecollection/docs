#!/usr/bin/env bash

set -o nounset

pushd fluentbit
./build.sh
popd

sleep 3

CLUSTER_NAME=$(terraform output ecs_example_cluster_name)
SERVICE_NAME=$(terraform output ecs_example_service_name)

# Force service deployment
aws ecs update-service \
  --cluster "$CLUSTER_NAME" \
  --service "$SERVICE_NAME" \
  --force-new-deployment \
  --profile platform | jq ".service.deployments[0]"

