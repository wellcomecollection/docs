# dlcs_iiif

## Architecture

The Digital Library Cloud Service for serving IIIF images.

See [this diagram for a detailed overview of the DLCS architecture](https://raw.githubusercontent.com/dlcs/protagonist/master/docs/c4-container-diagrams/DLCS-2023-l2.png), provided by Digirati.

It is maintained by a third-party vendor, [Digirati](../../partners.md), and is used to serve IIIF images and other material for the Wellcome Collection.

```mermaid
C4Container
    title DLCS IIIF Architecture

    System_Boundary(storage_account, "Storage AWS Account") {
        Container_Ext(storage_s3, "Storage S3 Bucket", "S3", "Stores digital assets for ingest.")
        Container_Ext(storage_service, "Storage Service", "ECS Service", "Notifies DLCS of new assets.")
    }


    System_Boundary(staff_users, "Staff Users") {
        Person(staff_user, "Staff User", "Browses ingest and processing status.")
    }

    System_Boundary(dlcs_account, "Digirati AWS Account") {
                    Container(dlcs_dashboard, "DLCS Dashboard", "Web App", "Staff-facing dashboard for managing assets.")
        System_Boundary(dlcs_backend, "DLCS Back-end") {
            Container(dlcs_ecs, "DLCS ECS Service", "ECS Service", "Processes assets, generates IIIF manifests, serves IIIF APIs.")
            ContainerDb(dlcs_s3, "DLCS S3", "S3", "Stores processed images and manifests.")
            ContainerDb(dlcs_lustre, "DLCS Lustre", "Lustre FS", "High-performance file storage for image processing.")
        }
    }

    System_Boundary(platform_account, "Platform AWS Account") {
        Container(api_cloudfront, "CloudFront (iiif.wellcomecollection.org)", "AWS CDN", "Entry point for IIIF APIs.")
    }

    System_Boundary(users, "Website Users") {
        Person(website_user, "Website User", "Browses IIIF images and manifests via the IIIF APIs.")
    }

    Rel(storage_service, dlcs_ecs, "Notifies of new assets")
    Rel(dlcs_ecs, storage_s3, "Retrieves assets from")
    Rel(dlcs_ecs, dlcs_s3, "Stores processed images/manifests in")
    Rel(dlcs_ecs, dlcs_lustre, "Uses for image serviing")
    Rel(dlcs_ecs, api_cloudfront, "Requests IIIF images/manifests from", "IIIF APIs")
    Rel(website_user, api_cloudfront, "Requests IIIF images/manifests from", "IIIF APIs")

    Rel(dlcs_dashboard, dlcs_ecs, "Manages assets via API")
    Rel(staff_user, dlcs_dashboard, "View ingest and processing status")


    UpdateLayoutConfig($c4ShapeInRow="2", $c4BoundaryInRow="3")
```

## Repositories

See the following repositories for more details on the services described above:

- [dlcs/protagonist](https://github.com/dlcs/protagonist)

## Accounts
