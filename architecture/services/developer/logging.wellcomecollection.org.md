# logging.wellcomecollection.org

## Architecture

Centralised logging for applications and services.

This service provides a centralised logging solution for all Wellcome Collection applications and services. Logs from ECS services are forwarded to Elasticsearch using Firelens as a sidecar container, while logs from AWS Lambda functions are sent to CloudWatch Logs and then streamed to Elasticsearch by a dedicated log shipper Lambda. All logs are stored and indexed in Elasticsearch, which is hosted in Elastic Cloud, and can be visualised and queried using Kibana.

See [this ADR for more details](../../../adr/logging.md).

```mermaid
C4Container
    title Logging Architecture

    System_Boundary(example_aws, "Example AWS Account") {
        Container(ecs_service, "ECS Service", "ECS Task", "Application container with Firelens sidecar for log forwarding.")
        Container(lambda_function, "Lambda Function", "AWS Lambda", "Emits logs to CloudWatch.")
        Container(firelens, "Firelens Sidecar", "Firelens", "Forwards ECS logs to Elasticsearch.")
        Container(lambda_log_shipper, "Lambda Log Shipper", "AWS Lambda", "Streams CloudWatch logs to Elasticsearch.")
        Container(cloudwatch, "CloudWatch Logs", "AWS CloudWatch", "Receives logs from Lambda.")
    }

    System_Boundary(elastic_cloud, "Elastic Cloud AWS Account") {
        ContainerDb(elasticsearch, "Elasticsearch", "Elastic Cloud", "Central log storage and search.")
        Container(kibana, "Kibana", "Elastic Cloud", "Log visualisation and dashboards.")
    }

    Rel(ecs_service, firelens, "Forwards logs to")
    Rel(firelens, elasticsearch, "Sends logs to", "HTTPS")
    Rel(lambda_function, cloudwatch, "Sends logs to")
    Rel(cloudwatch, lambda_log_shipper, "Triggers log shipper")
    Rel(lambda_log_shipper, elasticsearch, "Streams logs to", "HTTPS")
    Rel(elasticsearch, kibana, "Visualised in")

    UpdateLayoutConfig($c4ShapeInRow="3", $c4BoundaryInRow="1")
```

## Repositories

- [wellcomecollection/platform-infrastructure](https://github.com/wellcomecollection/platform-infrastructure/tree/main/logging)
- [wellcomecollection/elasticsearch-log-forwarder](https://github.com/wellcomecollection/elasticsearch-log-forwarder)
- [wellcomecollection/terraform-aws-ecs-service](https://github.com/wellcomecollection/terraform-aws-ecs-service/blob/main/modules/firelens/main.tf)

## Accounts

This configuration is used by all Collection AWS accounts.