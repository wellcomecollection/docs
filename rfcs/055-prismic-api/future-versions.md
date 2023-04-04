# The future of this endpoint

This document is used to keep track of things we've considered and decided should only be considered in future versions.

- Add a link to digital guides for Exhibitions
- `/books` endpoint
- Add `partOf` as a filter in Stories search. (List of series (e.g. serials - which is a scheduled list of articles, or webcomic series))
- Functional content (`/pages` ?)
- Building upon `/events` and `/exhibitions`, allowing us to have specific Search pages for them.
- is it possible to reuse the availability model we have in the catalogue API for `avaialbleOnline` data in `events` / `exhibitions`?

## Events filters and aggregations

### Filter

- **instantiations.start.from**
  YYYY-MM-DD
- **instantiations.start.to**
  YYYY-MM-DD
- **instantiations.end.from**
  YYYY-MM-DD
- **instantiations.end.to**
  YYYY-MM-DD
- **interpretation**
  Interpretations are useful accessibility tools for event searching. They are, for example: Captioned, BSL, Wheelchair friendly
- **place.label**
  List of physical locations, would also include "Online".
- **format**
  IDs corresponding to [`Session`, `Game`, `Installation`, `Discussion`, `Performance`, `Workshop`, `Chill out`, `Shopping`, `Festival`, `Screening`, `SEND workshop`, `Late`, `Symposium`, `Gallery tour`, `Seminar`, `Study day`, `Walking tour`]
- **partOf**
  Part of a series or season of events
- **audience**
  The public this is geared towards, e.g. Schools
- **contributors.contributor**
  e.g. Facilitator, Host
- **availableOnline**
  Was recorded and the video is made available for a rewatch online.

### Sort

- instantiations.start
- instantiations.end
- relevance

Default sort should be by relevance, with a fallback to id if no query is provided or where documents have the same score.

### Aggregations

- place
- contributor
- format
- audience

## Exhibitions filters and aggregations

### Filters

- **instantiations.start.from**
  YYYY-MM-DD
- **instantiations.start.to**
  YYYY-MM-DD
- **instantiations.end.from**
  YYYY-MM-DD
- **instantiations.end.to**
  YYYY-MM-DD
- **place.label**
  List of physical locations, would also include "Online".
- **contributors.contributor**
  e.g. Filmmaker, Curator
- **format**
  IDs corresponding to [`Permanent Exhibition`, `Season`, `Installation`]

### Sort options

- instantiations.start
- instantiations.end
- relevance

Default sort should be by relevance, with a fallback to id if no query is provided or where documents have the same score.

### Aggregations

- place
- contributor
