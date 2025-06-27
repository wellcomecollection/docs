# workflow (Goobi)

## Architecture

The Goobi workflow management system for digitisation.

Goobi is an ECS service accessed by Wellcome Collection digital production staff. It stores workflow and process data in RDS and S3, accepts ingests from S3, processes them, and sends them to the Wellcome Storage Service for long-term storage. Goobi runs in the Workflow AWS account.

It is maintained by a third-party vendor, [Intranda](../../partners.md), and is used to manage some of the digitisation workflows for Wellcome Collection.

```mermaid
C4Container
    title Goobi Workflow Architecture

    System_Boundary(staff, "Wellcome Collection Staff") {
        Person(staff_user, "Staff User", "Accesses Goobi to manage digitisation workflows.")
    }

    System_Boundary(workflow_account, "Workflow AWS Account") {
        Container(goobi_ecs, "Goobi ECS Service", "ECS Service", "Manages digitisation workflows and processes ingests.")
        ContainerDb(goobi_rds, "Goobi RDS", "RDS", "Stores workflow/process data.")
        ContainerDb(goobi_s3, "Goobi S3", "S3", "Stores ingest files and workflow data.")
    }

    System_Boundary(storage_account, "Storage AWS Account") {
        Container_Ext(storage_service, "Wellcome Storage Service", "API Gateway", "Receives processed ingests for long-term storage.")
    }

    Rel(staff_user, goobi_ecs, "Accesses Goobi UI/API")
    Rel(goobi_ecs, goobi_rds, "Reads/writes workflow data")
    Rel(goobi_ecs, goobi_s3, "Reads/writes ingest files")
    Rel(goobi_ecs, storage_service, "Sends processed ingests to")

    UpdateLayoutConfig($c4ShapeInRow="3", $c4BoundaryInRow="1")
```

## Repositories

See the following repositories for the code and configuration related to Goobi:

- [wellcomecollection/goobi-infrastructure](https://github.com/wellcomecollection/goobi-infrastructure)

## Accounts

- [workflow](../../aws_accounts.md#workflow)
