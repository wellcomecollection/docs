# dash.wellcomecollection.org

This service provides a dashboard for staff and developers, built with Next.js. It includes the toggles dashboard that drops cookies to indicate which features are enabled for the user.

## Architecture

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

## Accounts

- [experience](../../aws_accounts.md#experience)

## Repositories

See the following repositories for more details on the services described above:

- [wellcomecollection/wellcomecollection.org](https://github.com/wellcomecollection/wellcomecollection.org)
