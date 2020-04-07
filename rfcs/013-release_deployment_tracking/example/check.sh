#!/usr/bin/env bash
#
#set -o nounset
#
## Usage: ./check.sh prod app

ENV_NAME=${1:-prod}
CONTAINER_NAME=${2:-app}

ECR_REPO=$(terraform output ecr_example_repo_uri)
CLUSTER_NAME=$(terraform output ecs_example_cluster_name)
SERVICE_NAME=$(terraform output ecs_example_service_name)

ENV_DIGEST=$(docker images "$ECR_REPO" --digests --format "{{.Tag}} {{.Digest}}" | grep "$ENV_NAME" | awk '{print $2}')

echo "$ENV_NAME ENV_DIGEST: $ENV_DIGEST"

aws ecs list-tasks \
  --cluster "$CLUSTER_NAME" \
  --service-name "$SERVICE_NAME" \
  --profile platform > task_list.json

TASK_ARNS=$(jq ".taskArns[]" -r task_list.json)

echo ""
echo "All TASK_DIGESTS will match the ENV_DIGEST when the deployment is complete."
echo ""

for ARN in $TASK_ARNS
do
  TASK=$(aws ecs describe-tasks --cluster "$CLUSTER_NAME" --tasks "$ARN" --profile platform)
  TASK_DIGEST=$(echo "$TASK" | jq ".tasks[].containers[] | select(.name|test(\"$CONTAINER_NAME\")) | .imageDigest" -r)

  MATCH_STRING="match"

  if [ "$TASK_DIGEST" != "$ENV_DIGEST" ]
  then
    MATCH_STRING="no_match"
  fi

  echo "TASK_DIGEST: $TASK_DIGEST ($MATCH_STRING)"
done

