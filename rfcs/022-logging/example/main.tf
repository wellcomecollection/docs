resource "aws_ecs_cluster" "example" {
  name = "logging-example"
}

resource "aws_ecs_task_definition" "example" {
  family = "logging-example"

  network_mode = "awsvpc"

  requires_compatibilities = [
    "FARGATE"
  ]

  cpu = 256
  memory = 512

  task_role_arn = aws_iam_role.task_role.arn
  execution_role_arn = aws_iam_role.execution_role.arn

  container_definitions = local.container_definitions
}

resource "aws_ecs_service" "example" {
  name          = "logging-example"
  cluster       = aws_ecs_cluster.example.id
  desired_count = 1

  platform_version = "1.3.0"

  launch_type = "FARGATE"

  network_configuration {
    subnets         = local.private_subnets
    security_groups = [
      aws_security_group.allow_full_egress.id
    ]
  }

  task_definition = "${local.family}:${local.revision}"
}

resource "aws_security_group" "allow_full_egress" {
  name        = "full_egress"
  description = "Allow outbound traffic"
  vpc_id = local.vpc_id

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_ecr_repository" "example" {
  name = "uk.ac.wellcome/logging-example"
}

resource "aws_ecr_repository" "fluentbit" {
  name = "uk.ac.wellcome/fluentbit-example"
}