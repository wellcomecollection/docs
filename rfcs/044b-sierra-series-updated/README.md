# Work relationships in Sierra, part 2

This is an update to [RFC-044](../044-sierra-series). What is presented
here is a distillation of our currect understanding of this issue, and the 
practicalities of implementation.

RFC-044 is a year old, and engendered a large amount of discussion, making 
it unwieldy to review. Much of the information in that document is still 
valid, and provides essential context, so it is left intact.

RFC-044 concerns the linking of Works to Series, and of Works to other Works
coming from Sierra.

It is apparent that these are two different things, with two different 
manifestations in the API and Website. Though they do have some common
features.

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

If the title of a 773 field matches one of the Series fields, but it also
contains a $w subfield, then 
__Investigate where this happens in order to decide, before developing a solution__
 * Find out if it ever happens
 * Find out how many objects there are in each "series" where it does happen
 * Ask C&R what it means

### No id, treat as Series

If a 773 field has no id, ($w subfield), then it should be treated as a 
Series link.

### subPart property name

$g - Related parts and $v Volume/Sequential designation are used in the
Sierra data.  Giving them the same name in the API is simpler than
having two different names, forcing a client to first try one then the other
or look at one property if the parent is a Series and another one if the
parent is a Work or Unknown.

### No Nesting of subParts

Whereas hierarchies from CALM data can be arbitrarily deep, and benefit
from nested partOf values, values derived from these fields are 
effectively flat, and of known breadth.

They denote membership of a container, and optionally denote a subPart
within that container.

Semantically, it may be correct to define an object by nesting, but in
practice, using a structure that allows arbitrarily deep and wide nesting
adds unnecessary complexity.

* There is only one parent
* There is optionally one grandparent
* The terminal ancestor is the "important" one.

## Linking a Work to a Series

### Manifestation

These *are not* to be presented within a hierarchy. On the website, 
the name of the series should present as a link to a filtered search
for other objects in the same series.

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
be separated from the series title, and presented in a new field, `subPart`

`830 Published papers (Wellcome Chemical Research Laboratories)
;|vno. 149.`

becomes

```json
"partOf": [
  {
    "title": "Published papers (Wellcome Chemical Research Laboratories) ;",
    "subPart": "no. 149."      
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

In some cases, there is a 773 with a corresponding 830 or 4x0 property.
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

As there is no object corresponding to the parent, there is no symmetrical
`parts` list.

### In Depth

A Series may be something like:  

* a run of books, possibly, but not necessarily, on a common subject.
  * e.g. the Usborne Touchy-Feely series, or Oxford Very Short Introductions
* A grouping of things, possibly from an external source.

These are designated using the 4xx and 8xx codes.

These should not be represented in the same fashion as a CALM hierarchy because:

* There may be very many objects in any given series, 
* There may not be any inherent order, the series is just a bag of items.

However, membership of a series is useful information, as is the ability to 
find other objects from that series.

#### series title and subPart

Separating the subPart from the series title allows us to create an accurate
filtered search. The partOf title is the exact match to use.

##### Why not store it all in title?

Storing the series title and subPart in the same field makes this difficult.

One could expect there to be only one "Published papers (Wellcome Chemical Research Laboratories) ; no. 149",
and at least 149 "Published papers (Wellcome Chemical Research Laboratories)". One would
also expect there to be many Series with titles containing most of those tokens.

* A search for all those tokens would return too many results (anything containing Published, or papers, or Wellcome etc.)
* A search for the exact string would return only one result (i.e. this one)
* A client would have to somehow know how to parse out the subPart to request the right exact phrase (without the benefit of the MARC subfield markers).

#### Other considerations

subPart information may be found in subfield $v - Volume/Sequential designation.

There are also subfields $p (Name of part/section of a work) and $n (Number of part/section of a work)
Both of these are present on at least one example:

[Madame Delait, the bearded woman of Plombières](https://search.wellcomelibrary.org/iii/encore/record/C__Rb1532371__Sfallaize__P0,2__Orightresult__U__X3?lang=eng&suite=cobalt&marcData=Y)

However, in this case, the values do not look useful:

`830  0 Fallaize Collection.|pname of grouping ;|nnumber`

It may be worth investigating whether these subfields ever have useful
information.

In the interest of consistency with Work->Work links (see below), this field
should not have a name like "volume".

## Links from child Works to parent Works

### Manifestation

These *are* to be presented with a hierarchy. On the website, this 
should behave in the same manner as CALM-derived Collection hierarchies.

Order can be determined from the order of 774 properties in the parent object.

### In Depth

A Host Item/Constituent Unit relationship may describe something like:

* Pictures in an album
* A single work published in multiple volumes

## Links from parent Works to child Works

### No ids

Some 774 values have no id, e.g. [Catalogues of Malayan plants, birds and snakes](https://search.wellcomelibrary.org/iii/encore/record/C__Rb3017508__SLists%20of%20snake%20names%20in%20Malay__Orightresult__U__X3?lang=eng&suite=cobalt&marcData=Y)
[Wellcome Malay 8](https://wellcomecollection.org/works/s5cmqb9q) on wellcomecollection.org.


```
LEADER 00000 tm a2200313 a 4500 
008    180202s18uu    my              0   mul   
245 00 [Catalogues of Malayan plants, birds and snakes] 
246 1  MS Malay 8 
505 0  8A. Lists of plants collected in January 1885. Malay in 
       Roman script; uses in English.  -- 8B. Lists of snake 
       names in Malay (Roman script). Notes explaining whether 
       poisonous or not according to Malay and European ideas. 
       The lists are contained in a file and are accompanied by 
       official correspondence regarding whether or not to offer 
       rewards for the destruction of snakes. The lists were 
       prepared in response to a request from Hervey dated 28 
       January 1890. -- 8C. Lists of Malacca birds. Roman script.
       Dated 18 September 1893. -- 8D. Lists of varieties of rice
       and rattan. Roman script. -- 8E. Names of plants. Dated 14
       November 1892. Roman script. -- 8F. Lists of plant names 
       and uses. Roman script. Some English annotation. -- 8G. 
       Lists of grasses collected in Malacca, in a mixture of 
       Arabic and Roman scripts. -- 8H. Names of plants collected
       at Mĕrliman, 12 December 1885. Roman script. Uses 
       described in English. 
510 0  For full details, see 'The Hervey Malay collections in the
       Wellcome Institute' / by R.F. Ellen, M.B. Hooker and A.C. 
       Milner. Journal of the Malaysian Branch of the Royal 
       Asiatic Society, vol. 54, no. 1 (1981), p. 82-92. Also 
       included in 'Indonesian manuscripts in Great Britain: 
       Addenda et Corrigenda' / by M.C. Ricklefs and P. 
       Voorhoeve. Bulletin of the School of Oriental and African 
       Studies, vol. 45, no. 2 (1982), pp. 312-315. 
520    8G comprises four lists of grasses collected in Malacca: 
       G1: 3 pp. Collected by Leman of Malaka Pindah. -- G2: 4 
       pp. Collected by Mata-mata Mahat of Sungei Pĕtei. -- G3: 3
       pp. Collected by Mohamat Amin bin Omar of Pangkalan Rama. 
       -- G4: 3 pp. Collected by Hasan of Sĕlandau. These lists 
       are contained in an official file; a note by Hervey on the
       file, dated 4 April 1891, requests the Assistant 
       Superintendent of Forests to use the '4 best men you can 
       find in the settlement' to obtain the collection. On 15 
       April 1891 Hervey directs that the collection be 'as 
       complete as possible'. 
561    Owned by D. F. A. Hervey; purchased by Wellcome at 
       Hodgsons, London, 23 November 1934. 
599    ol 
650  2 Natural History.|0D019021 
650  2 Botany.|0D001901 
651  0 Malaya. 
655  0 Manuscripts, Malay. 
759    digmalay 
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
907    .b30175082 
956 41 |uhttp://wellcomelibrary.org/item/b30175082|zView online 

```

I don't know what that means. This cannot be presented as any kind of list
of links in a UI, because there is nothing to link to.

However, that object is currently displayed with a Collection Hierarchy,
with poor titling. 