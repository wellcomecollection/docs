# wellcomeimages_redirects

## Architecture

Redirects for the legacy Wellcome Images website.

```mermaid
C4Container
    title Simplified Container diagram for Storage Service

    Person(user, "Website User", "A visitor to https://wellcomeimages.org")

    System_Boundary(experience_account, "Experience AWS Account") {
                Container(wellcomecollection_cloudfront, "CloudFront (wellcomecollection.org)", "AWS CDN", "Receives all user traffic and routes based on URL path.")

        System_Boundary(cloudfront, "Wellcome Images CloudFront") {

        Container(wellcomeimages_cloudfront, "CloudFront (wellcomeimages.org)", "AWS CDN", "Routes API requests.")
        Container(wellcomeimages_cloudfront_functions, "Redirect Lambda", "Lambda@Edge", "Generates request redirects.")
        }
    }

    System_Boundary(platform_account, "Platform AWS Account") {
        Container(iiif_api_cloudfront, "CloudFront (iiif.wellcomecollection.org)", "AWS CDN", "Entry point for IIIF APIs.")
    }

    System_Boundary(platform_account, "Platform AWS Account") {
        Container(api_cloudfront, "CloudFront (api.wellcomecollection.org)", "AWS CDN", "Main entry point for all APIs.")
    }

    Rel(user, wellcomeimages_cloudfront, "Navigates to https://wellcomeimages.org")
    Rel(wellcomeimages_cloudfront, wellcomeimages_cloudfront_functions, "Proxies request")
    Rel(wellcomeimages_cloudfront_functions, api_cloudfront, "Performs image ID lookup")
    Rel(user, iiif_api_cloudfront, "Redirected to")
    Rel(user, wellcomecollection_cloudfront, "Redirected to")


    UpdateLayoutConfig($c4ShapeInRow="2", $c4BoundaryInRow="2")
```

## Repositories

- [wellcomecollection/wellcomeimages.org](https://github.com/wellcomecollection/wellcomeimages.org)

## Accounts

- [experience](../../aws_accounts.md#experience)