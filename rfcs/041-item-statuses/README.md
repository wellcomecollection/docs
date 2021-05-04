# RFC 041: Statuses in the items API

As part of the [requesting API](../039-requesting-api-design), we need to present an item status.
We already have a model that we'll use:

```json
"status": {
  "id" : "available",
  "label" : "Available",
  "type": "ItemStatus"
}
```

but we need to decide what value it can take.

This RFC proposes a set of values that we will present through this API.



## Guiding principles

1.  **We should not assume requests are sent to a particular service.**

    Although the initial implementation will be making requests for items in Sierra, we may add support for requesting from other systems in a future update.
    We should not assume the use of Sierra, or of Sierra item statuses.

2.  **A user's list of holds is private.**

    Alice should not be able to find out what items Bob has placed on hold, and vice versa.

3.  **The status information will be publicly visible, and displayed on the works page.**

    For consistency, we should use the same terminology as will be used on the works page.
    We should assume users will see these statuses, and not expose information about the library workings.
