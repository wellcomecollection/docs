#!/usr/bin/env bash

set -o nounset

# Usage: ./deploy.sh prod app

RELEASE_HASH=${1:-hash_1}

# Get ECR repository URI from terraform
ECR_EXAMPLE_REPO_URI=$(terraform output ecr_example_repo_uri)
CLUSTER_NAME=$(terraform output ecs_example_cluster_name)
SERVICE_NAME=$(terraform output ecs_example_service_name)

# Login to ECR
DOCKER_LOGIN=$(aws ecr get-login --no-include-email --profile platform)
$DOCKER_LOGIN

# Setup example image using busybox
docker pull busybox:1.30.1

# Simulate building and labelling with id & latest
docker tag busybox:1.30.1 example:hash_1
docker tag example:hash_1 "$ECR_EXAMPLE_REPO_URI":hash_1
docker push "$ECR_EXAMPLE_REPO_URI":hash_1

echo ""

docker tag busybox:1.31.1 example:hash_2
docker tag example:31 "$ECR_EXAMPLE_REPO_URI":hash_2
docker push "$ECR_EXAMPLE_REPO_URI":hash_2

echo ""

# Push hash to prod
docker tag example:"$RELEASE_HASH" example:prod
docker tag example:prod "$ECR_EXAMPLE_REPO_URI":prod
docker push "$ECR_EXAMPLE_REPO_URI":prod

echo ""
echo "Images in ECR"
echo ""


# View images in ECR
aws ecr list-images \
  --repository-name "uk.ac.wellcome/deployment-example" \
  --profile platform

echo ""
echo "Forcing service deployment"
echo ""

# Force service deployment (new deployment is always first in list)
./redeploy.sh | jq ".service.deployments[0]"
