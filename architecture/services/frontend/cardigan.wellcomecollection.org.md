# cardigan.wellcomecollection.org

This service is the Storybook component library for the design system, built with Next.js.

## Architecture

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

## Accounts

- [experience](../../aws_accounts.md#experience)

## Repositories

See the following repositories for more details on the services described above:

- [wellcomecollection/wellcomecollection.org](https://github.com/wellcomecollection/wellcomecollection.org)
