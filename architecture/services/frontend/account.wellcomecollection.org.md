# account.wellcomecollection.org

This service handles user registration and login and is managed by Auth0. It integrates with the Sierra library management system for user authentication. Successful logins redirect to the main website, and will set a cookie to indicate the user is logged in.

## Architecture

```mermaid
C4Container
    title Container Diagram for account.wellcomecollection.org

    Person(user, "Library Member", "A user of Wellcome Collection's digital services.")

    System_Boundary(auth0_platform, "Auth0 Platform") {
        Container(universal_login, "Universal Login Page", "Auth0 Hosted", "Handles login, sign-up, and forgot password flows.")
    }
    
    System_Boundary(public_internet, "Public Internet") {
        System_Ext(sierra, "Sierra", "3rd Party Cloud-Hosted Library Management System", "The system of record for library members.")
    }

    Rel(user, universal_login, "Uses", "HTTPS")
    Rel(universal_login, sierra, "Authenticates users against", "Custom Database Integration")
    
    UpdateLayoutConfig($c4ShapeInRow="1", $c4BoundaryInRow="1")
```

## Accounts

- [identity](../../aws_accounts.md#identity)

## Repositories

See the following repositories for more details on the services described above:

- [wellcomecollection/wellcomecollection.org](https://github.com/wellcomecollection/wellcomecollection.org)
- [wellcomecollection/identity](https://github.com/wellcomecollection/identity)
