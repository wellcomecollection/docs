resource "aws_ecs_cluster" "example" {
  name = "example"
}

resource "aws_ecs_task_definition" "example" {
  family = "example"

  container_definitions = <<DEFINITION
  [{
    "cpu": 128,
    "environment": [{
      "name": "SECRET",
      "value": "KEY"
    }],
    "essential": true,
    "image": "tutum/hello-world",
    "memory": 256,
    "memoryReservation": 64,
    "name": "app"
  }
]
DEFINITION
}

resource "aws_ecs_service" "example" {
  name          = "example"
  cluster       = aws_ecs_cluster.example.id
  desired_count = 1

  task_definition = "${local.family}:${local.latest_revision}"
}

data "aws_ecs_task_definition" "example" {
  task_definition = local.family
}

locals {
  family = aws_ecs_task_definition.example.family

  local_revision  = aws_ecs_task_definition.example.revision
  remote_revision = data.aws_ecs_task_definition.example.revision

  # Track the latest ACTIVE revision
  latest_revision = max(local.local_revision, local.remote_revision)
}

resource "aws_ecr_repository" "example" {
  name                 = "example"
  image_tag_mutability = "MUTABLE"
}