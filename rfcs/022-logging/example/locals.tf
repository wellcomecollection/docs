locals {
  family = aws_ecs_task_definition.example.family

  revision = aws_ecs_task_definition.example.revision

  secret_esuser_arn = "arn:aws:secretsmanager:eu-west-1:760097843905:secret:shared/logging/es_user-NzgYRK"
  secret_espass_arn = "arn:aws:secretsmanager:eu-west-1:760097843905:secret:shared/logging/es_pass-Wrmt3C"
  secret_eshost_arn = "arn:aws:secretsmanager:eu-west-1:760097843905:secret:shared/logging/es_host-wFZkP1"
  secret_esport_arn = "arn:aws:secretsmanager:eu-west-1:760097843905:secret:shared/logging/es_port-KAwnVi"

  private_subnets = data.terraform_remote_state.infra_shared.outputs.catalogue_vpc_delta_private_subnets
  vpc_id = data.terraform_remote_state.infra_shared.outputs.catalogue_vpc_delta_id

  vars = {
    app_repository_url = aws_ecr_repository.example.repository_url
    fluentbit_repository_url = aws_ecr_repository.fluentbit.repository_url
    service_name = "my_service_name"

    secret_esuser_arn = local.secret_esuser_arn
    secret_espass_arn = local.secret_espass_arn
    secret_eshost_arn = local.secret_eshost_arn
    secret_esport_arn = local.secret_esport_arn
  }

  container_definitions = templatefile("${path.module}/container_definitions.json", local.vars)
}