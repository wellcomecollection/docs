# requesting_api

The Requesting API is responsible for managing user requests to view items in the Wellcome Collection. It provides endpoints for submitting and tracking requests, and is authorized by the Identity API.

## Architecture

```mermaid
C4Container
    title Container Diagram for the Requesting API

    System(client_app, "Client Application", "e.g., identity_frontend, making item requests.")

    System_Boundary(aws_identity, "Identity Account (AWS)") {
        Container(api_gateway, "API Gateway", "AWS API Gateway", "Custom domain: v1-api.account.wellcomecollection.org")
        Container(requesting_api_lambda, "Requesting API", "AWS Lambda", "Handles item request logic.")
        Container(identity_api_lambda, "Identity API", "AWS Lambda", "Handles user authentication.")
    }

    System_Boundary(public_internet, "Public Internet") {
        System_Ext(sierra, "Sierra", "3rd Party Cloud-Hosted Library Management System", "The system of record for library members.")
    }

    Rel(client_app, api_gateway, "Submits requests to", "HTTPS")
    Rel(api_gateway, requesting_api_lambda, "Routes requests to")
    Rel(requesting_api_lambda, identity_api_lambda, "Authorizes requests with")
    Rel(requesting_api_lambda, sierra, "Places holds on items in")

    UpdateLayoutConfig($c4ShapeInRow="2", $c4BoundaryInRow="2")
```

## Accounts

- [identity](../../aws_accounts.md#identity)

## Repositories

See the following repositories for more details on the services described above:

- [wellcomecollection/identity](https://github.com/wellcomecollection/identity) 
- [wellcomecollection/catalogue-api](https://github.com/wellcomecollection/catalogue-api)
