# wellcomelibrary_redirects

## Architecture

Redirects for the legacy Wellcome Library website.

C4Container
    title Simplified Container diagram for Storage Service

    Person(user, "Website User", "A visitor to https://wellcomelibrary.org")

    System_Boundary(platform_account, "Platform AWS Account") {
        Container(wellcomecollection_cloudfront, "CloudFront (wellcomecollection.org)", "AWS CDN", "Receives all user traffic and routes based on URL path.")

        System_Boundary(cloudfront, "Wellcome Library CloudFront") {
            Container(wellcomelibrary_cloudfront, "CloudFront (wellcomelibrary.org)", "AWS CDN", "Routes API requests.")
            Container(wellcomelibrary_cloudfront_functions, "Redirect Lambda", "Lambda@Edge", "Generates request redirects.")
        }
        
        Container(api_cloudfront, "CloudFront (api.wellcomecollection.org)", "AWS CDN", "Main entry point for all APIs.")

    }

    Rel(user, wellcomelibrary_cloudfront, "Navigates to https://wellcomelibrary.org")
    Rel(wellcomelibrary_cloudfront, wellcomelibrary_cloudfront_functions, "Proxies request")
    Rel(wellcomelibrary_cloudfront_functions, api_cloudfront, "Performs image ID lookup")
    Rel(user, wellcomecollection_cloudfront, "Redirected to")


    UpdateLayoutConfig($c4ShapeInRow="2", $c4BoundaryInRow="1")

## Repositories

See the following repositories for more details on the services described above:

- [wellcomecollection/wellcomelibrary.org](https://github.com/wellcomecollection/wellcomelibrary.org)

## Accounts

- [platform](../../aws_accounts.md#platform)
