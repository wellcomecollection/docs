# rss_feed

This service generates RSS feeds for website content.

## Architecture

```mermaid
C4Container
    title Container Diagram for rss.wellcomecollection.org

    Person(subscriber, "RSS Subscriber", "A user or application consuming the RSS feed.")

    System_Boundary(experience_account, "Experience AWS Account") {
        Container(rss_cloudfront, "CloudFront Distribution", "AWS CDN", "Receives traffic for rss.wellcomecollection.org.")
        Container(alb, "Application Load Balancer", "AWS ALB", "Routes application traffic.")
        Container(content_frontend, "Content Frontend", "ECS Service", "Renders RSS feed for '/rss' paths.")
    }

    System_Boundary(public_internet, "Public Internet") {
        System_Ext(prismic, "Prismic APIs", "External Headless CMS")
    }

    Rel(subscriber, rss_cloudfront, "Requests RSS feed via", "HTTPS")
    Rel(rss_cloudfront, alb, "Routes requests to")
    Rel(alb, content_frontend, "Forwards requests to")
    Rel(content_frontend, prismic, "Pulls data for feed from")

    UpdateLayoutConfig($c4ShapeInRow="3", $c4BoundaryInRow="1")
```

## Accounts

- [experience](../../aws_accounts.md#experience)

## Repositories

See the following repositories for more details on the services described above:

- [wellcomecollection/wellcomecollection.org](https://github.com/wellcomecollection/wellcomecollection.org)
