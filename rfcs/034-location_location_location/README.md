# RFC 034: Modelling Locations in the Catalogue API

As part of upcoming work to add holdings, online resources, and more detailed journal information to the Catalogue API, we need to expand the range of locations which are presented by the API.

Additionally, we want to model locations in a way that can be reused by the requesting service.
We don't want to have two entirely different location models in the Catalogue and Requesting APIs.

This RFC describes the types of location we want to model, and proposes how they will be returned in the catalogue API.

**Current status:** this RFC describes the sort of Location data we want to model, and some proposed changes for:

*   Adding shelf location and shelfmark data
*   Creating a smaller set of LocationTypes specifically for the Catalogue API, rather than repeating the Sierra location codes



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

We need to support filtering and aggregating by location.
For example, users should be able to find all the material that's openly available online (if they're working remotely), or all the material in the library (if they're in the building).



## What locations do we need to support?

These are the types of location our model needs to support:

*   **Open shelves.**

    This should include a *shelf location* (e.g. History of Medicine Collection) and a *shelfmark* (e.g. TW.AL) so that a user can find it.

*   **Closed stores.**

    Although the MARC records include a shelf location and a shelfmark, the Collections team would prefer this not to be exposed publicly.

    Note:

    -   Material kept offsite takes longer to retrieve, and may require a manual request to Library Enquiries (although that might change in future).
        The catalogue API doesn't care about this distinction, so material in closed stores onsite or offsite will get the same location type.
        If we need to expose this (e.g. to set expectations about retrieval times), we can revisit this when we work on requesting.

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

    Note: if these three values are inconsistent, the code will not set an AccessStatus from our controlled vocabulary.
    This is protection against future inconsistency; there are no known examples.



## Proposed changes

*   The AccessStatus model in the Catalogue API (which draws from a fixed vocabulary) should reflect the access statuses in section 12 of the [Wellcome Collection Access Policy](https://wellcomecollection.org/pages/Wvmu3yAAAIUQ4C7F#access-policy).

    Currently it has: `Open`, `OpenWithAdvisory`, `Restricted`, `Unavailable`, `Closed`, `LicensedResources` and `PermissionRequired`.

    We should add:

    -   `ByAppointment`, which the current implementation of the Catalogue API treats as synonymous with `Restricted`
    -   `TemporarilyUnavailable`, so we can distinguish between, say, material that's being digitised and will be available later, and material that has been de-accessioned and will never become available.

*   Currently the `"license"` field only appears on digital locations.

    Although we don't have any examples of it on physical locations yet, a license is sufficiently core that we'll make it part of the PhysicalLocation model.

*   We will add an optional `"link_text"` field to digital locations.

*   Currently the `LocationType` model uses the full range of location codes supported by Sierra.

    We will replace this with a controlled set of types (similar to AccessStatus), and the Sierra transformer will make a best-effort guess to map the Sierra location code/label onto one of these types.
    If it is unable to map the Sierra location code to one of these types, it will skip adding a location to the item.

    This will include a warning log, so the developers can know if/when new locationTypes have been added and are being skipped by the transformer.

    This is an initial suggestion for the list of types:

    *   ClosedStores
    *   OpenShelves
    *   IIIFPresentationAPI
    *   IIIFImageAPI
    *   OnExhibition
    *   OnlineResource
    *   Conservation

    <details>
    <summary>Proposed heuristic for matching Sierra item locations to controlled types</summary>

    For Sierra items, the API returns both a location *code* (e.g. semsa) and a location *name* (e..g Closed Stores EPB MSL A).
    We will do a case-insensitive match on the location name to map to the controlled type.

    <table>
      <tr><th>New LocationType</th><th>Sierra location names that match:</th></tr>
      <tr>
        <td>ClosedStores</td>
        <td>
          archives & mss well.coll<br/>
          by appointment<br/>
          closed stores<br/>
          early printed books<br/>
          iconographic collection<br/>
          offsite<br/>
          unrequestable
        </td>
      </tr>
      <tr>
        <td>OpenShelves</td>
        <td>
          biographies<br/>
          folios<br/>
          history of medicine<br/>
          journals<br/>
          medical collection<br/>
          medicine & society collection<br/>
          open shelves<br/>
          quick ref collection<br/>
          quick ref. collection<br/>
          rare materials room<br/>
          student coll
        </td>
      </tr>
      <tr>
        <td>OnExhibition</td>
        <td>on exhibition</td>
      </tr>
      <tr>
        <td>Conservation</td>
        <td>conservation</td>
      </tr>
    </table>

    This heuristic allows us to create locations in our controlled type for **94.7% of all items**.

    Some Sierra items have a location like "as above" or "bound in above".
    For these, we could apply an additional heuristic: if every other item has the same location (e.g. every other item is ClosedStores), then we give this item the same location.
    Otherwise, we skip adding a Location to that item until we can come back and write more sophisticated logic (e.g. matching on shelfmark).

    This additional heuristic would allow us to create locations in our controlled type for **99.97% of all items**.

    The unmapped Sierra locations are as follows:

    <table>
      <tr><th>Sierra location</th><th># of items</th></tr>
      <tr><td>bwith / bound in above</td><td>218</td></tr>
      <tr><td>cwith / Contained in above</td><td>28</td></tr>
      <tr><td>digit / Digitised Collections</td><td>10</td></tr>
      <tr><td>wqrfe / Enquiry Line</td><td>2</td></tr>
      <tr><td>temp1 / At Digitisation</td><td>1</td></tr>
      <tr><td>wghig / Gallery</td><td>1</td></tr>
      <tr><td>sgmip / sgmip</td><td>1</td></tr>
      <tr><td>gblip / 215 Information Point</td><td>1</td></tr>
    </table>

    </details>

    <details>
    <summary>Proposed heuristic for matching Sierra holdings locations to controlled types</summary>

    For Sierra holdings, the API only returns a location *code* (e.g. stax) via fixed field 40.

    We will look up the location code to find the location name, then apply a similar rule to that which we apply for items.
    If the location code or name are unrecognised, we will skip adding a location to the holding.

    This heuristic allows us to create locations in our controlled type for **99.87% of all holdings**.
    </details>

*   We will add an optional `"shelfMark"` field to the PhysicalLocation model.
    We will reuse the `"label"` field for the shelf location.

    The shelfmark will be drawn from the *callNumber* field in Sierra (e.g. "/HIS").
    The label will be drawn from the *location.name* in Sierra (e.g. "History of Medicine").
    This gives us a good initial implementation, and we can refine it later if necessary.

    For holdings records, only the `"label"` will be populated.
    The holdings records don't have enough information to populate a shelfMark.

    For now, this will be populated on all "PhysicalLocation" records, including ClosedStores.
    We may choose to remove it from some locations later, after appropriate discussions with Collections Information to ensure the API still includes all the identifiers and information required by users.

    <details>
      <summary>Examples of the proposed output</summary>

      An item in closed stores:

      ```json
      {
        "id": "i1000008",
        "label": "Closed stores",
        "locationType": {
          "code": "closed-stores",
          "label": "Closed stores",
          "type": "LocationType"
        },
        "type": "Location"
      }
      ```

      An item on open shelves:

      ```json
      {
        "id": "i1000011",
        "label": "Medical Collection",
        "shelfmark": "WP300 1902C96c",
        "locationType": {
          "code": "open-shelves",
          "label": "Open shelves",
          "type": "LocationType"
        },
        "type": "Location"
      }
      ```

      An online journal resource:

      ```json
      {
        "id": "h1234567",
        "url": "https://journals.example.org/login",
        "link_text": "View this journal",
        "credit": "ACME Journal Publishings",
        "locationType": {
          "code": "online-resource",
          "label": "Online resource",
          "type": "LocationType"
        },
        "type": "Location"
      }
      ```

    </details>