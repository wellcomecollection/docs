## Identity & Requesting discovery


#### Problem outline

As part of a Systems Transformation Program, Sierra is being replaced by Folio (they're both Library Management Sytems/LMS)
Currently Sierra holds patrons' (library users) data such name, email address, whether they are allowed to place holds on library items, any holds they have placed on library items (among other things? TBC). Crucially Sierra also keeps the patron's login credentials, ie. email and account password.
Folio, OTOH, does all of this but does not authenticate patrons; it doesn't hold patron credentials and offers no mechanism to validate them in order to authenticate or authorise patron requests.
In the middle of this we use Auth0 to generate and sign auth tokens, then validate these tokens on subsequent patron requests. 
See README.md for overview of the Identity services, including identity API, authorizer lambda, and Auth0 DB scripts/integration


#### Discussion points

- Folio can and most likely will store and manage hold data, eg. GET what items a patron has requested, POST a new hold request. What are Auth0 capabilities in terms of user/patron profile data storage and management? Can we migrate the authentication layer out of the LMS and into Auth0? 
- If we can, what would be a sensible way to migrate credentials and authentication out of the LMS and into Auth0?


---


# User Flows — Custom DB Script Usage

## Registration (create)

```mermaid
sequenceDiagram
    participant User
    participant Auth0UL as Auth0 Universal Login
    participant Auth0 as Auth0 Tenant
    participant CreateScript as DB Script: create
    participant Sierra
    participant Action as Action: redirect_to_full_registration
    participant Webapp as Identity Webapp
    participant API as Identity API

    User->>Auth0UL: Sign up (email + password)
    Auth0UL->>Auth0: Create user request
    Auth0->>CreateScript: create(user)
    CreateScript->>Sierra: createPatron(tempLastName, tempFirstName, email, password)
    alt Email already exists
        Sierra-->>CreateScript: UserAlreadyExists
        CreateScript-->>Auth0: ValidationError("user_exists")
        Auth0-->>User: "A user with this email already exists"
    else PIN too trivial / too long
        Sierra-->>CreateScript: PIN validation error
        CreateScript-->>Auth0: ValidationError (password message)
        Auth0-->>User: "Please use a more complex/shorter password"
    else Success
        Sierra-->>CreateScript: recordNumber
        CreateScript->>Sierra: updatePatron(recordNumber, barcode=recordNumber)
        Sierra-->>CreateScript: OK
        CreateScript-->>Auth0: User created
    end

    Auth0->>Action: Post-login trigger
    Action->>Action: Check given_name/family_name for temp prefix
    Action->>User: Redirect to /registration with session_token

    User->>Webapp: Fill in first name, last name, accept T&Cs
    Webapp->>API: PUT /users/:id/registration {firstName, lastName}
    API->>Sierra: getPatronRecordByRecordNumber (verify temp names)
    API->>Sierra: updatePatron (set real name)
    Sierra-->>API: OK
    API-->>Webapp: 204
    Webapp->>Auth0: Redirect to /continue
    Auth0-->>User: Issue tokens, logged in
```

## Login (login)

```mermaid
sequenceDiagram
    participant User
    participant Auth0UL as Auth0 Universal Login
    participant Auth0 as Auth0 Tenant
    participant LoginScript as DB Script: login
    participant Sierra

    User->>Auth0UL: Sign in (email + password)
    Auth0UL->>Auth0: Login request
    Auth0->>LoginScript: login(email, password)
    LoginScript->>Sierra: getPatronRecordByEmail(email)
    alt Patron not found
        Sierra-->>LoginScript: NotFound
        LoginScript-->>Auth0: WrongUsernameOrPasswordError
        Auth0-->>User: "We don't recognise the email and/or password"
    else Patron found
        Sierra-->>LoginScript: patronRecord
        LoginScript->>Sierra: validateCredentials(barcode, password)
        alt Invalid credentials
            Sierra-->>LoginScript: Failure
            LoginScript-->>Auth0: WrongUsernameOrPasswordError
            Auth0-->>User: "We don't recognise the email and/or password"
        else Valid credentials
            Sierra-->>LoginScript: Success
            LoginScript-->>Auth0: User profile (with app_metadata: barcode, role)
            Auth0-->>User: Tokens issued
        end
    end
```

## Get User (get_user)

```mermaid
sequenceDiagram
    participant Auth0 as Auth0 Tenant
    participant GetUserScript as DB Script: get_user
    participant Sierra

    Note over Auth0: Triggered when Auth0 needs to<br/>look up a user (e.g. password reset,<br/>email verification, silent auth)

    Auth0->>GetUserScript: get_user(email)
    GetUserScript->>Sierra: getPatronRecordByEmail(email)
    alt Patron found
        Sierra-->>GetUserScript: patronRecord
        GetUserScript-->>Auth0: User profile {user_id, email, name, app_metadata}
    else Not found
        Sierra-->>GetUserScript: NotFound
        GetUserScript-->>Auth0: undefined (user doesn't exist)
    else Duplicate users
        Sierra-->>GetUserScript: DuplicateUsers
        GetUserScript-->>Auth0: ValidationError (contact Library Enquiries)
    end
```

## Change Password (change_password)

```mermaid
sequenceDiagram
    participant User
    participant Webapp as Identity Webapp
    participant API as Identity API
    participant Auth0 as Auth0 Tenant
    participant script as DB Script: change_password
    participant Sierra

    User->>Webapp: Change password (old + new)
    Webapp->>API: PUT /users/:id/password {password, newPassword}
    API->>Auth0: validateCredentials (password grant, old password)
    Auth0->>script: login script validates old password against Sierra
    script-->>Auth0: Valid
    Auth0-->>API: OK
    API->>Auth0: Management API PATCH /users/:id {password: newPassword}
    Auth0->>script: change_password(email, newPassword)
    script->>Sierra: getPatronRecordByEmail → recordNumber
    script->>Sierra: updatePatron(recordNumber, {pin: truncate(newPassword, 30)})
    alt PIN trivial pattern
        Sierra-->>script: PasswordTooWeak
        script-->>Auth0: WrongUsernameOrPasswordError
        Auth0-->>API: Error
        API-->>User: "Passwords can't contain repeated characters"
    else Success
        Sierra-->>script: OK
        script-->>Auth0: true
        Auth0-->>API: 200
        API-->>User: Password updated
    end
```

## Change Email (change_email)

```mermaid
sequenceDiagram
    participant User
    participant Webapp as Identity Webapp
    participant API as Identity API
    participant Auth0 as Auth0 Tenant
    participant script as DB Script: change_email
    participant Sierra

    User->>Webapp: Change email (current password + new email)
    Webapp->>API: PUT /users/:id {password, email: newEmail}
    API->>Auth0: validateCredentials (password grant, current password)
    Auth0-->>API: Valid
    API->>Auth0: Management API PATCH /users/:id {email: newEmail, verify_email: true}
    Auth0->>script: change_email(oldEmail, newEmail, verified=false)
    script->>Sierra: getPatronRecordByEmail(oldEmail) → recordNumber
    script->>Sierra: updatePatronEmail(recordNumber, newEmail, verified)
    Sierra-->>script: OK
    script-->>Auth0: true
    Auth0-->>API: 200 (updated user)
    API-->>User: Email updated, verification email sent
```

## Verify Email (verify)

```mermaid
sequenceDiagram
    participant User
    participant Auth0 as Auth0 Tenant
    participant VerifyScript as DB Script: verify
    participant Sierra

    User->>Auth0: Click verification link in email
    Auth0->>VerifyScript: verify(email)
    VerifyScript->>Sierra: getPatronRecordByEmail(email) → recordNumber
    VerifyScript->>Sierra: markPatronEmailVerified(recordNumber)
    Sierra-->>VerifyScript: Updated patronRecord
    VerifyScript-->>Auth0: User profile (verified)
    Auth0->>Auth0: Mark email_verified = true
```

## Delete (delete)

```mermaid
sequenceDiagram
    participant Auth0 as Auth0 Tenant
    participant DeleteScript as DB Script: delete
    participant Sierra

    Note over Auth0: Triggered when a user is<br/>deleted from Auth0

    Auth0->>DeleteScript: delete(id)
    DeleteScript->>DeleteScript: console.log("User deleted: ", id)
    Note over DeleteScript,Sierra: No-op: does NOT delete from Sierra<br/>(deletion handled separately by Patron Deletion Tracker)
```

## Validate Password (via Identity API)

```mermaid
sequenceDiagram
    participant User
    participant Webapp as Identity Webapp
    participant API as Identity API
    participant Auth0 as Auth0 Tenant
    participant LoginScript as DB Script: login
    participant Sierra

    Note over User,Webapp: Used as a "confirm identity" check<br/>before sensitive operations

    User->>Webapp: Confirm current password
    Webapp->>API: POST /users/:id/validate {password}
    API->>Auth0: POST /oauth/token (password grant)
    Auth0->>LoginScript: login(email, password)
    LoginScript->>Sierra: validateCredentials(barcode, password)
    Sierra-->>LoginScript: Success/Failure
    LoginScript-->>Auth0: User profile / Error
    Auth0-->>API: 200 / 401
    API-->>User: 200 OK / Error
```
