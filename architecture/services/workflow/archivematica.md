# archivematica

## Architecture

The Archivematica digital preservation system.

Archivematica is a digital preservation system managed by Artefactual. It is accessed by Wellcome Collection staff, stores workflow and preservation data in RDS and S3, accepts ingests from S3, processes them, and sends them to the Wellcome Storage Service for long-term storage. Archivematica runs in the Workflow AWS account.

It is maintained by a third-party vendor, [Artefactual](../../partners.md), and is used to manage digital preservation workflows for Wellcome Collection.

```mermaid
C4Container
    title Archivematica Architecture

    System_Boundary(staff, "Wellcome Collection Staff") {
        Person(staff_user, "Staff User", "Accesses Archivematica to manage digital preservation workflows.")
    }

    System_Boundary(workflow_account, "Workflow AWS Account") {
        Container(archivematica, "Archivematica", "Managed Service (Artefactual)", "Manages digital preservation workflows and processes ingests.")
        ContainerDb(archivematica_rds, "Archivematica RDS", "RDS", "Stores workflow/preservation data.")
        ContainerDb(archivematica_s3, "Archivematica S3", "S3", "Stores ingest files and workflow data.")
    }

    System_Boundary(storage_account, "Storage AWS Account") {
        Container_Ext(storage_service, "Wellcome Storage Service", "API Gateway", "Receives processed ingests for long-term storage.")
    }

    Rel(staff_user, archivematica, "Accesses Archivematica UI/API")
    Rel(archivematica, archivematica_rds, "Reads/writes workflow data")
    Rel(archivematica, archivematica_s3, "Reads/writes ingest files")
    Rel(archivematica, storage_service, "Sends processed ingests to")

    UpdateLayoutConfig($c4ShapeInRow="3", $c4BoundaryInRow="1")
```

## Repositories

See the following repositories for the code and configuration related to Archivematica:

- [wellcomecollection/archivematica-infrastructure](https://github.com/wellcomecollection/archivematica-infrastructure)

## Accounts

- [workflow](../../aws_accounts.md#workflow)
