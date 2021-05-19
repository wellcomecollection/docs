# Tracking changes to the Miro data

The Miro data was originally exported as a collection of XML files, one per letter prefix.
We have split these XML files into a series of JSON files, one per image.
These JSON files are stored in S3, with a pointer in DynamoDB:

```
MiroSourcePayload {
  id: String
  isClearedForCatalogueAPI: Boolean
  location: S3ObjectLocation
  version: Int
}

S3ObjectLocation {
  bucket: String
  key: String
}
```

Although the Miro data is static, we may change how we want to use it.
For example:

-   A contributor may ask us to remove an image from the site
-   We may change the license on an image
-   We may make an image available that we were previously unsure about

We need a way to apply these changes and record them.

## Principles

-   We should be able to override specific values in the Miro data/transformer.
    We should assume we will asked to make changes on an ongoing basis -- this isn't a one-off operation.
-   We should keep a record of our changes: who made them, when, and why
-   Our changes should be separate from the Miro exports

## Proposal

We extend the `MiroSourcePayload` model with two optional fields:

```
MiroSourcePayload {
  id: String
  isClearedForCatalogueAPI: Boolean
  location: S3ObjectLocation
  version: Int
  events: List[MiroUpdateEvent]?
  overrides: MiroSourceOverride?
}
```

The `MiroUpdateEvent` model will track our changes to the data:

```
MiroUpdateEvent {
  description: String
  message: String
  date: Datetime
  user: String
}
```

The `description` will be an automatically generated description of the change, e.g.

> Change license override from "None" to "cc-by"

and the `message` will be a human-written explanation of why we made the change, e.g.

> We realised we could make this available under a more permissive licence.

The `date` and `user` will be automatically populated.

The `MiroSourceOverride` model will allow us to track overrides:

```
MiroSourceOverride {
  license: License?
}
```

This model can be extended to add new overrides as necessary.

When we make changes to a Miro record, we add a new MiroUpdateEvent to record the change, and we update the DynamoDB record.
This gives us change tracking that preserves the integrity of the original Miro data in S3.

### Python API

As part of this change, there will be a collection of Python functions that you can use to write scripts for modifying the Miro data.

```
# miro_updates.py

def make_image_available(image_id, message: str)

def suppress_image(image_id, message: str)

def set_license_override(image_id, license_code: str, message: str)

def remove_license_override(image_id, message: str)
```

You could use these to, for example, write a script to suppress three images:

```python
from miro_updates import suppress_image

for image_id in ["A0000001", "A0000002", "A0000003"]:
    suppress_image(image_id, message="We were asked to take these images down; see email from John Smith on 18 May 2021")
```

### Worked example

Suppose we have the following Miro record:

```
MiroSourcePayload {
  id = "A0000001"
  isClearedForCatalogueAPI = true
  location = S3ObjectLocation { bucket = "vhs-miro", key = "A0000001.json" }
  version = 1
}
```

The data in the S3 metadata means this is mapped to an "in-copyright" license.

We get an email from the contributor, who tells us we can release it under the CC-BY-NC license.
We call the Python helper:

```python
set_license_override(
    image_id="A0000001",
    license_code="cc-by-nc",
    message="An email from John Smith (the contributor) explained we can use CC-BY-NC"
)
```

The helper will add an appropriate MiroUpdateEvent and MiroSourceOverride:

```diff
 MiroSourcePayload {
   id = "A0000001"
   isClearedForCatalogueAPI = true
   location = S3ObjectLocation { bucket = "vhs-miro", key = "A0000001.json" }
+  events = [
+    MiroUpdateEvent {
+      description = "Change license override from 'None' to 'cc-by-nc'"
+      message = "An email from John Smith (the contributor) explained we can use CC-BY-NC"
+      date = 2001-01-01T01:01:01Z
+      user = "Alex Chan <chana@wellcomecloud.onmicrosoft.com>"
+    },
+  ]
+  overrides = MiroSourceOverride {
+    license = "cc-by-nc"
+  }
+  version = 2
 }
```

Later we get another contributor, saying we can now use CC-BY.
We call the helper a second time:

```python
set_license_override(
    image_id="A0000001",
    license_code="cc-by",
    message="An email from John Smith (the contributor) said we can use CC-BY"
)
```

And the record gets updated again:

```diff
 MiroSourcePayload {
   id = "A0000001"
   isClearedForCatalogueAPI = true
   location = S3ObjectLocation { bucket = "vhs-miro", key = "A0000001.json" }
   events = [
     MiroUpdateEvent {
       description = "Change license override from 'None' to 'cc-by-nc'"
       message = "An email from John Smith (the contributor) explained we can use CC-BY-NC"
       date = 2001-01-01T01:01:01Z
       user = "Alex Chan <chana@wellcomecloud.onmicrosoft.com>"
     },
    MiroUpdateEvent {
      description = "Change license override from 'cc-by-nc' to 'cc-by'"
      message = "An email from John Smith (the contributor) said we can use CC-BY"
      date = 2002-02-02T02:02:02Z
      user = "Henry Wellcome <wellcomeh@wellcomecloud.onmicrosoft.com>"
    },
   ]
   overrides = MiroSourceOverride {
+    license = "cc-by"
   }
+  version = 3
 }
```
