# wellcomecollection.org Services

Services that are directly related to the Wellcome Collection website and its user-facing features.

- [content_frontend / identity_frontend](#content_frontend-identity_frontend)
- [account.wellcomecollection.org](#accountwellcomecollectionorg)
- [dash.wellcomecollection.org](#dashwellcomecollectionorg)
- [cardigan.wellcomecollection.org](#cardiganwellcomecollectionorg)
- [rss_feed](#rss_feed)
- [toggles.wellcomecollection.org](#toggleswellcomecollectionorg)

## content_frontend / identity_frontend

These services are built with Next.js and provide the main website content and user account management features.

```mermaid
C4Container
    title Container Diagram for wellcomecollection.org with Account Boundaries

    Person(user, "Website User", "A visitor to wellcomecollection.org")

    System_Ext(prismic, "Prismic APIs", "External Headless CMS")

    System_Boundary(experience_account, "Experience AWS Account") {
        Container(cloudfront, "CloudFront", "AWS CDN", "Receives all user traffic and routes based on URL path.")
        ContainerDb(s3, "S3 Bucket", "AWS S3", "Serves static assets for the website.")
        Container(alb, "Application Load Balancer", "AWS ALB", "Routes application traffic to the correct frontend service.")

        Container(content_frontend, "Content Frontend", "ECS Service", "Renders the main website content.")
        Container(identity_frontend, "Identity Frontend", "ECS Service", "Renders the '/account' pages.")
    }

    System_Boundary(catalogue_account, "Catalogue AWS Account") {
        Container(content_api, "Content API", "ECS Service")
        Container(catalogue_api, "Catalogue API", "ECS Service")
        Container(search_api, "Search API", "ECS Service")
        Container(concepts_api, "Concepts API", "ECS Service")
        Container(items_api, "Items API", "ECS Service")
    }

    System_Boundary(identity_account, "Identity AWS Account") {
        Container(requesting_api, "Requesting API", "ECS Service")
        Container(identity_api, "Identity API", "ECS Service", "v1-api.account.wellcomecollection.org")
    }

    System_Boundary(digirati_account, "Digirati AWS Account") {
        Container(iiif_api, "IIIF Image API", "ECS Service", "iiif.wellcomecollection.org")
    }

    Rel(user, cloudfront, "Visits wellcomecollection.org", "HTTPS")

    Rel(cloudfront, s3, "Routes requests for static assets to")
    Rel(cloudfront, alb, "Routes all other requests to")

    Rel(alb, content_frontend, "Routes requests to", "Default traffic")
    Rel(alb, identity_frontend, "Routes '/account/*' requests to")

    Rel(content_frontend, prismic, "Requests data from")
    Rel(content_frontend, content_api, "Requests data from")
    Rel(content_frontend, catalogue_api, "Requests data from")
    Rel(content_frontend, search_api, "Requests data from")
    Rel(content_frontend, concepts_api, "Requests data from")
    Rel(content_frontend, items_api, "Requests data from")
    Rel(content_frontend, iiif_api, "Requests images from")

    Rel(identity_frontend, identity_api, "Requests data from")
    Rel(identity_frontend, requesting_api, "Requests data from")
```

See the following repositories for more details on the services described above:

- [wellcomecollection/wellcomecollection.org](https://github.com/wellcomecollection/wellcomecollection.org)
- [wellcomecollection/catalogue-api](https://github.com/wellcomecollection/catalogue-api)
- [wellcomecollection/identity](https://github.com/wellcomecollection/identity)

## account.wellcomecollection.org

This service handles user account management, including registration, and login and is managed by Auth0. It integrates with the Sierra library management system for user authentication. Successful logins redirect to the main website, and will set a cookie to indicate the user is logged in.

```mermaid
C4Container
    title Container Diagram for account.wellcomecollection.org

    Person(user, "Library Member", "A user of Wellcome Collection's digital services.")

    System_Boundary(auth0_platform, "Auth0 Platform") {
        Container(universal_login, "Universal Login Page", "Auth0 Hosted", "Handles login, sign-up, and forgot password flows.")
    }

    System_Ext(sierra, "Sierra", "3rd Party Cloud-Hosted Library Management System", "The system of record for library members.")

    Rel(user, universal_login, "Uses", "HTTPS")
    Rel(universal_login, sierra, "Authenticates users against", "Custom Database Integration")
```

See the following repositories for more details on the services described above:

- [wellcomecollection/wellcomecollection.org](https://github.com/wellcomecollection/wellcomecollection.org)
- [wellcomecollection/identity](https://github.com/wellcomecollection/identity)

## dash.wellcomecollection.org

This service provides a dashboard for staff and developers, built with Next.js. It includes the toggles dashboard that drops cookies to indicate which features are enabled for the user.

```mermaid
C4Container
    title Container Diagram for dash.wellcomecollection.org

    Person(user, "User", "A user accessing the dashboard.")

    System_Boundary(experience_account, "Experience AWS Account") {
        Container(cloudfront, "CloudFront Distribution", "AWS CDN", "Serves the dashboard application to users.")
        ContainerDb(s3, "S3 Website", "AWS S3", "Hosts the static files for dash.wellcomecollection.org.")
    }

    Rel(user, cloudfront, "Accesses dash.wellcomecollection.org", "HTTPS")
    Rel(cloudfront, s3, "Pulls content from")
```

See the following repositories for more details on the services described above:

- [wellcomecollection/wellcomecollection.org](https://github.com/wellcomecollection/wellcomecollection.org)

## cardigan.wellcomecollection.org

This service is the Storybook component library for the design system, built with Next.js.

```mermaid
C4Container
    title Container Diagram for cardigan.wellcomecollection.org

    Person(user, "Developer / Designer", "A user of the Storybook design system.")

    System_Boundary(experience_account, "Experience AWS Account") {
        Container(cloudfront, "CloudFront Distribution", "AWS CDN", "Serves the Cardigan design system application.")
        ContainerDb(s3, "S3 Website", "AWS S3", "Hosts the static files for cardigan.wellcomecollection.org.")
    }

    Rel(user, cloudfront, "Accesses cardigan.wellcomecollection.org", "HTTPS")
    Rel(cloudfront, s3, "Pulls content from")
```

See the following repositories for more details on the services described above:

- [wellcomecollection/wellcomecollection.org](https://github.com/wellcomecollection/wellcomecollection.org)

## rss_feed

This service generates RSS feeds for website content.

```mermaid
C4Container
    title Container Diagram for rss.wellcomecollection.org

    Person(subscriber, "RSS Subscriber", "A user or application consuming the RSS feed.")

    System_Ext(prismic, "Prismic APIs", "External Headless CMS")

    System_Boundary(experience_account, "Experience AWS Account") {
        Container(rss_cloudfront, "CloudFront Distribution", "AWS CDN", "Receives traffic for rss.wellcomecollection.org.")
        Container(alb, "Application Load Balancer", "AWS ALB", "Routes application traffic.")
        Container(content_frontend, "Content Frontend", "ECS Service", "Renders RSS feed for '/rss' paths.")
    }

    Rel(subscriber, rss_cloudfront, "Requests RSS feed via", "HTTPS")
    Rel(rss_cloudfront, alb, "Routes requests to")
    Rel(alb, content_frontend, "Forwards requests to")
    Rel(content_frontend, prismic, "Pulls data for feed from")
```

See the following repositories for more details on the services described above:

- [wellcomecollection/wellcomecollection.org](https://github.com/wellcomecollection/wellcomecollection.org)

## toggles.wellcomecollection.org

This service provides a JSON endpoint for feature flags and A/B testing toggles. It is used by the main website to determine which features are enabled for the user.

```mermaid
C4Container
    title Combined view of a user request and server-side toggle fetching

    Person(user, "Website User", "A visitor to wellcomecollection.org")

    System_Boundary(experience_account, "Experience AWS Account") {
        Container(main_cloudfront, "CloudFront (wellcomecollection.org)", "AWS CDN", "Main entry point for the website.")
        Container(alb, "Application Load Balancer", "AWS ALB", "Routes application traffic.")
        Container(content_frontend, "Content Frontend", "ECS Service", "Renders website pages; consumes feature toggles.")
        Container(toggles_cloudfront, "CloudFront (toggles)", "AWS CDN", "Serves the toggles JSON file.")
        ContainerDb(toggles_s3, "S3 Bucket (toggles)", "AWS S3", "Hosts the static JSON file of toggles.")
    }

    Rel(user, main_cloudfront, "1. Requests a page", "HTTPS")
    Rel(main_cloudfront, alb, "2. Routes request to")
    Rel(alb, content_frontend, "3. Forwards request to")

    Rel(content_frontend, toggles_cloudfront, "4. Fetches toggles.json", "HTTPS (Server-Side)")
    Rel(toggles_cloudfront, toggles_s3, "5. Pulls file from")
```

See the following repositories for more details on the services described above:

- [wellcomecollection/wellcomecollection.org](https://github.com/wellcomecollection/wellcomecollection.org)