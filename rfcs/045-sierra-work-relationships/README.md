# RFC 045: Work relationships in Sierra, part 2

This RFC is a continuation of the work started in [RFC-044: Sierra Series](044-sierra-series).

**Last modified:** 2022-02-21T15:06:55+00:00

## Context

This is an update to the original [RFC-044: Sierra Series](044-sierra-series). What is presented
here is a distillation of our current understanding of this issue, and the 
practicalities of implementation.

RFC-044 is a year old, and engendered a large amount of discussion, making 
it unwieldy to review. Much of the information in that document is still 
valid, and provides essential context, so it is left intact.

These RFCs concern the linking of Works to Series, and of Works to other Works
coming from Sierra.

It is apparent that these are two different things, with two different 
manifestations in the API and Website. Though they do have some common
features.

## Summary

At the broadest level, there are three features to be added resulting from this RFC.

* Linking of Works to Series
* Linking of parent Works to child Works
* Linking of child Works to parent Works

## API change

This requires a change to the API:
* `id` is currently required in partOf objects, it needs to be optional.
* a new field needs to be added to part and partOf objects: `partName`

## Preliminary Work

We must ensure that the website will not attempt to render inappropriate
hierarchies when we start adding new part/partOf relationships.

## Staged development proposal

1. All parent relationships described in this document to be displayed as series links. 
   - This includes 773 relationships with identifiers, which will eventually link between Works.
   - The partName ($g or $v) is ignored
2. Improve handling of identified Work->Work links for hierarchical display.
3. Improve handling of asymmetric partOf links to link directly by id.
4. Display the partName if desired.

This approach allows us to first deliver an improvement to the linking of
as many records as possible, and then iterates over _how_ that linking
can be improved for those records where we have more information.

It also represents a cone of uncertainty.  It is clear that we want to link
from Works to Series via a filtered search for the Series title.  The 
correct presentation of links between parent and child works is less clear. 
In particular, how best to handle asymmetric links.
The value of presenting the partName text to users is not clear.

## Relevant MARC fields

* [440 - Series Statement/Added Entry-Title](https://www.loc.gov/marc/bibliographic/bd440.html)
* [490 - Series Statement](https://www.loc.gov/marc/bibliographic/bd490.html)
* [773 - Host Item Entry](https://www.loc.gov/marc/bibliographic/bd773.html)
* [774 - Constituent Unit Entry](https://www.loc.gov/marc/bibliographic/bd774.html)
* [830 - Series Added Entry-Uniform Title](https://www.loc.gov/marc/bibliographic/bd830.html)


## Common features

### Most Precise Wins

The 773 field is not restrictive about what it can point to, whereas the 4x0 and 830 
fields explicitly refer to a Series.  Records with a 773 field that matches
one of the series fields should ignore the 773 field and just present it
as a Series link. 

Where a 773 field does not match one of the Series fields, then it 
is treated as a partOf in its own right.

If the title of a 773 field matches one of the Series fields, but it also
contains a $w subfield, then 
__Investigate where this happens in order to decide, before developing a solution__
 * Find out if it ever happens
 * Find out how many objects there are in each "series" where it does happen
 * Ask C&I what it means
 
### partName property name

The subfields `$g - Related parts` and `$v Volume/Sequential designation` are used in the
Sierra data in 773/774 and 440/490/830 fields, respectively.  
Giving them a common name in the API is simpler than
having two different names, forcing a client to first try one then the other
or look at one property if the parent is a Series and another one if the
parent is a Work or Unknown.

### No Nesting of part/partOf

Whereas hierarchies from CALM data can be arbitrarily deep and broad, 
and benefit from nested `partOf` and `part` values, 
values derived from these fields are effectively flat. Although the 
first layer in either may be arbitrarily broad (multiple parents/children), 
the next layer would have maximally one value.

In addition, where `$g` or `$v` are used, the immediate parent/child as proposed in
the original RFC is of less importance, being a volume number or page number.

They denote membership of a container, and optionally denote some kind of subsection
within that container.

Semantically, it may be correct to define an object by nesting, but in
practice, using a structure that allows arbitrarily deep and wide nesting
adds unnecessary complexity to both server and client.

For each field value from Sierra creating a partOf object

* There is optionally one grandparent
* The terminal ancestor is the "important" one.

And the same is true In a part relationship derived from these fields:

* Each child optionally has one child
* The terminal descendant is the "important" one.

Using nesting in this situation would mean that a client would have to 
iterate to find terminal ancestors/descendants.  This pattern may be clear to 
Wellcome Collection developers, but not obvious to external consumers of the API.

## Linking a Work to a Series

### Manifestation

These *are not* to be presented within a hierarchy. On the website, 
the name of the series should present as a link to a filtered search
for other objects in the same series.  The behaviour of the API will need 
to be updated in order to support filtering partOf by `title` as well as `id`
as it currently does.

In the API, this should be represented in a partOf value with no id, and a 
type of "Series", thus:

```json
"partOf": [
  {
    "title": "Fallaize Collection.",
    "type": "Series"
  }
]
```

A MARC value may have a subfield denoting a "part" of the series, this should
be separated from the series title, and presented in a new field, `partName`

In the case of 830, 430 nd 490 fields, this is in the $v subField.

`830 Published papers (Wellcome Chemical Research Laboratories)
;|vno. 149.`

becomes

```json
"partOf": [
  {
    "title": "Published papers (Wellcome Chemical Research Laboratories) ;",
    "partName": "no. 149."      
    "type": "Series"
  }
]
```

Some 773 entries do not have a $w subField, e.g. [Think of Me](
https://search.wellcomelibrary.org/iii/encore/record/C__Rb2058813__Smontage__Ff:facetmediatype:k:k:Pictures::__P0,9__Orightresult__U__X3?lang=eng&suite=cobalt&marcData=Y
) 

```
773 0  |tJames Gardiner Collection: Romantic fantasy and comic 
       postcards, and photographs on gender and masculinity.|q3a 
```

These should be treated as a Series.

```json
"partOf": [
  {
    "title": "James Gardiner Collection: Romantic fantasy and comic postcards, and photographs on gender and masculinity.",
    "type": "Series"
  }
]
```

In some cases, there is a 773 with a matching 830 or 4x0 property.
This should result in only one partOf.

```
773 0  |tACLS Humanities E-Book.|nURL: http://
           www.humanitiesebook.org/
830  0 ACLS Humanities E-Book.
```

```json
"partOf": [
  {
    "title": "ACLS Humanities E-Book.",
    "type": "Series"
  }
]
```

A record may be part of multiple Series, e.g. [Derrida after the end of writing](https://search.wellcomelibrary.org/iii/encore/record/C__Rb3180411__S%20Fordham%20perspectives%20in%20continental%20philosophy__Orightresult__U__X3?lang=eng&suite=cobalt&marcData=Y):

```
773 0  |tACLS Humanities E-Book.|nURL: http://
       www.humanitiesebook.org/ 
830  0 Fordham Perspectives in Continental Philosophy. 
830  0 ACLS Humanities E-Book. 
```

This will result in a partOf entry for each series.

As there is no object corresponding to the parent, there is no symmetrical
`parts` list.

### In Depth

A Series may be something like:  

* a run of books, possibly, but not necessarily, on a common subject.
  * e.g. the Usborne Touchy-Feely series, or Oxford Very Short Introductions
* A grouping of things, possibly from an external source.

These are designated using the 4xx and 8xx codes, and (normally) only identified by name.

These should not be represented in the same fashion as a CALM hierarchy because:

* There may be very many objects in any given series, 
* There may not be any inherent order, the series is just a bag of items.

However, membership of a series is useful information, as is the ability to 
find other objects from that series.

#### series title and partName

Separating the partName from the series title allows us to create an accurate
filtered search. The partOf title is the exact match to use.

##### Why not store it all in title?

Storing the series title and partName in the same field makes this difficult.

One could expect there to be only one "Published papers (Wellcome Chemical Research Laboratories) ; no. 149",
and at least 149 "Published papers (Wellcome Chemical Research Laboratories)". One would
also expect there to be many Series with titles containing most of those tokens.

* A search for all those tokens would return too many results (anything containing Published, or papers, or Wellcome etc.)
* A search for the exact string would return only one result (i.e. this one)
* A client would have to somehow know how to parse out the partName to request the right exact phrase (without the benefit of the MARC subfield markers).

## Links from child Works to parent Works

### Manifestation

These *are* to be presented with a hierarchy. On the website, this 
should behave in the same manner as CALM-derived Collection hierarchies.

Order can be determined from the order of 774 properties in the parent object.

The value of partName should be extracted from the $g subfield, if present.

If the relationship is asymmetric, there should be no hierarchy. The
child should link to the parent Work in such a way as to allow the 
user to find other children of that parent.

### In Depth

A Host Item/Constituent Unit relationship may describe something like:

* Pictures in an album or montage (e.g. Basil Hood)
* Articles in a Journal (e.g. Edinburgh Medical and Surgical Journal)
* A single work published in multiple volumes? (I don't have any examples of this)

#### 773 without corresponding 774

Given a Work A that has a 773 that refers to Work B, but Work A is not listed as
a 774 of Work B, there is insufficient information to attempt to render 
a hierarchy.

Some articles in the [Edinburgh Medical and Surgical Journal](https://search.wellcomelibrary.org/iii/encore/record/C__Rb1311219__SEdinburgh%20medical%20and%20surgical%20journal__Orightresult__U__X8?lang=eng&suite=cobalt&marcData=Y)
Refer to the journal, with an id in a 773 field ($w subfield), e.g. [Notice of an instance of molluscum chronicum](
https://search.wellcomelibrary.org/iii/encore/record/C__Rb1363769__Snotice%20of%20an%20instance%20of%20molluscum%20chronicum__Orightresult__U__X7?lang=eng&suite=cobalt&marcData=Y
). A search for [Edinburgh Medical and Surgical Journal](https://search.wellcomelibrary.org/iii/encore/search/C__SEdinburgh%20medical%20and%20surgical%20journal__Orightresult__U?lang=eng&suite=cobalt)
yields over 1000 hits, which indicates that this should behave more like a Series link
(though this could include other matches, not just articles in the journal).

These are to be treated as a Series.

## Links from parent Works to child Works
### Manifestation

These *are* to be presented with a hierarchy. On the website, this
should behave in the same manner as CALM-derived Collection hierarchies.

Whether to include the partName in the display value can be decided on 
implementation.

The value of partName should be extracted from the $g subfield, if present.

In the API, this will manifest in the `parts` list.

This extract from the [Basil Hood Photograph Album](https://search.wellcomelibrary.org/iii/encore/record/C__Rb1172977__Sbasil%20hood__P0,1__Orightresult__U__X6?lang=eng&suite=cobalt&marcData=Y)
```
...
774 0  |gPage 6 :|tCharing Cross Hospital: a portrait of house 
       surgeons. Photograph, 1906.|w(Wcat)28916i 
774 0  |gPage 7 :|tCharing Cross Hospital: a portrait of house 
       surgeons. Photograph, 1906.|w(Wcat)28922i 
774 0  |gPage 7 :|tCharing Cross Hospital: a portrait of house 
       surgeons. Photograph, 1906.|w(Wcat)28924i 
...
```
becomes
```
  "parts":[
    ...
    {
      "id": "[canonical id derived from](Wcat)28916i"
      "partName": "Page 6"
      "title": "Charing Cross Hospital: a portrait of house surgeons. Photograph, 1906."
    },
    {
      "id": "[canonical id derived from](Wcat)28922i"
      "partName": "Page 7"
      "title": "Charing Cross Hospital: a portrait of house surgeons. Photograph, 1906."
    },
    {
      "id": "[canonical id derived from](Wcat)28924i"
      "partName": "Page 7"
      "title": "Charing Cross Hospital: a portrait of house surgeons. Photograph, 1906."
    }
    ...
  ]
```

Where a 774 field has no id associated, these are to be ignored.
e.g. `774 1  |tLists of snake names in Malay.|h4 p.; 34 x 21 cm`

### In Depth

#### 774 without id

Some 774 values have no id, e.g. [Catalogues of Malayan plants, birds and snakes](https://search.wellcomelibrary.org/iii/encore/record/C__Rb3017508__SLists%20of%20snake%20names%20in%20Malay__Orightresult__U__X3?lang=eng&suite=cobalt&marcData=Y)
[Wellcome Malay 8](https://wellcomecollection.org/works/s5cmqb9q) on wellcomecollection.org.

This cannot be presented as any kind of list of links in a UI, because there is nothing to link to.

This example is a TEI manuscript, so the data for the API comes from there
rather than Sierra, so the Sierra data can safely be ignored.

```
245 00 [Catalogues of Malayan plants, birds and snakes] 
246 1  MS Malay 8 

...

774 1  |tLists of plants collected in January 1885.|h30 p.; 34 x 
       21 cm 
774 1  |tLists of snake names in Malay.|h4 p.; 34 x 21 cm 
774 1  |tLists of Malacca birds.|h6 p.; 34 x 21.5 cm 
774 1  |tLists of varieties of rice and rattan.|h2 p.; 34 x 21 cm
774 1  |tNames of plants.|h2 p.; 34.5 x 20 cm 
774 1  |tLists of plant names and uses.|h3 p.; 34.5 x 21.5 cm 
774 1  |tLists of grasses collected in Malacca.|h13 p.; 34 x 21 
       cm 
774 1  |tNames of plants collected at Mĕrliman.|h9 p.; 34 x 21 cm

```
## Unanswered Questions

### Worldcat ids

Because it may be difficult to match a worldcat id to an id in the pipeline, it may be simpler to
check for symmetry by title.
e.g.
Having found a record with a 774 field containing an identifier
```
246 1  My Made Up Title
...
774 1 |tSome part of the main thing |g page 4 |w (Wcat)12345
```

Search for the document with the title from the 774.

```
246 1  Some part of the main thing 
...
773 1 |tMy Made Up Title |g page 4: |w (Wcat)54321
```
Having found that that document contains a 773 with the title of the main document, we can then link them.

### Other potential partName subfields

There are also subfields $p (Name of part/section of a work) and $n (Number of part/section of a work)
Both of these are present on at least one example:

[Madame Delait, the bearded woman of Plombières](https://search.wellcomelibrary.org/iii/encore/record/C__Rb1532371__Sfallaize__P0,2__Orightresult__U__X3?lang=eng&suite=cobalt&marcData=Y)

However, in this case, the values do not look useful:

`830  0 Fallaize Collection.|pname of grouping ;|nnumber`

It may be worth investigating whether these subfields ever have useful
information.

### Punctuation between subfields.

MARC data is designed to be printed out verbatim (after stripping subfield tags), so fields and subfields often contain
punctuation to permit this, e.g. the colon and semicolon at the ends of subfields in these two examples.

`830 Published papers (Wellcome Chemical Research Laboratories) ;|vno. 149.`
`774 0  |gPage 6 :|tCharing Cross Hospital: a portrait of house surgeons. Photograph, 1906.|w(Wcat)28916i`

Ideally, these separators would not be presented unless the fields are output together.  We will need to iterate
towards the correct way to trim them.

Note that the order of subfields is defined in the data, so the full string cannot be simply reconstructed from 
individual fields.

It may be the case that we need to store the whole field as a separate string for presentation, as well as storing the
main or title field to facilitate linking.
