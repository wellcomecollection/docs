# iiif.wellcomecollection.org

The IIIF APIs serve metadata and images for Wellcome Collection digital assets ingested via the digital preservation workflow.

## Architecture

```mermaid
C4Container
    title Container Diagram for the IIIF APIs

    System(client_app, "Client Application", "e.g., content_frontend, requesting IIIF manifests and images.")

    System_Boundary(platform_account, "Platform AWS Account") {
        Container(api_cloudfront, "CloudFront (iiif.wellcomecollection.org)", "AWS CDN", "Entry point for IIIF APIs.")
    }

    System_Boundary(digirati_account, "Digirati AWS Account") {
        Container(dlcs, "Digital Library Cloud Services (DLCS)", "ECS Service", "Serves IIIF Presentation and Image APIs.")
    }

    Rel(client_app, api_cloudfront, "Requests manifests and images from", "HTTPS")
    Rel(api_cloudfront, dlcs, "Routes requests to", "HTTPS")
```

DLCS services contain a number of complex subsystems, not described here. 

Further detail is available in the DLCS repository linked below.

## Accounts

- [digirati](../../aws_accounts.md#digirati)

## Repositories

See the following repositories for more details on the services described above:

- [wellcomecollection/platform-infrastructure](https://github.com/wellcomecollection/platform-infrastructure)
- [dlcs/protagonist](https://github.com/dlcs/protagonist)
