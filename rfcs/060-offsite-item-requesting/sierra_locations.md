

# Sierra locations in the Catalogue API

1. [Sierra items have](https://github.com/wellcomecollection/scala-libs/blob/fbd61a4f7980b068007380b5d42b6ed24d9736f7/sierra/src/main/scala/weco/sierra/models/data/SierraItemData.scala) `location`s which consist of a `code` and a `name` . There are a large number of possible values of these.
2. Catalogue API items have `locations` which can be `DigitalLocation`s or `PhysicalLocations`. This document is about physical locations. 
3. [Catalogue API physical locations](https://github.com/wellcomecollection/catalogue-pipeline/blob/6f7bd7d4338a316669b7f9d5d177537bef971181/common/internal_model/src/main/scala/weco/catalogue/internal_model/locations/LocationType.scala#L47-L65) have `locationType`s which have an `id` and a `label`. These can currently take the following values:

| id            | label         |
| ------------- | ------------- |
| closed-stores | Closed stores |
| open-shelves  | Open shelves  |
| on-exhibition | On exhibition |
| on-order      | On order      |

4. We currently map Sierra item `location`s to the above  `locationType`s using the `name` only. We could also use the `code`, but we currently don't. [This mapping](https://github.com/wellcomecollection/catalogue-pipeline/blob/6f7bd7d4338a316669b7f9d5d177537bef971181/common/source_model/src/main/scala/weco/catalogue/source_model/sierra/rules/SierraPhysicalLocationType.scala) is done by looking for *case-insensitive substrings* in the location names:

| substring exists in name?     | locationType ID |
| ----------------------------- | --------------- |
| archives & mss well.coll      | closed-stores   |
| at digitisation               | closed-stores   |
| by appointment                | closed-stores   |
| closed stores                 | closed-stores   |
| conservation                  | closed-stores   |
| early printed books           | closed-stores   |
| iconographic collection       | closed-stores   |
| offsite                       | closed-stores   |
| unrequestable                 | closed-stores   |
| biographies                   | open-shelves    |
| folios                        | open-shelves    |
| history of medicine           | open-shelves    |
| journals                      | open-shelves    |
| medical collection            | open-shelves    |
| medicine & society collection | open-shelves    |
| open shelves                  | open-shelves    |
| quick ref collection          | open-shelves    |
| quick ref. collection         | open-shelves    |
| rare materials room           | open-shelves    |
| student coll                  | open-shelves    |
| exhibition                    | on-exhibition   |

Additionally:

- If the `name` is empty, or if it contains `bound in above` or `contained in above`, we look at the [other items](https://github.com/wellcomecollection/catalogue-pipeline/blob/6f7bd7d4338a316669b7f9d5d177537bef971181/pipeline/transformer/transformer_sierra/src/main/scala/weco/pipeline/transformer/sierra/transformers/SierraItems.scala#L71) on the bib:
  - We find all the distinct valid `locationType`s of the other items
  - If there is only one, we use that for this location too. Otherwise, we assign no `locationType`.
- `on-order` items are created [slightly differently](https://github.com/wellcomecollection/catalogue-pipeline/blob/6f7bd7d4338a316669b7f9d5d177537bef971181/pipeline/transformer/transformer_sierra/src/main/scala/weco/pipeline/transformer/sierra/transformers/SierraItemsOnOrder.scala) using order records and can be considered separate for the purposes of this document.

## Access conditions

Locations in the catalogue API (described above) have [`accessConditions`](https://github.com/wellcomecollection/catalogue-pipeline/blob/c1686bf4902cbebb72c6624205ca3953209f0a7b/common/internal_model/src/main/scala/weco/catalogue/internal_model/locations/AccessCondition.scala) consisting of a `method` and optionally a `status`, plus some optional free text  `terms` and/or a `note`.

Access `method`s can currently take the following values:

| id              | label           |
| --------------- | --------------- |
| online-request  | Online request  |
| manual-request  | Manual request  |
| not-requestable | Not requestable |
| view-online     | View online     |
| open-shelves    | Open shelves    |

Access `status`es can take the following values:

| id                      | Label                   |
| ----------------------- | ----------------------- |
| open                    | Open                    |
| open-with-advisory      | Open with advisory      |
| restricted              | Restricted              |
| by-appointment          | By appointment          |
| temporarily-unavailable | Temporarily unavailable |
| unavailable             | Unavailable             |
| closed                  | Closed                  |
| licensed-resources*     | Licensed resources      |
| permission-required     | Permission required     |

*the internal representation of licensed resources is further specified into "resources" and "related resources" as per [MARC 856 ind 2](https://www.loc.gov/marc/bibliographic/bd856.html), in order to implement *availability.*

#### Availability and Restrictions

*Internally*, access statuses also have derived boolean properties of `isAvailable` and `hasRestrictions`. Access conditions and locations inherit these properties transitively.

- An access status is **available** if it is `open`, `open-with-advisory`, or is a `licensed-resource` that is not a related resource.
- An access status **has restrictions** if it is  `open-with-advisory`, `restricted`, `by-appointment`, `closed` or `permission-required`.

*Externally*, these properties have the following effects:

1. Catalogue API works have `availabilities`, a list of any number (including none) of the following:

| id            | label         |
| ------------- | ------------- |
| online        | Online        |
| closed-stores | Closed stores |
| open-shelves  | Open shelves  |

- A work has an `online` availability if any of its items have a `DigitalLocation` which is *available*

- A work has a `closed-stores` availability if any of its items have a `PhysicalLocation` with a `closed-stores` location type and none of the work's `notes` are a terms-of-use note that [implies](https://github.com/wellcomecollection/catalogue-pipeline/blob/d61febc565af1dc15d13b1afec71109b54ce2763/common/internal_model/src/main/scala/weco/catalogue/internal_model/work/Availability.scala#L83-L100) that the work is held at another institution. *Note JP 18/01/24: this seems like a hack, should we address it?*

- A work has an `open-shelves` availability if any of its items have a `PhysicalLocation` with an `open-shelves` location type

2. Catalogue API digital location `thumbnail`s are not populated if the location is **restricted**.

 ### Determining access conditions

Access methods are determined as a [function of the following properties](https://github.com/wellcomecollection/catalogue-pipeline/blob/6e8b6439398078692bc9ab54aecb045d39c49173/common/source_model/src/main/scala/weco/catalogue/source_model/sierra/rules/SierraItemAccess.scala#L65) of the item in Sierra:

- Hold count
- Status code in fixed field 88
- OPAC message code in fixed field 108
- The result of the Sierra rules for requesting (*see below*)
- The location type (*see above*)
- The presence of a due date in fixed field 65
- The notes, in any varfield with a field tag `n`
- The reserves notes, in any varfield with a field tag `r`

**Rules for requesting**

The "rules for requesting" live in Sierra, but are replicated in *both* the [catalogue pipeline](https://github.com/wellcomecollection/catalogue-pipeline/blob/97e4a43ad57b26d7e933c1f2708716a46eedd3ff/common/source_model/src/main/scala/weco/catalogue/source_model/sierra/rules/SierraRulesForRequesting.scala#L40) and the [items API](https://github.com/wellcomecollection/catalogue-api/blob/1680c3c0484fa23942887950c46c626db8baff1f/common/stacks/src/main/scala/weco/catalogue/source_model/sierra/rules/SierraRulesForRequesting.scala). They determine whether an item is requestable or not. If it is not requestable, the rules can provide a message.

**Mapping Sierra data to access conditions**

*Note JP 19/01/2024: the rules are described here in the roughly same way that they are written in the code. My view is that the logic here has grown in a way which mixes wholly unrelated concerns and that it would be possible and desirable to rewrite this mapping in a way that would be easier to reason about. I think a "funneling" or flowchart-like approach to the mapping would be preferable to this very flat representation.*

For **`closed-stores`** location types:

- If they have **no holds**, an **available** status code, an **online request** OPAC message, and are determined as **requestable** by the rules for requesting: they are accessible by the method **`online-request`** with status **`open`**. 
- If they have **no holds**, an **available** status code, a **restricted** OPAC message, and are determined as **requestable** by the rules for requesting: they are accessible by the method **`online-request`** with status **`restricted`**. 
- If they have **no holds**, an **available** status code, a **manual request** OPAC message, and are determined as **not requestable** with a message corresponding to "needs manual request" by the rules for requesting: they are accessible by the method **`manual-request`**. Relevant notes are copied into the notes field.
- If they have a **closed** status code, an **unavailable** OPAC message, and are determined as **not requestable** with a message corresponding to a closed item by the rules for requesting: they are  **`not-requestable`** with status **`closed`**.
- If they have **no holds**, a **permission required** status code, a **by appointment** OPAC message, and are determined as **not requestable** with a message corresponding to "no public message" by the rules for requesting: they are accessible by the method **`manual-request`** with status **`by-appointment`**.
- If they have **no holds**, a **permission required** status code, a **donor permission** OPAC message, and are determined as **not requestable** by the rules for requesting: they are accessible by the method **`manual-request`** with status **`permission-required`**.
- If they have **1 or more holds**: they are **`not-requestable`** with status **`temporarily-unavailable`**.
- If the rules for requesting determine them to be **not requestable** with a message corresponding to "in use by another reader": they are **`not-requestable`** with status **`temporarily-unavailable`**.

For **`open-shelves`** location types:

- If they have **no holds**, an **available** status code, an **open shelves** OPAC message, **no due date**, and are determined as **not requestable** with a message corresponding to "on open shelves" by the rules for requesting: they are accessible by the method **`open-shelves`**.
- If they are determined as **not requestable** with a message corresponding to "in use by another reader" by the rules for requesting: they are **`open-shelves`** with status **`temporarily-unavailable.`**
- If they **have a due date**: they are **`open-shelves`** with status **`temporarily-unavailable`**.

**`on-exhibition`** location types with a **non-empty reserve notes varfield** are **`not-requestable`** with the note from the reserve notes.

Finally, for all locations not yet mapped:

- If they are determined as **not requestable** with a message corresponding to "request top item" by the rules for requesting: they are **`not-requestable`** with a note from the message.
- If they have **no location type**, a **closed** access status, an **unavailable** OPAC message, and are determined as **not requestable** with a message corresponding to a closed item by the rules for requesting: they are  **`not-requestable`** with status **`closed`**.
- If they have an **unavailable** status code, an **unavailable** OPAC message, and are determined as **not requestable** with a message corresponding to "item unavailable" **or** "at digitisation" by the rules for requesting: they are **`not-requestable`** with status **`temporarily-unavailable`**.
- If they have a **missing** or **withdrawn** status code annd are determined as **not requestable** with a message corresponding to "item missing" or "item withdrawn" by the rules for requesting: they are **`not-requestable`**  with status **`unavailable`**.
- If any non-mapped item **has a due date**, it is **`not-requestable`**  with status **`temporarily-unavailable`**.
- **Any remaining items are `not-requestable`**.

### Requesting

Answering the question of "what makes a work requestable?" thankfully only requires knowledge of a subset of the above. This is represented by the [equivalent class](https://github.com/wellcomecollection/catalogue-api/blob/1680c3c0484fa23942887950c46c626db8baff1f/common/stacks/src/main/scala/weco/catalogue/source_model/sierra/rules/SierraItemAccess.scala) in the items API.

*Note JP 19/01/2024: is it wise to duplicate a subset of the logic from the pipeline like this? Why are we representing rules for requesting results as Options?*

An item is requestable via the items API if **all** of the below hold:

- It is in the closed stores
- It has an available status code
- It has no current holds
- It satisfies the rules for requesting
- It has an OPAC message for online request *or* restricted access

*Note JP 19/01/2024: Are all of these necessary? Why don't the rules for requesting cover the status code and OPAC message?*

From the perspective of API consumers, this is equivalent to an item being requestable if it:

- Has a location type of `closed-stores`
- Has an `online-request` access method
- Has an `open`, `open-with-advisory`, or `restricted` access status

**Request dates**

The items API can receive a request with a `pickupDate`. This is not validated (other than for correctness) against any opening times etc. It is placed in the hold note with the [format](https://github.com/wellcomecollection/catalogue-api/blob/e113145a1771a3b72aa3ee66de8034ffdd8f95a3/requests/src/main/scala/weco/api/requests/models/HoldNote.scala#L12) `"Requested for: yyyy-MM-dd"`.

A list of valid pickup dates is created by the frontend webapp and presented to the user by using the venue opening times.

1. We take the list of all days on which the library is open (starting the next open day if it's currently before 10am, or 2 working days later if it's after 10am) over the next 2 weeks.
2. If there are any exceptional (ie non-routine working hours) closure dates during that period, we extend the list until until the total number of available days is equivalent to a normal 2 week period.

The data for opening times comes from Prismic.

*Note JP 19/01/2024: the way this data is computed is very complex. I wonder if it could be simplified. It also feels like the responsibility to provide possible pickup dates should reside in the items API, although this would require it to talk to Prismic.*
