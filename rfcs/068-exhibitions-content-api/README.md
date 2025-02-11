# RFC 068: Exhibitions in Content API
Exhibitions are to be added to Events search, becoming Events & Exhibitions search. We'll therefore be working on indexing Exhibitions in a more intentional manner. 
That indexing and subsquent API endpoint will power the Events & Exhibitions search as well as, eventually, the existing listing pages.

## Indexing Exhibitions
I can think of two ways to go about indexing Exhibitions for ranking against Events to make sense and be easier to handle.

### Exhibitions-only index
- We create a new index (`exhibitions`) and index exhibition documents in there.
- We then create a new endpoint (`events-exhibitions`?) that [searches through both the events and the exhibitions index](https://www.elastic.co/guide/en/elasticsearch/reference/current/search-multiple-indices.html).
- We use that endpoint in `/search/events`.

Meaning that the `/events` endpoint can then still be used for events listing pages, and a separate new one for exhibitions can be used in exhibitions listing pages.

This feels cleaner and clearer, but might end up meaning duplicate work (e.g. we want to support a new field). 

### Exhibitions added to Events index
- We pull Exhibitions in the existing `events` index, with something marking them as `Exhibitions`, possibly the `format` field (see [Format](#format) section below).
- Individual listing pages (`/events`, `/exhibitions`) would be rendered using a filter to ensure only the relevant ones are displayed.

It would simplify the work when adding filters or maintaining the indices, only doing it once, but is possibly harder to maintain in the long run, should the two content types grow apart or more complicated.

## Decision on Exhibition indexing
The Experience team has discussed the above and is leaning heavily upon the first option: a new index for Exhibitions. We like the clarity and flexibility it offers.


## Format
All exhibitions will fit under the Format filter "Exhibition":
<img src="./event-type-filter.png" alt="Event type filter" style="max-width: 400px;" />

but their format on the card (yellow label) will be the Exhibition Format that was selected in Prismic (e.g. Display, Installation...):
<img src="./exhibition-card.png" alt="Exhibition cards" style="max-width: 550px;" />

Meaning the value of "format" should differ in the `filter` and `aggregrations` objects versus the `display` object.

I suggest we make the Exhibition format queryable, so keeping the Exhibition format in the `query` object.


## API response
TODO
`/exhibitions/[exhibitionId]`:
`/exhibitions`:
`/events-exhibitions`:


## Front-end integration decisions
- Exhibitions should use [the same rendering component on the Front-end](https://github.com/wellcomecollection/wellcomecollection.org/blob/main/content/webapp/components/EventsSearchResults/index.tsx) (will there be renaming to do?), with the required tweaks where displayed fields differ (e.g. "Now on" dot).
- Search tab title to be changed from "Events" to "Events & Exhibitions".
- Metadata copy changes to include exhibitions.

Aside from the last two, we're not refferring to Exhibitions anymore. Within search, exhibitions are considered to be a type of Event. So:
- No change to search events URL (`/search/events`).
- "Event type" filter keeps its name.
- The future date filter will also just mention events, for example "all future events".


### Out of scope but have been discussed
- Redirect `events/past?availableOnline=true` to `/search/events?isAvailableOnline=true`. The other listing pages stay as is as they serve a different purpose than the search page.