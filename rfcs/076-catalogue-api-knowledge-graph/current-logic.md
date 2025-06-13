# Logic and background for Related works queries

There have been [a few different tickets](https://github.com/wellcomecollection/wellcomecollection.org/milestone/78) tackling the desired MVP logic for the [Related works component](https://github.com/wellcomecollection/wellcomecollection.org/tree/main/content/webapp/components/RelatedWorks) and even more conversations around what we think should be queried. Because of the amount of people involved, we thought it best to document those decisions somewhere. It is likely to change and be improved upon.

## Resources
- [Final design and spec](https://www.figma.com/design/6ZvjrD9yhBBZSAXENc8vK4/Related-content-on-Works-pages?node-id=532-7370&p=f&m=dev)
- [Related works component](https://github.com/wellcomecollection/wellcomecollection.org/tree/main/content/webapp/components/RelatedWorks)
- [This .org helpers file](https://github.com/wellcomecollection/wellcomecollection.org/blob/main/content/webapp/components/RelatedWorks/RelatedWorks.helpers.tsx) containing the queries

## Table of contents
- [Related works component](#related-works-component)
- [Current queries](#current-queries)
    - [Subject related queries](#subject-related-queries)
    - [Date range](#date-range)
    - [Types/techniques](#typestechniques)
- [Query changes](#query-changes)
- [Interesting works to consider](#interesting-works-to-consider)
    - [Date range vs date-related subject label](#date-range-vs-date-related-subject-label)
    - [Same results](#same-results)

## Related works component
The component [gets added to a works page](https://github.com/wellcomecollection/wellcomecollection.org/blob/main/content/webapp/pages/works/%5BworkId%5D/index.tsx#L207) if the work has at least one subject label.

## Current queries
The base of all queries lies with the subject labels. If a work does not have any subject labels, we don't query for the others at all, since their results would be too generic.

The queries are split in three categories:
- Subject related
- From the same century (date range) with similar subjects
- Types/Techniques related, with similar subjects

For each query we fetch 4 works, because we want to display 3 and the work being viewed is likely to be returned as a result. We filter it out afterwards.

There can therefore be up of six queries made on each work page.

### Subject related queries
Up to three queries/tabs.
Uses the first three subjects from the response array.

#### Query
- `pageSize: 4`
- `includes: [production, contributor]`
- `subjects.label: the first three subject labels of the work`

### Date range
One query/tab
Used for a "Century" tab, e.g. "From 1900s".

#### Queried if the date is a string made of four numbers. 
Valid:
- `1999`
- `1284`
- `1683`

Not valid:
- `[1928]`
- `1937?`
- `From 1930 to 1934`
- `1933-1954`

If the string is valid, we then use it to [get the century range](https://github.com/wellcomecollection/wellcomecollection.org/blob/main/content/webapp/components/RelatedWorks/RelatedWorks.helpers.tsx#L13-L30).

#### Query
- `pageSize: 4`
- `includes: [production, contributor]`
- `subjects.label: the first three subject labels of the work`
- `production.dates.from: First day of the century`
- `production.dates.to: Last day of the century`


### Types/techniques
Maximum of 2 queries/tabs, but only because we wanted to reduce the amount of total queries. 
The original request was for up to 3 tabs for types and techniques.

We get the first two types/techniques (genres) in the response array:
`genres?.map(genre => genre.label).slice(0, 2)`

So up to two queries are done, by looping through the above's results:

#### Query
- `pageSize: 4`
- `includes: [production, contributor]`
- `subjects.label: the first three subject labels of the work`
- `genres.label: The genre label`

## Query changes
(For Gareth) We used to pass the subject, date or genre label as a keyword search, but removing it seemed to change nothing, so I did. Was that a decision that I shouldn't have touched?

## Interesting works to consider
Throughout our work, we found some works whose related works results made it clear more work would be required on the logic.

### Date range vs date-related subject label
https://wellcomecollection.org/works/a2262ru9
https://wellcomecollection.org/works/a376cmj9

It's strange when one of the subject label is date related, because we then also have the century tab. That can be the same century, or a different work if the work is a modern one about a different century.

### Same results
https://wellcomecollection.org/works/a22xvp3c

Many works will display the same results for most of their tabs. The answer would be to fetch more works and compare and filter, but we chose to not to that at this stage.

