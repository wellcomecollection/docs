# RFC 034: Modelling Locations in the Catalogue API

As part of upcoming work to add holdings, online resources, and more detailed journal information to the Catalogue API, we need to expand the range of locations which are presented by the API.
Additionally, we want to model locations in a format suitable for the requesting service.

This RFC describes the types of location we want to model, and proposes how they will be returned in the catalogue API.

**Current status:** this RFC outlines the problem, by describing the types of location we want to model.
Please check if the information contained is accurate and complete.



## The existing approach

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

    -   Can something be requested faster if it's stored on-site?
    -   Does the requesting service need to know the location of something when it tells Sierra "please ask somebody to fetch this item", or can it just provide Sierra the item ID?

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
