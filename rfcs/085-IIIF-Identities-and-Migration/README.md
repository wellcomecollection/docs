# RFC 085: Identifiers of and within IIIF resources after the migration

Wellcome's published IIIF resource make heavy use of b numbers to generate URIs of resources such as Manifests and Canvases within Manifests. This RFC discusses the implications of the migration to Folio and Axiell Collections; b number won't exist.
 
**Last modified:** 2026-02-27T17:00+00:00

## Context

Wellcome has until now published IIIF resources at URIs that use b numbers and Calm identifiers to form persistent identifiers for Manifests and Collections. Within Manifests, nested IIIF resources such as Canvases derive their URIs from elements in METS files which in turn derive their identities from filenames. These filenames are typically those of captured JP2s for digitised works, and original file names for born digital items. JP2 filenames until now use b numbers, e.g., the fourth page of a book is b12345678_0004.jp2. This RFC discusses how IIIF resources are handled when b numbers are no longer the bibliographic source identifier. We need to consider what happens to existing IIIF resources as well as new ones introduced after the change.

## Current behaviour

Consider _The Biocrats:_

[https://wellcomecollection.org/works/zjytxny8](https://wellcomecollection.org/works/zjytxny8)

- The catalogue API for this is [https://api.wellcomecollection.org/catalogue/v2/works/zjytxny8](https://api.wellcomecollection.org/catalogue/v2/works/zjytxny8).
- The IIIF Manifest for this is [https://iiif.wellcomecollection.org/presentation/b18035978](https://iiif.wellcomecollection.org/presentation/b18035978)

> _This work was one of the very first test resources the DDS processed, in prototypes all the way back to 2011. It has had a b-number-based IIIF URI since then and a iiif.wellcomecollection.org URI for nearly a decade._ 

Ideally, canonical URIs for IIIF resources **should use the work identifier** rather than the b number (or any other underlying system-specific identifier), so the IIIF Manifest for The Biocrats would be https://iiif.wellcomecollection.org/presentation/zjytxny8. This insulates the public persistent identity of the work from changes in source catalogue identifiers (b numbers are Sierra-specific).

This link actually works now, and will redirect to the currently-canonical b-number. We can flip this around, so that in the new system the redirect is the other way - a link to [https://iiif.wellcomecollection.org/presentation/b18035978](https://iiif.wellcomecollection.org/presentation/b18035978) would now redirect to [https://api.wellcomecollection.org/catalogue/v2/works/zjytxny8](https://api.wellcomecollection.org/catalogue/v2/works/zjytxny8).

If we are just dealing with discrete HTTP-level resources, then the redirect mechanisms of HTTP: **301 Moved Permanently** handles this situation as intended. But for IIIF Presentation resources, the situation is much more complicated. Manifests contain many, many child HTTPS URIs: the `id` values of resources like Ranges and most importantly, of Canvases. These are not necessarily dereferenceable (and at Wellcome, you cannot load a Canvas on its own from its HTTPS URI `id`). Whether or not they are dereferenceable (and therefore redirectable) in any given implementation is irrelevant, however, because a IIIF Client application will use the identifiers in the JSON body of the resource: it _expects_ Manifests to contain their Canvases in their entirety. Even though they have https URIs they are not _external_ resources (in IIIF terms).

While any IIIF resource might be the `target` of an Annotation, they are usually on Canvases. If someone has transcribed or commented or otherwise made any annotation, in any system, for whatever purpose, where the target is a Canvas within a Wellcome Manifest, that annotation's `target` property uses the published `id` of the Canvas within the Manifest. An example:

```json
{
    "id": "https://iiif.wellcomecollection.org/presentation/b21286437/canvases/b21286437_0145.jp2/classifying/i0",
    "type": "Annotation",
    "motivation": ["commenting"],
    "body": {
        "type": "TextualBody",
        "language": ["en"],
        "value": "This is a picture of a jellyfish"
    },
    "target": "https://iiif.wellcomecollection.org/presentation/b21286437/canvases/b21286437_0145.jp2#xywh=156,1336,1728,1430"
}
```

If this annotation is linked from the Manifest then the short form of the `target` is sufficent, because the client application already has the Canvas ID loaded. If this annotation were published standalone, an expanded form would be needed:

```jsonc
    // ...rest of annotation
    "target": {
        "id": "https://iiif.wellcomecollection.org/presentation/b21286437/canvases/b21286437_0145.jp2#xywh=156,1336,1728,1430",
        "type": "Canvas",
        "partOf": {
             "id": "https://iiif.wellcomecollection.org/presentation/b21286437",
             "type": "Manifest"
        }
    }
```

This chunk of JSON may be held external to Wellcome, out of our control. It targets part of Wellcome's published IIIF linked data. Given the expanded form, a client could load the Manifest and be redirected to the new Manifest URI, but it would still look for a Canvas with `"id": "https://iiif.wellcomecollection.org/presentation/b21286437/canvases/b21286437_0145.jp2"` within the received JSON payload. There's no opportunity for the server to intervene and "redirect" to a new Canvas identity.

The sources of these Canvas identities are filenames in METS:

```xml
<mets:file ID="FILE_0145_OBJECTS" MIMETYPE="image/jp2">
    <mets:FLocat LOCTYPE="URL" xlink:href="objects/b21286437_0145.jp2" />
</mets:file>
```

Simplifying somewhat, we generate a `StorageIdentifier` from the `xlink:href` attribute; this is a path-element safe version of the file path after /objects (in this case it's the same as that path, but isn't always). This `xlink:href` attribute also gives us the relative locaton of the file in the storage service, so we can load it into the DLCS from there. The `id` of the image asset in the DDS is derived from its storage location filename. In the IIIF, we generate a Canvas `id` by joining the METS manifestation identifier (a single work may have multiple manifestations) with this storage identifier. Here's the full Canvas from the Manifest, with added comments showing all the places such IDs form part of identifiers, both dereferenceable and non-dereferenceable.

```jsonc
{
    "id": "https://iiif.wellcomecollection.org/presentation/b21286437/canvases/b21286437_0145.jp2",
    "type": "Canvas", // IIIF Resource identifier           ^^^^^^^^^          ^^^^^^^^^^^^^^
    "label": { "none": ["127"] },
    "width": 2234,
    "height": 3410,
    "thumbnail": [
        {
            "id": "https://iiif.wellcomecollection.org/thumbs/b21286437_0145.jp2/full/66,100/0/default.jpg",
            "type": "Image", // DLCS URL (an image)           ^^^^^^^^^^^^^^^^^^
            "width": 66,
            "height": 100,
            "service": [
                {
                    "@id": "https://iiif.wellcomecollection.org/thumbs/b21286437_0145.jp2",
                            // DLCS URL (an image service)           ^^^^^^^^^^^^^^^^^^
                    "@type": "ImageService2",
                    "profile": "http://iiif.io/api/image/2/level0.json",
                    "width": 671,
                    "height": 1024,
                    "sizes": [
                        {"width":66,"height":100},
                        {"width":131,"height":200},
                        {"width":262,"height":400},
                        {"width":671,"height":1024}
                    ]
                }
            ]
        }
    ],
    "seeAlso": [
        {
            "id": "https://api.wellcomecollection.org/text/alto/b21286437/b21286437_0145.jp2",
            // Dereferenceable - ALTO file for this page        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
            "type": "Dataset",
            "profile": "http://www.loc.gov/standards/alto/v3/alto.xsd",
            "label": {"none":["METS-ALTO XML"]},
            "format": "text/xml"
        }
    ],
    "items": [
    {
        "id": "https://iiif.wellcomecollection.org/presentation/b21286437/canvases/b21286437_0145.jp2/painting",
        // DDS ID  (AnnotationPage URI for this page)           ^^^^^^^^^          ^^^^^^^^^^^^^^^^^^
        "type": "AnnotationPage",
        "items": [
            {
                "id": "https://iiif.wellcomecollection.org/presentation/b21286437/canvases/b21286437_0145.jp2/painting/anno",
                    // DDS ID  (Painting annotation)                    ^^^^^^^^^          ^^^^^^^^^^^^^^^^^^
                "type": "Annotation",
                "motivation": "painting",
                "body": {
                    "id": "https://iiif.wellcomecollection.org/image/b21286437_0145.jp2/full/671,1024/0/default.jpg",
                    "type": "Image", // DLCS URL (an image)          ^^^^^^^^^^^^^^^^^^
                    "width": 671,
                    "height": 1024,
                    "format": "image/jpeg",
                    "service": [
                        {
                            "@id": "https://iiif.wellcomecollection.org/image/b21286437_0145.jp2",
                                     // DLCS URL (an image service)           ^^^^^^^^^^^^^^^^^^
                            "@type": "ImageService2",
                            "profile": "http://iiif.io/api/image/2/level1.json",
                            "width": 2234,
                            "height": 3410
                        }
                    ]
                },
                "target": "https://iiif.wellcomecollection.org/presentation/b21286437/canvases/b21286437_0145.jp2"
                    // Canvas repeated as target                            ^^^^^^^^^          ^^^^^^^^^^^^^^
            }
        ]
    }
    ],
    "annotations": [
        {
            "id": "https://iiif.wellcomecollection.org/annotations/v3/b21286437/b21286437_0145.jp2/line",
                // Dereferenceable - full text annotations            ^^^^^^^^^ ^^^^^^^^^^^^^^^^^^
            "type": "AnnotationPage",
            "label": {"en":["Text of page 127"]}
        }
    ]
}
```

Canvases aren't the only IIIF resources to be identified with URIs derived from METS. Given a METS Logical structMap:

```xml
<mets:structMap TYPE="LOGICAL">
<mets:div ADMID="AMD" DMDID="DMDLOG_0000" ID="LOG_0000" LABEL="Elementary text-book of zoology" TYPE="Monograph">
    <mets:div ID="LOG_0001" TYPE="Cover" />
    <mets:div ID="LOG_0002" TYPE="TitlePage" />
    <mets:div ID="LOG_0003" TYPE="Preface" />
    <mets:div ID="LOG_0004" TYPE="TableOfContents" />
</mets:div>
</mets:structMap>
```

...we generate IIIF Ranges using these assigned `ID` attributes:

```json
{
    "structures": [
        {
            "id": "https://iiif.wellcomecollection.org/presentation/b21286437/ranges/LOG_0001",
            "type": "Range",
            "label": {"none":["Cover"]},
            "items": [
                {
                    "id": "https://iiif.wellcomecollection.org/presentation/b21286437/canvases/b21286437_0001.jp2",
                    "type": "Canvas"
                }
            ]
        },
        {
            "id": "https://iiif.wellcomecollection.org/presentation/b21286437/ranges/LOG_0002",
            "type": "Range",
            "label": {"none":["Title Page"]},
            "items": [
                {
                    "id": "https://iiif.wellcomecollection.org/presentation/b21286437/canvases/b21286437_0005.jp2",
                    "type": "Canvas"
                }
            ]
        },
        {
        "id": "https://iiif.wellcomecollection.org/presentation/b21286437/ranges/LOG_0003",
        "type": "Range",
        "label": {"none":["Preface"]},
        "items": [
            {
                "id": "https://iiif.wellcomecollection.org/presentation/b21286437/canvases/b21286437_0009.jp2",
                "type": "Canvas"
            }
        ]
        },
        {
            "id": "https://iiif.wellcomecollection.org/presentation/b21286437/ranges/LOG_0004",
            "type": "Range",
            "label": {"none":["Table of Contents"]},
            "items": [
                {
                    "id": "https://iiif.wellcomecollection.org/presentation/b21286437/canvases/b21286437_0011.jp2",
                    "type": "Canvas"
                }
            ]
        }
    ]
}
```

However, for Goobi at least, the Range identifiers are independent of the work identity. So for these, we are OK.

### Points to note

 - The 60m+ files in the storage service have b-number- or CALM RecordID-based IDs and therefore URIs.
 - There is a clear relationship between:
   - METS xlink:href attributes
   - Storage service locations
   - Canvas identifiers in IIIF resources (and annotations, annotation pages)
   - DLCS-hosted Content (AV, image etc) URIs for digitised and born digital material - image services, AV derivatives and other files. 
 - They all involve b numbers, or CALM Record IDs.


## Proposal

A desirable outcome is that:

 - IIIF Manifests and Collections adopt a work-id-based URI as the canonical URI
 - Any existing published IIIF Manifest or Collection requested on a B-number or CALM recordID-based path will redirect to the work ID
 - Anything already published that uses b-number identifiers for Canvases will continue to use those identifiers
 

Other dereferenceable resources linked from Manifests:

 - ALTO files per Canvas
 - Line level annotations per Canvas
 - Full text per Manifest
 - Single Annotation Page identifying images, figures and tables, per Manifest
 
Unknowns:

 - What will a Goobi METS file look like for a completely new work that never had a b number?
 - What will a Goobi METS file look like when a workflow is re-run (i.e., an existing METS file is updated)?
 - What happens to existing files in the storage service when a workflow is re-run?
 - 
 - 


_A detailed description of the proposed solution, including any relevant technical details, diagrams, or examples._

## Alternatives considered

A discussion of any alternative solutions that were considered, and why they were not chosen.

## Impact

A description of the impact of the proposed solution, including any potential risks or challenges.

## Next steps

A list of next steps for implementing the proposed solution, including any dependencies or prerequisites.



Description

See https://digirati.slack.com/archives/CBT40CMKQ/p1764251298635379Connect your Slack account  for a starting point.

What will the DDS be doing with new works in the future when the sources of truth are Folio and Axiell Collections?

What will it be doing with reprocessed works that exist today?

What does a canonical IIIF resource URI look like in future?

What redirects happen?

How will Canvas IDs and other resources internal to a manifest be persistent?

What might we need from a Wellcome identity service?

What will METS files look like from Goobi and Archivematica in the new world?

how are files named in the storage service?

 

From Jonathan:

 

We agreed that the Work ID becomes the canonical ID in IIIF manifests, this is for all works whether they are bibliographic or archival records.

There will be an identity service (essentially an extension of the ID minter database)  with an API so that the existing manifests (anywhere which use B Numbers) will continue to work

When something was created before the Sierra/Folio cut-over (i.e. if it is likely to have a manifest with a b number) the ID service will be needed to use the previous identity if it is being reprocessed for whatever reason

Tom/Digirati to write an RFC on the above [which I will assume will inform the basis of a work package]
We will write an RFC on the approach to the identity service i.e. what we need to do to expose that DB so that it can be consumed by DLCS

----


Redirect "problem" for IIIF resources.


---

[11:51 AM]Integration tests that verify CanvasIds are the same for pre-cutoff manifests as they were before, even if the manifest id is now the workid
[11:51 AM]workid becomes canonical form for all IIIF (loses the hierarchical CALM version although will still work)
tomcrane  [12:05 PM]
Is it a cutoff date or is it something learned from the id service - whether to use workid or bnumber in canvas generation
(only use legacy canvas ids for b nums and not calm refs)