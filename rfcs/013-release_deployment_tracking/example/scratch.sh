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
docker tag busybox:1.30.1 example:30
docker tag example:30 $ECR_EXAMPLE_REPO_URI:30
docker push "$ECR_EXAMPLE_REPO_URI":30

docker tag example:31 example:latest
docker tag example:latest "$ECR_EXAMPLE_REPO_URI":latest
docker push "$ECR_EXAMPLE_REPO_URI":latest

# Push latest to stage
docker tag example:latest example:stage
docker tag example:stage "$ECR_EXAMPLE_REPO_URI":stage
docker push "$ECR_EXAMPLE_REPO_URI":stage

# View images in ECR
aws ecr list-images \
  --repository-name "uk.ac.wellcome/example" \
  --profile platform

# Force service deployment
aws ecs update-service \
  --cluster "$CLUSTER_NAME" \
  --service "$SERVICE_NAME" \
  --force-new-deployment \
  --profile platform > deployment.json

# New deployment is always first in list
jq ".service.deployments[0].id" deployment.json
