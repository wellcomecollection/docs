# identity_api

The Identity API is responsible for managing user identity and authentication. It provides endpoints for user registration, and profile management.

## Architecture

```mermaid
C4Container
    title Container Diagram for the Identity API

    System(client_app, "Client Application", "e.g., identity_frontend, making user management requests.")

    System_Boundary(aws_identity, "Identity Account (AWS)") {
        Container(api_gateway, "API Gateway", "AWS API Gateway", "Custom domain: v1-api.account.wellcomecollection.org")
        Container(identity_api_lambda, "Identity API", "AWS Lambda", "Handles user management logic.")
    }

    System_Boundary(public_internet, "Public Internet") {
        System_Ext(sierra, "Sierra", "3rd Party Cloud-Hosted Library Management System", "The system of record for library members.")
    }

    Rel(client_app, api_gateway, "Requests user data from", "HTTPS")
    Rel(api_gateway, identity_api_lambda, "Routes requests to")
    Rel(identity_api_lambda, sierra, "Authenticates users against", "Custom Database Integration")

    UpdateLayoutConfig($c4ShapeInRow="2", $c4BoundaryInRow="2")
```

## Accounts

- [identity](../../aws_accounts.md#identity)

## Repositories

See the following repositories for more details on the services described above:

- [wellcomecollection/identity](https://github.com/wellcomecollection/identity)
