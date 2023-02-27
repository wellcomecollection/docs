# Glossary
## Third parties

**Archivematica** - [A tool for born-digital workflows](https://www.archivematica.org/en/). We use Archivematica to package (+metadata) born-digital content.

**BagIt** - [A standard for packaging digital content](https://datatracker.ietf.org/doc/html/rfc8493). Both Archivematica and Goobi output BagIt-compliant "bags", which are stored in the storage service.

**CALM** - [Archive management software](https://www.axiell.com/uk/solutions/product/calm/) which stores all catalogue data pertaining to archives. These are "harvested" into Sierra every night, but we get archive data from the CALM API directly.

**Digirati** - [An agency](https://digirati.com/) who create/maintain DLCS and contribute to the IIIF standards, who did a lot of the work on wellcomelibrary.org and also helped with our identity/requesting functionality.

**DLCS** - [Our image/IIIF server](https://dlcs.info/), run by Digirati, which provides both the actual asset delivery and the IIIF image APIs.

**Encore** - [The "frontend" for Sierra](https://www.iii.com/products/encore/), which has historically been used on wellcomelibrary.org. This provides search and other user-facing interfaces; much of our work has been to replace it. 

**Goobi** - [Software for digitisation projects](https://www.intranda.com/en/digiverso/goobi/goobi-overview/). The digital production team use Goobi for packaging (+ metadata) digitised content.

**Intranda** - [The company](https://www.intranda.com/) who created and maintain Goobi. They are based in Germany.

**IIIF** - [A set of standards for image data](https://iiif.io/). All of our images (from MIRO or via METS files) are exposed using IIIF APIs, which at their simplest can allow users to select the size, rotation, crop etc of an image; they can also expose metadata for images in context.

**iiif-builder** - The server that provides metadata in the form of the IIIF presentation and search APIs. This is in practice part of the same system as DLCS, and is also maintained by Digirati, but it is a separate service which evolved out of DDS, the old library service layer.

**MARC** - [A data format for library-related data](https://www.loc.gov/marc/). Both the format and the use of specific fields is standardised. MARC was created by the Library of Congress - in the 1960s!

**METS** - [A standard for metadata for digitised content](https://www.loc.gov/standards/mets/). Our new (post-MIRO) digitised content has metadata stored in METS files, and it also has catalogue records in Sierra.

**MIRO** - The system which stored the data for wellcomeimages.org, now frozen and subsumed into our services. 

**OPAC, the** - An older and more limited frontend for Sierra, kind of equivalent to Encore. Comes "in the box" with Sierra, rather than being a separate product like Encore. Sometimes known as WebPAC.

**Sierra** - [Our Library Management System](https://www.iii.com/products/sierra-ils/). Sierra manages catalogue records, patrons and more. It exposes a pretty good API which is [well documented](https://techdocs.iii.com/sierraapi/Content/titlePage.htm).

**TEI** - [A metadata standard for text/manuscripts](https://github.com/wellcomecollection/wellcome-collection-tei). We are using this for some non-Western manuscripts as it offers much better metadata than existing library systems and standards.

## Internal terms

In an effort to ensure everyone uses the same language and help with onboarding, here is a incomplete glossary of the terms used in relation to the website content and context.


**Archive**

**Article**
Umbrella term for everything under `/stories`. Could be a story, a webcomic, a photo essay...

**Author**

**Book** 
[Example](https://wellcomecollection.org/books/Y7QWrREAAHC43oH0)
Book is a content type in Prismic, displayed on the [Books listing page](https://wellcomecollection.org/books). They are books that are published by Wellcome.

**Collection**

**Concept**

**Contributor**

**Content Type**

**Digital Guide**

**Digital Location**

**Digitised Item**

**Event**
[Example](https://wellcomecollection.org/events/Y7P3oxEAAHC43k0_)
Displayed in various listing pages, including [Events](https://wellcomecollection.org/events)
<!-- Add description -->

**Exhibition**
[Example](https://wellcomecollection.org/exhibitions/Yv95yBAAAILuCNv6)
Displayed in various listing pages, including [Exhibitions](https://wellcomecollection.org/exhibitions)
<!-- Add description -->

**Exhibition Guide**

**Format**

**Image Gallery**

**In Pictures**

**Installation**

**License/Licence**
Spelled Licence on the UI (UK spelling) and License in the API.
<!-- Add description -->

**Manuscript**

**Photo Story**

**Location**

**Role**
Part of the Contributors object, defines the type of contributor (author, illustrator, etc.)

**Season**
A season is a grouping of most any content types, but primarily events, exhibitions, stories. The idea is that it's a time-limited, curated programme of activities, and it gets promoted as one programme. e.g.: [What does it mean to be human, now?](https://wellcomecollection.org/seasons/X84FvhIAACUAqiqp)

**Serial**
A serial is a type of series, in which articles are scheduled to be published.

**Series**

**Story**
If no format is assigned to an article, its label on the FE defaults to "Story".

**Subject**

**Type (Content Type)**

**Type (Types/Techniques)**

**Technique**

**Webcomic**
Type of article

**Work**

