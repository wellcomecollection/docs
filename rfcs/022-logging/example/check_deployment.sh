#!/usr/bin/env bash

set -o nounset

# Usage: ./check_deployment.sh fluentbit-example log_router

REPO_NAME=${1:-fluentbit-example}
CONTAINER_NAME=${2:-log_router}

ECR_REPO=760097843905.dkr.ecr.eu-west-1.amazonaws.com/uk.ac.wellcome/"$REPO_NAME"

CLUSTER_NAME=$(terraform output ecs_example_cluster_name)
SERVICE_NAME=$(terraform output ecs_example_service_name)

LATEST_DIGEST=$(docker images "$ECR_REPO" --digests --format "{{.Tag}} {{.Digest}}" | grep latest | awk '{print $2}')

echo "LATEST_DIGEST: $LATEST_DIGEST"

aws ecs list-tasks \
  --cluster "$CLUSTER_NAME" \
  --service-name "$SERVICE_NAME" \
  --profile platform > task_list.json

TASK_ARNS=$(jq ".taskArns[]" -r task_list.json)

echo ""
echo "All TASK_DIGESTS will match the LATEST_DIGEST when the deployment is complete."
echo ""

for ARN in $TASK_ARNS
do
  TASK=$(aws ecs describe-tasks --cluster "$CLUSTER_NAME" --tasks "$ARN" --profile platform)
  TASK_DIGEST=$(echo "$TASK" | jq ".tasks[].containers[] | select(.name|test(\"$CONTAINER_NAME\")) | .imageDigest" -r)

  MATCH_STRING="match"

  if [ "$LATEST_DIGEST" != "$TASK_DIGEST" ]
  then
    MATCH_STRING="no_match"
  fi

  echo "TASK_DIGEST: $TASK_DIGEST ($MATCH_STRING)"
done

