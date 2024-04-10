output "ecr_example_repo_uri" {
  value = aws_ecr_repository.example.repository_url
}

output "ecs_example_cluster_name" {
  value = aws_ecs_cluster.example.name
}

output "ecs_example_service_name" {
  value = aws_ecs_service.example.name
}