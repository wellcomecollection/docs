#!/usr/bin/env bash

DOCKER_LOGIN=$(aws ecr get-login --no-include-email --profile platform)
$DOCKER_LOGIN

ECR_REPO=ACCOUNT_ID.dkr.ecr.eu-west-1.amazonaws.com/uk.ac.wellcome/fluentbit-example:latest

docker build -t fluentbit_custom:latest .
docker tag fluentbit_custom:latest $ECR_REPO
docker push $ECR_REPO