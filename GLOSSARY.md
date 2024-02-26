# Glossary
## Third parties

**Archivematica** - [A tool for born-digital workflows](https://www.archivematica.org/en/). We use Archivematica to package (+metadata) born-digital content.

**BagIt** - [A standard for packaging digital content](https://datatracker.ietf.org/doc/html/rfc8493). Both Archivematica and Goobi output BagIt-compliant "bags", which are stored in the storage service.

**CALM** - [Archive management software](https://www.axiell.com/uk/solutions/product/calm/) which stores all catalogue data pertaining to archives. These are "harvested" into Sierra every night, but we get archive data from the CALM API directly.

**Digirati** - [An agency](https://digirati.com/) who create/maintain DLCS and contribute to the IIIF standards, who did a lot of the work on wellcomelibrary.org and also helped with our identity/requesting functionality.

**DLCS** - [Our image/IIIF server](https://dlcs.info/), run by Digirati, which provides both the actual asset delivery and the IIIF image APIs.

**Ebsco** - [A provider of library metadata services](https://www.ebsco.com/), named for Mr Elton B. Stephens. They provide e-journal metadata to the catalogue pipeline.

**Encore** - [The "frontend" for Sierra](https://www.iii.com/products/encore/), which was historically used on wellcomelibrary.org. This provided search and other user-facing interfaces; much of our work has been to replace it. 

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
In an effort to ensure everyone uses the same language and help with onboarding, here is a incomplete glossary of the terms used in relation to the website content and its context.
These definitions will apply to all contexts unless otherwise specified (e.g. codebase, UI...)


#### Archive
A work _format_ (twinned with _manuscript_).
An archive is a collection of items, also referred to as records, that have been created or accumulated by a single person, a group or an organisation. [More information can be found on our website](https://wellcomecollection.org/guides/YL9OAxIAAB8AHsyv#what-is-an-archive-).


#### Article
Umbrella term for anything under `/stories`. Could have a format of _story_, a _webcomic_, a _photo essay_...


#### Audience
A _content type_ used for _Events_ & _Exhibitions_ that declares what specific audience it's target to. e.g. "16+" or "Experts".


#### Book
[Example](https://wellcomecollection.org/books/Y7QWrREAAHC43oH0)
Book is a content type in Prismic, displayed on the [Books listing page](https://wellcomecollection.org/books). They are books that are published by Wellcome.


#### Closed stores
One of the _Location_ options, closed stores are places where only staff can go. A a reader has to make a request for items in closed stores.


#### Collection
A complex one, it might be best to refer to [this Gitbook page](https://app.gitbook.com/o/-LumfFcEMKx4gYXKAZTQ/s/18DwJCSD1tjue3OkGDPy/functional-digital-content-style-guide/terminology-all-the-parts-of-wellcome-collection) as it can have multiple meanings in different contexts.


#### Concept
1. Concepts are the units of thought — ideas, meanings, or (categories of) objects and events — which underlie many knowledge organization systems. As such, concepts exist in the mind as abstract entities which are independent of the terms used to label them.
2. We have concept pages which group items (works, images, etc.) linked to the concept (either because they were written by it or about it). [See an example here](https://wellcomecollection.org/concepts/n4fvtc49).


#### Contributor
1. _Contributor_ in data holds two objects, _Contributor_ and _Role_. The former is about the person (their name) and the latter is about the role they held when contributing to a piece. Depending on the content type, it could be the author, a photographer, a curator, a host, etc.
2. So _Contributor_ could refer to either the higher level or the person-level.


#### Content Type
Node type in Prismic, such as Event, Exhibition, Person, Story, etc. This is the higher level node type, which can then have a _format_ to categorise it further if need be.


#### Digital Guide
See _Exhibition guide_.


#### Digital Location
One of the _Location_ options, materials that are available online are identified as such. [Example of an online work](https://wellcomecollection.org/works/a222wwjt).


#### Digitised Item
<!-- TODO Add description -->


#### Event
[Example](https://wellcomecollection.org/events/Y7P3oxEAAHC43k0_)
Displayed in various listing pages, including [Events](https://wellcomecollection.org/events)
<!-- TODO Add description -->


#### Exhibition
[Example](https://wellcomecollection.org/exhibitions/Yv95yBAAAILuCNv6)
Displayed in various listing pages, including [Exhibitions](https://wellcomecollection.org/exhibitions)
<!-- TODO Add description -->


#### Exhibition Guide
[Example](https://www-stage.wellcomecollection.org/guides/exhibitions/Y2omihEAAKLNfLar)
A Prismic _Content type_ that allows the creation of online exhibition guides in multiple formats, such as BSL videos or audio tours.
Also referred to as _Digital Guide_.


#### Format
The options change based on the content type, but for Stories (Articles), for example, it could be Webcomic, Long Read, In Picture&hellip; For an Event, it could be Game, Screening, Workshop&hellip;. They are sometimes referred to as the "type" of [insert content type name].


#### Image Gallery
A component that can be added in a Story (Article). These articles will most likely have the _format_ "In Pictures".


#### In Pictures
A _format_ for a Story (Article) that most likely contains an Image Gallery component.


#### Installation
A type of _exhibition_ or display, generally smaller scale than an exhibition.
Installations are:
- Generally created by an artist, collective, or organisation (_contributor_) as distinct from the curatorial work that is the exhibition
- May be commissioned specifically for the space, or created in response to the space
- Smaller scale than an exhibition
- On display inside or outside the gallery space - is something you can go to
- Needs to appear in a calendar
- May have different date ranges to its associated exhibition


#### Interpretation types
A _content type_'s access offerings, such as "Audio described", "British Sign Language" or "Captions (online)".


#### License/Licence
Tells you how you're able to use the material. For example; [PDM](https://creativecommons.org/publicdomain/mark/1.0/), [CC-BY-NC-ND](https://creativecommons.org/licenses/by-nc-nd/2.0/).
Spelled Licence on the UI (UK spelling) and License in the API.


#### Location
- In works; Where the item can be found. Could be on the open shelves (readily available to readers), or in _closed stores_, as well as online (known as _digital location_).
- In _Events_ & _Exhibitions_ it relates to the _Place_ content type but used as a synonym.


#### Manuscript
[Example](https://wellcomecollection.org/works/a29c8r26)
A work _format_ (twinned with _archive), it is for hand-written material.


#### Photo Story
A Story (Article) content type, which is primarily lead by imagery and supported by text, exploring a single narrative or perspective. The creators of this story type are usually photographers, artists or illustrators. All the imagery in this story type is usually created by one person and the work hangs together as a distinct body of work


#### Place
A _content type_ created for any place/location we might need in an _Event_ or an _Exhibition_, e.g. "Level 1 landing" or "Malet Street Gardens".

#### Role
Part of the _Contributors_ object, defines the type of _contributor_ (author, illustrator, etc.)


#### Season
A season is a grouping of most any _content types_, but primarily events, exhibitions, stories. The idea is that it's a time-limited, curated programme of activities, and it gets promoted as one programme. e.g.: [What does it mean to be human, now?](https://wellcomecollection.org/seasons/X84FvhIAACUAqiqp). They are displayed on `/seasons/[id]`.


#### Serial
A serial is a type of _series_, in which _articles_ are scheduled to be published.


#### Series
1. Events can be grouped into event series: a grouping of events under a regularly occurring singular title/theme (e.g. Exploring Research, Study Days)
2. _Articles_ can be grouped into _Story_ series: a grouping of articles connected thematically. These may be guest edited and include articles written by multiple _contributors_ (unlike a _serial_ which tends to have the same contributor(s) across all articles in the serial).


#### Story
In Prismic, this is the _Content Type_ for _Articles_ (listed at `/articles`). If no format is assigned to an article, its label on the UI defaults to "Story".


#### Subject
<!-- TODO Add description -->



#### Type (Types/Techniques)
<!-- TODO Add description -->


#### Technique
<!-- TODO Add description -->


#### Webcomic
1. Before the _Article_ _Content type_ was created, there was a _Content type_ called Webcomic. 156 webcomics were created before it was disabled and it was added as an _Article_ _format_ instead. The created Webcomics are still visible and searchable, but new ones can't be created.
2. _Format_ of Article


#### Work
This is a complex one, at the time of writing this we have [a ticket](https://github.com/wellcomecollection/wellcomecollection.org/issues/9071) in progress, with some different definitions [listed in a document](https://docs.google.com/document/d/1nAUmwMQen8WuYu7TVz8PxJtp25oYd4Rk1h-5hymUR04/edit). Speak to the team for more information.
