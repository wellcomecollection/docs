# RFC 034: Modelling Locations in the Catalogue API

As part of upcoming work to add holdings, online resources, and more detailed journal information to the Catalogue API, we need to expand the range of locations which are presented by the API.

Additionally, we want to model locations in a way that can be reused by the requesting service.
We don't want to have two entirely different location models in the Catalogue and Requesting APIs.

This RFC describes the types of location we want to model, and proposes how they will be returned in the catalogue API.

**Current status:** this RFC outlines the problem, by describing the types of location we want to model.
Please check if the information contained is accurate and complete.



## The existing model

The Catalogue API contains *Works*, and Works contain *Items*.
In turn, each Item can have *Locations*, which tell the user how they can get the item.
We're not planning to change the Item model; we want to consider if the Location model is fit for purpose.

<details>
<summary>Examples of physical and digital locations in the existing model</summary>

Papers in the closed stores (a physical location):

```json
{
  "locationType": {
    "id": "scmac",
    "label": "Closed stores Arch. & MSS",
    "type": "LocationType"
  },
  "label": "Closed stores Arch. & MSS",
  "accessConditions": [
    {
      "status": {
        "id": "open",
        "label": "Open",
        "type": "AccessStatus"
      },
      "terms": "The papers are available subject to the usual conditions of access to Archives and Manuscripts material.",
      "type": "AccessCondition"
    }
  ],
  "type": "PhysicalLocation"
}
```

A single Miro image (a IIIF image location):

```json
{
  "locationType": {
    "id": "iiif-image",
    "label": "IIIF Image API",
    "type": "LocationType"
  },
  "url": "https://iiif.wellcomecollection.org/image/A0000681.jpg/info.json",
  "credit": "Royal Veterinary College",
  "license": {
    "id": "cc-by-nc",
    "label": "Attribution-NonCommercial 4.0 International (CC BY-NC 4.0)",
    "url": "https://creativecommons.org/licenses/by-nc/4.0/",
    "type": "License"
  },
  "accessConditions": [],
  "type": "DigitalLocation"
}
```

A digitised item (a IIIF Presentation location):

```json
{
  "locationType": {
    "id": "iiif-presentation",
    "label": "IIIF Presentation API",
    "type": "LocationType"
  },
  "url": "https://wellcomelibrary.org/iiif/b22398752/manifest",
  "license": {
    "id": "pdm",
    "label": "Public Domain Mark",
    "url": "https://creativecommons.org/share-your-work/public-domain/pdm/",
    "type": "License"
  },
  "accessConditions": [
    {
      "status": {
        "id": "open",
        "label": "Open",
        "type": "AccessStatus"
      },
      "type": "AccessCondition"
    }
  ],
  "type": "DigitalLocation"
}
```

</details>



## What should a location tell you?

When somebody looks at an item, here's what they want to know about location:

*   **Am I allowed to see it?**
    This is encoded by the *access conditions* field, which includes an *access status* (drawn from a fixed vocabulary: open, closed, requires-permission, etc.) and an *access description* (free-text, written by cataloguers).

*   **If I'm allowed to see it, where can I find it?**
    For example: where it sits on the physical shelves within the library, or a particular URL, or a IIIF resource.

*   **If I'm allowed to see it, can I use it?**
    This is the *license* on the item.

    Note: Our current model only supports a license on digital locations.
    Is this correct, or do we need to support licenses on physical locations also?

We need to support filtering and aggregating by location.
For example, users should be able to find all the material that's openly available online (if they're working remotely), or all the material in the library (if they're in the building).



## What locations do we need to support?

These are the types of location our model needs to support:

*   **Open shelves.**

    This should include a *shelf location* (e.g. History of Medicine Collection) and a *shelfmark* (e.g. TW.AL) so that a user can find it.

*   **Closed stores.**

    Although the MARC records include a shelf location and a shelfmark, the Collections team would prefer this not to be exposed publicly.

    Do we need to expose this information for the requesting service?

    -   We don't need to expose the full detail of our closed stores, but do we want to expose the difference between onsite/offsite?
        The latter will take longer to retrieve, and may require a manual request to Library Enquiries.
        Is this something that should be exposed by the Catalogue API, or only by the Requesting service?

*   **A standalone IIIF image.**

    For example, the Miro images.
    This should include a *URL* (to the IIIF resource), and optionally a *license* and *credit line*.

*   **A IIIF presentation manifest.**

    For example, the digitised books.
    As with a standalone IIIF image, this should include a *URL*, and optionally a *license* and *credit line*.

*   **External websites or URLs.**

    For example, a journal with online access.
    This should include a *URL* (to access the resource), and optional *link text* (e.g. View this e-book).

    If it's a journal to which Wellcome subscribes, access is IP-restricted.
    This requires using a proxy URL, which is of the form `https://{proxyname}.catalogue.wellcomelibrary.org`.
    How is the journal accessed?

    *   If users are in our building, they don't need to log in
    *   If users are off-site, they need to log in to their Library account to use the proxy

*   **On exhibition.**

    This should include the *name of the exhibition* and the *due date* when the item will be returning to the library.

    For an example of this, see <https://wellcomecollection.org/works/azrhju85>.
    There might be a free-form text description that lives separately in the "notes" field.

There are a number of other infrequently used location codes (e.g. "offsite", "at digitisation", "Rare Materials Room") that we currently present in the API.
We'll need to continue to support these in some form.

(See included spreadsheets that tally the locations from a recent snapshot.)



## The existing transformation

This section explains how we create locations in the current version of the Catalogue API, as of commit 885a26d in the catalogue repo.

Miro images:

*   We create a DigitalLocation with location type `iiif-image`.
*   The URL points to `iiif.wellcomecollection.org`, and uses the Miro image number (from the `image_no_calc` field in the Miro record)
*   The credit line is based on the value in the `image_credit_line` field
*   The license is based on the value in the `image_use_restrictions` field

Calm records:

*   We create a PhysicalLocation with location type `scmac` (Closed stores Arch. & MSS)
*   We create access conditions based on the `AccessStatus` and `AccessConditions` fields.
    Additionally, we use the `ClosedUntil` and `UserDate1` fields to determine when a given set of access conditions end (if appropriate).

Digitised items from METS:

*   We create a digital location with location type `iiif-presentation`.
*   The URL points to the IIIF manifest on `wellcomelibrary.org`.
*   The license, access status and access conditions are drawn from the METS XML:

    ```xml
    <mods:accessCondition type="dz">CC-BY-NC</mods:accessCondition>
    <mods:accessCondition type="status">Open</mods:accessCondition>
    <mods:accessCondition type="usage">Some terms</mods:accessCondition>
    ```

Bibs and items from Sierra:

*   We create a physical location whose location type comes from the `"location"` field on the Sierra API response for the item.
*   The access conditions are based on the varfields with MARC tag 506:

    -   If the first indicator is 0, the access status is "Open"
    -   We look at subfield $a for a free-text description of the access conditions
    -   We look at subfield $f for the standardised open/closed/restricted terminology

    Note: if these three values are inconsistent, we do not set an AccessStatus from our controlled vocabulary.



## Proposed changes

*   The AccessStatus model in the Catalogue API (which draws from a fixed vocabulary) should reflect the access statuses in section 12 of the [Wellcome Collection Access Policy](https://wellcomecollection.org/pages/Wvmu3yAAAIUQ4C7F#access-policy).

    Currently it has: `Open`, `OpenWithAdvisory`, `Restricted`, `Unavailable`, `Closed`, `LicensedResources` and `PermissionRequired`.

    We should add:

    -   `ByAppointment`, which the current implementation of the Catalogue API treats as synonymous with `Restricted`
    -   `TemporarilyUnavailable`, so we can distinguish between, say, material that's being digitised and will be available later, and material that has been de-accessioned and will never become available.
