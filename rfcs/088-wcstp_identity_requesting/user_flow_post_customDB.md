# User Flows — After Custom DB Script Removal (Auth0 Native DB)

These diagrams show the same user flows as `user_flows.md`, but with Auth0 as the native credential store. No Custom DB scripts are involved. Sierra is still used for patron profile/hold data during the transition period (until Folio replaces it).

## Registration

```mermaid
sequenceDiagram
    participant User
    participant Auth0UL as Auth0 Universal Login
    participant Auth0 as Auth0 Tenant
    participant Action as Action: create_patron
    participant Sierra
    participant ClaimsAction as Action: add_custom_claims

    User->>Auth0UL: Sign up (email, password, first name, last name, T&Cs ✓)
    Auth0UL->>Auth0: Create user in native DB
    Auth0->>Auth0: Store credentials (bcrypt hash)
    Auth0->>Auth0: Store given_name, family_name in user profile
    Auth0->>Auth0: Store T&Cs acceptance in user_metadata

    Note over Auth0,Action: Post-login trigger (first login after signup)
    Auth0->>Action: onExecutePostLogin(event, api)
    Action->>Action: Check app_metadata.sierra_patron_id missing?
    Action->>Sierra: createPatron(firstName, lastName, email)
    alt Email already exists in Sierra
        Sierra-->>Action: UserAlreadyExists
        Action->>Action: Look up existing patron by email
        Sierra-->>Action: patronRecord
        Action->>Auth0: Set app_metadata (sierra_patron_id, barcode, role)
    else Success
        Sierra-->>Action: recordNumber
        Action->>Sierra: updatePatron(recordNumber, barcode=recordNumber)
        Sierra-->>Action: OK
        Action->>Auth0: Set app_metadata (sierra_patron_id, barcode, role)
    end

    Auth0->>ClaimsAction: onExecutePostLogin(event, api)
    ClaimsAction->>ClaimsAction: Add barcode + role claims to ID token

    Auth0-->>User: Tokens issued, logged in
```

**Key differences from today:**
- Single form: all data collected upfront (no redirect to separate registration page)
- No temp names — patron created with real data
- No `create` DB script — Auth0 stores credentials natively
- No orphaned patrons from abandoned signups (Sierra patron only created after Auth0 user exists)
- No forced logout to refresh name (Auth0 native DB allows direct profile updates)
- Sierra patron creation is idempotent: check `app_metadata.sierra_patron_id` before creating

**Note:** The `create_patron` action replaces both the old `create` DB script and the `redirect_to_full_registration` action. If the 20s action timeout is a concern, patron creation could alternatively happen via the Identity API called from a post-login redirect — but the action approach is simpler.

## Login

```mermaid
sequenceDiagram
    participant User
    participant Auth0UL as Auth0 Universal Login
    participant Auth0 as Auth0 Tenant
    participant ClaimsAction as Action: add_custom_claims

    User->>Auth0UL: Sign in (email + password)
    Auth0UL->>Auth0: Login request
    Auth0->>Auth0: Validate credentials against native store (bcrypt)

    alt Invalid credentials
        Auth0-->>User: "Wrong email or password"
    else Valid credentials
        Auth0->>ClaimsAction: onExecutePostLogin(event, api)
        ClaimsAction->>ClaimsAction: Add barcode + role claims to ID token
        Auth0-->>User: Tokens issued
    end
```

**Key differences from today:**
- No `login` DB script — Auth0 validates against its own store
- No Sierra calls at all during login
- No implicit email verification logic for pre-2022 patrons (handled during migration)
- Significantly faster login (no external API calls)

## Get User

```mermaid
sequenceDiagram
    participant Auth0 as Auth0 Tenant

    Note over Auth0: Triggered internally for password reset,<br/>email verification, silent auth, etc.

    Auth0->>Auth0: Look up user in native store
    Auth0->>Auth0: Return user profile
```

**Key differences from today:**
- No `get_user` DB script — Auth0 reads from its own store
- No Sierra dependency for user lookups
- No risk of "duplicate users" error (Auth0 enforces unique email natively)

## Change Password

```mermaid
sequenceDiagram
    participant User
    participant Webapp as Identity Webapp
    participant API as Identity API
    participant Auth0 as Auth0 Tenant

    User->>Webapp: Change password (old + new)
    Webapp->>API: PUT /users/:id/password {password, newPassword}
    API->>Auth0: POST /oauth/token (password grant, old password)
    Auth0->>Auth0: Validate old password against native store
    Auth0-->>API: Valid / Invalid

    alt Invalid old password
        API-->>User: "Current password is incorrect"
    else Valid
        API->>Auth0: Management API PATCH /users/:id {password: newPassword}
        Auth0->>Auth0: Validate against password policy
        alt Password too weak
            Auth0-->>API: PasswordStrengthError
            API-->>User: "Please use a stronger password"
        else Success
            Auth0->>Auth0: Store new bcrypt hash
            Auth0-->>API: 200
            API-->>User: Password updated
        end
    end
```

**Key differences from today:**
- No `change_password` DB script — Auth0 updates its own store
- No Sierra PIN update (Sierra credentials are stale/irrelevant)
- Password policy enforced by Auth0 config only (min 8 chars, no personal info, dictionary check) — no Sierra PIN rules (trivial, too long)
- No 30-character PIN truncation
- Identity API code is unchanged

## Change Email

```mermaid
sequenceDiagram
    participant User
    participant Webapp as Identity Webapp
    participant API as Identity API
    participant Auth0 as Auth0 Tenant

    User->>Webapp: Change email (current password + new email)
    Webapp->>API: PUT /users/:id {password, email: newEmail}
    API->>Auth0: POST /oauth/token (password grant, current password)
    Auth0-->>API: Valid

    API->>Auth0: Management API PATCH /users/:id {email: newEmail, verify_email: true}
    alt Email already exists
        Auth0-->>API: 400 "email already exists"
        API-->>User: "A user with this email already exists"
    else Success
        Auth0->>Auth0: Update email, mark unverified
        Auth0->>User: Verification email sent
        Auth0-->>API: 200 (updated user)
        API-->>User: Email updated
    end
```

**Key differences from today:**
- No `change_email` DB script — Auth0 updates its own store
- No Sierra email update (Sierra is no longer the source of truth for email)
- Duplicate email detection handled natively by Auth0
- Identity API code is unchanged

## Verify Email

```mermaid
sequenceDiagram
    participant User
    participant Auth0 as Auth0 Tenant

    User->>Auth0: Click verification link in email
    Auth0->>Auth0: Mark email_verified = true
```

**Key differences from today:**
- No `verify` DB script — Auth0 handles verification natively
- No Sierra call to mark patron email verified
- Single atomic operation

## Delete

```mermaid
sequenceDiagram
    participant Tracker as Patron Deletion Tracker
    participant Auth0 as Auth0 Tenant
    participant Sierra

    Note over Tracker: Daily scheduled job (unchanged)

    Tracker->>Sierra: Query for patrons deleted yesterday
    Sierra-->>Tracker: List of deleted patron IDs
    loop For each deleted patron
        Tracker->>Auth0: Management API DELETE /users/:id
        Auth0->>Auth0: Remove user from native store
    end
```

**Key differences from today:**
- No `delete` DB script (was already a no-op)
- Patron Deletion Tracker continues to run unchanged
- Direction remains Sierra → Auth0 during transition (reverses to Auth0/Folio → Sierra once Sierra is being retired)

## Validate Password (via Identity API)

```mermaid
sequenceDiagram
    participant User
    participant Webapp as Identity Webapp
    participant API as Identity API
    participant Auth0 as Auth0 Tenant

    Note over User,Webapp: Used as a "confirm identity" check<br/>before sensitive operations

    User->>Webapp: Confirm current password
    Webapp->>API: POST /users/:id/validate {password}
    API->>Auth0: POST /oauth/token (password grant)
    Auth0->>Auth0: Validate against native store
    Auth0-->>API: 200 / 401
    API-->>User: 200 OK / Error
```

**Key differences from today:**
- No `login` DB script triggered — Auth0 validates natively
- No Sierra call
- Identity API code is unchanged

---

## Summary of changes

| Flow | Before (Custom DB) | After (Native DB) | Code changes needed |
|------|-------------------|-------------------|-------------------|
| Registration | `create` script → Sierra, then redirect to form | Single form, post-login action → Sierra | New action, remove `redirect_to_full_registration`, remove `/registration` endpoint |
| Login | `login` script → Sierra | Auth0 native validation | None |
| Get user | `get_user` script → Sierra | Auth0 native lookup | None |
| Change password | `change_password` script → Sierra | Auth0 native update | None (Identity API unchanged) |
| Change email | `change_email` script → Sierra | Auth0 native update | None (Identity API unchanged) |
| Verify email | `verify` script → Sierra | Auth0 native verification | None |
| Delete | `delete` script (no-op) | No script needed | None (Deletion Tracker unchanged) |
| Validate password | `login` script → Sierra | Auth0 native validation | None (Identity API unchanged) |