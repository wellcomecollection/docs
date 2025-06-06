# RFC 074: Offsite requesting

This RFC outlines the plan for enabling online requesting of items that are held offsite, with a phased approach to accommodate both onsite and offsite viewing.

**Last modified:** 2024-04-23T11:57:13+01:00

## Context

We want library patrons to be able to make online requests for items that are held offsite. Some of these items will be recalled to Wellcome Collection for viewing, whereas some will require patrons to travel elsewhere to view. 

While we already have an online requesting process, this currently assumes that items are held onsite and as such follow a "hardcoded" requesting schedule: they are available to view according to the venue opening times and the time at which the request is made. 

A requesting process for offsite requesting must include affordances for (a) an availability schedule based on the item location and (b) information for the patron regarding items that are to be viewed offsite. These can form two sequential work phases: the first enabling offsite requesting for items that will be viewed onsite, and the second for those that will be viewed offsite.

#### API Model

Currently, works have items with locations. Items that are currently requestable online have locations that look like this:

```json
{
  "label": "Closed stores",
  "accessConditions": [
    {
      "method": {
        "id": "online-request",
        "label": "Online request",
        "type": "AccessMethod"
      },
      "status": {
        "id": "open",
        "label": "Open",
        "type": "AccessStatus"
      },
      "shelfmark": "<string>",
      "locationType": {
        "id": "closed-stores",
        "label": "Closed stores",
        "type": "LocationType"
      },
      "type": "PhysicalLocation"
    }
  ]
}
```

We can see from this that there are 3 controlled fields:

- Location type: could also be open shelves, on exhibition, on order, etc.
- Access status: this refers to intellectual/legal access restrictions.
- Access method: could also be manual request, view online, not requestable, etc.

Now we consider how we might represent offsite items using this model:

- Location type seems initially appealing; we could create a new "offsite stores" or similar location type. However, this doesn't tell us anything about the actual availability/location of that item - and aren't offsite stores just a type of closed stores? What about the difference between items that are *viewed* on/off-site?
- Access status is not relevant (and needs to exist in full for offsite items)
- Access method is the most literal, but "online request" already covers what we want to do. But what if that is a hint towards a scalable solution? Items that are held offsite but viewed onsite and are requested online can look exactly like the above, and items that are held and viewed offsite could have a new access method like "Offsite online request" etc.
- Furthermore, user-facing information about item location (contextualising longer order times and offering an indication to experienced researchers about items that need to be viewed offsite) could be stored in the shelfmark string or in the label (which is currently "Closed stores" for all closed-stores items.) 

Following this logic, we propose the following:

### Phase 1: Requesting for items held offsite, viewed onsite

- No changes to the model (and therefore pipeline behaviour) other than ensuring that items with an offsite location code are online-requestable.
- Items API to use data direct from Sierra (as it does currently) to discriminate offsite items and to return appropriate availability slots.
- Possible changes to location label and/or shelfmarks for offsite items (confirm with library colleagues).
- Changes to frontend requesting copy to allow for variable requesting schedule.

This means that there will be no *API-consumer-facing indication* that an item is held offsite, other than potentially a reflection of this in the location label (which would not be reliably machine-readable). This leaves the items API free to determine the availability of an offsite item (eg its increased lead time over held-onsite items) based on the location data it receives directly from Sierra.

**Questions**

- Is it really OK to have no machine-readable method for discriminating offsite items in our APIs? Will we end up writing hacks, stuff like `if (location.label.includes("offsite")) { displaySomeOtherUIVariant(); }`?

### Phase 2: Requesting for items held offsite, viewed offsite

- Addition of a new access method for items that are requested online to be viewed offsite
- Items API to discriminate using Sierra data as in phase 1
- User flow in frontend app and/or APIs to be determined using the new access method	

For these items there will be an API-consumer-facing indication that the item is to be viewed offsite, in the form of the access method - but this will not give any details about the specifics of that location. As with Phase 1, the specifics will be determined by business logic held in the Items API, which has access to the Sierra data.