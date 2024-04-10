resource "aws_ecs_cluster" "example" {
  name = "deployment-example"
}

resource "aws_ecs_task_definition" "example" {
  family = "deployment-example"

  network_mode = "awsvpc"

  requires_compatibilities = [
    "FARGATE"
  ]

  cpu = 256
  memory = 512

  execution_role_arn = aws_iam_role.ecsTaskExecutionRole.arn

  container_definitions = <<DEFINITION
[{
  "essential": true,
  "image": "${aws_ecr_repository.example.repository_url}:prod",
  "name": "app",
  "command": ["/bin/sh", "-c", "while true; do echo \"zzz\" && sleep 5s; done"]
}]
DEFINITION
}

resource "aws_ecs_service" "example" {
  name          = "deployment-example"
  cluster       = aws_ecs_cluster.example.id
  desired_count = 1

  launch_type = "FARGATE"

  network_configuration {
    security_groups = []
    subnets         = local.private_subnets
  }

  task_definition = "${local.family}:${local.latest_revision}"
}

data "aws_ecs_task_definition" "example" {
  task_definition = local.family
}

locals {
  family = aws_ecs_task_definition.example.family

  local_revision  = aws_ecs_task_definition.example.revision
  remote_revision = data.aws_ecs_task_definition.example.revision

  private_subnets = data.terraform_remote_state.infra_shared.outputs.catalogue_vpc_delta_private_subnets

  # Track the latest ACTIVE revision
  latest_revision = max(local.local_revision, local.remote_revision)
}

resource "aws_ecr_repository" "example" {
  name = "uk.ac.wellcome/deployment-example"
}