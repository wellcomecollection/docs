# Work relationships in Sierra

There are various ways to represent relationship between Works in the library and the archive. One example is collections in archives, 
where Works are organized in hierarchy with parents, children and siblings.

In Sierra there are many ways to represent relationships between Works. One of them is series, 
which represent group of Works. Another relationship that is represented in Sierra is the Host Item 
entry and Constituent Unit Entry. Host Item entry links the Work to something that the Work is a part of, which could be for 
example another Work or a serie. Constituent Unit Entry links a Work to something that the Work is composed of, 
for example another Work or a page or chapter of the Work.

There are other ways in sierra to represent Work relationships but this RFC is focusing on these 3 with the aim of defining 
a model for representing these relationships that is flexible enough to be re-used for others.

## MARC representation

### Sierra series
Sierra series are in Marc tag 490 (plus sometimes 830) of the bib record. 
Legacy series are in tag 440 and will me migrated to 490 by collections team.

Based on investigation of the Sierra data done at the end of March 2021, there are 131883 record with a Sierra serie statement.
The biggest serie is 
[Early European Books : Printed sources to 1700 ;](https://search.wellcomelibrary.org/iii/encore/search/C__SEarly%20European%20Books%20%3A%20Printed%20sources%20to%201700%20SMCLN__Orightresult__U?lang=eng&suite=cobalt) with 31956 bibs, followed by
[ACLS Humanities E-Book](https://search.wellcomelibrary.org/iii/encore/search/C__SACLS%20Humanities%20E-Book.__Orightresult__U?lang=eng&suite=cobalt) with 5118.

Series can have volumes in subfield $v. Volume "Collection 3" 
of "Early European Books : Printed sources to 1700 ;" is the biggest in the library and contains 10245 works.
Series can also have identifiers in subfield $l (Library of Congress call number) or $x (ISSN). 
Records with the same identifier in a Serie statement can have different volumes in subfield $v.

### Host Item Entry and Constituent Unit Entry
Host Item Entry is in 773 MARC tag. Host Item entries can have a title, related parts in $g that can be volumes or dates, 
identifers such as ISSN in $x, ISBN in $z or record control number in $w.

At the time of the investigation there are 492529 works with a Host Item entry statement. The Host Item entry with
the most works is "Eighteenth Century collections online" with 182106 works followed by "Early European Books." with 31956 works.

Some records in Host Item Entry overlap partially or entirely with series: "ACLS Humanities E-Book." is in 773 and 830 and 
"Early European Books.” in 773 also nearly completely overlaps with “Early European Books : Printed sources to 1700 ;" in 490.

Not all Host Item entries refer to Series though, like for example 
[1377450](https://search.wellcomelibrary.org/iii/encore/record/C__Rb1377450?lang=eng&suite=cobalt&marcData=Y) which refers to another work. 

Constituent Unit Entry is in 774 MARC tag. Constituent Unit entries can have a title, related parts in $g that can be volumes or dates,
identifiers such as ISSN in $x, ISBN in $z or record control number in $w. There are 760 works with a 774 MARC tag. 

## Proposed modeling
The proposal is to use properties `parts` and `partOf` of the Work model that are already used to represent
archive collections. This is an example of how relations are rendered by the Catalogue API for archive works for
[dq3spb42](https://api.wellcomecollection.org/catalogue/v2/works/dq3spb42?include=parts,partOf):
```yaml
"parts": [
  {
    "id": "fncn55x6",
    "title": "Articles on Nutrition Education",
    "referenceNumber": "PP/DSM/3/1",
    "totalParts": 0,
    "totalDescendentParts": 0,
    "type": "Work"
  },
  {
    "id": "a8hbc266",
    "title": "Articles on Dietetics",
    "referenceNumber": "PP/DSM/3/2",
    "totalParts": 0,
    "totalDescendentParts": 0,
    "type": "Work"
  },
  {
    "id": "qhvzeece",
    "title": "Nutrition Newsletters, Conference Literature etc",
    "referenceNumber": "PP/DSM/3/3",
    "totalParts": 0,
    "totalDescendentParts": 0,
    "type": "Work"
  },
  {
    "id": "cpp2xh99",
    "title": "Articles and Papers on Nutrition",
    "referenceNumber": "PP/DSM/3/4",
    "totalParts": 0,
    "totalDescendentParts": 0,
    "type": "Work"
  },
  {
    "id": "ur5sakg9",
    "title": "\"Nutrition in Britain in the twentieth century\" - PhD thesis",
    "referenceNumber": "PP/DSM/3/5",
    "totalParts": 0,
    "totalDescendentParts": 0,
    "type": "Work"
  },
  {
    "id": "k4vp98bp",
    "title": "Miscellaneous Items",
    "referenceNumber": "PP/DSM/3/6",
    "totalParts": 0,
    "totalDescendentParts": 0,
    "type": "Work"
  }
],
"partOf": [
  {
    "id": "hb9hqd8p",
    "title": "McLaren, Dr Donald S",
    "referenceNumber": "PP/DSM",
    "partOf": [],
    "totalParts": 3,
    "totalDescendentParts": 9,
    "type": "Collection"
  }
],
```
For archive collections, the website renders these as a collapsible hierarchy: ![The collapsible hierachy of the archive the work is part of](archives.png)
Given the size of many series and Host Item Entry that would not be practical in this case, so the proposal 
is for the frontend to choose whether to render the hierarchy base on the Work `WorkType`, which is `Collection` 
in the case of archive Works.

As series and Host Item Entries can have volumes, the proposal is to represent them as Works with a `partOf` field 
containing the Work that they belong to.
Additionally, if a serie or Host Item Entry has an identifier (such as ISSN os ISBn or other) the proposal is 
to mint a canonical identifier in the pipeline and to expose that identifier in the API. 
Finally, the proposal is to model a serie statement or a Host Item Entry with a type `Work`.

### Examples
 
- [1074785](https://search.wellcomelibrary.org/iii/encore/record/C__Rb1074785?lang=eng&suite=cobalt&marcData=Y) 
This is an example of a serie statement in 490 + 830. In this example the information contained in 830 and 490 is 
  exactly the same, so the result is just one statement. 
```yaml
"partOf": [
  {
    "title": "Morphogenesis of the vertebrate brain; 2",
    "partOf": [
      {
        "title": "Morphogenesis of the vertebrate brain",
        "type": "Work"
      }
    ],
    "type": "Work"
  }
]
```
- [3109805](https://search.wellcomelibrary.org/iii/encore/record/C__Rb3109805?lang=eng&suite=cobalt&marcData=Y)
  490 + 773 with slightly different information
```yaml
"partOf": [
  {   //490
    "title": "Early European Books : Printed sources to 170; Collection 4",
    "partOf": [
      {
        "title": "Early European Books : Printed sources to 170",
        "type": "Work"
      }
    ],
    "type": "Work"
  },
  {   //773
    "title": "Early European Books",
    "type": "Work"
  }
]
```

- [3178769](https://search.wellcomelibrary.org/iii/encore/record/C__Rb3178769?lang=eng&suite=cobalt&marcData=Y) 490 + 830 multiple entries + 773
```yaml
"partOf": [
  {   // 490 & 830 with same information
    "title": "Perspectives in Continental philosophy series; no. 39",
    "partOf": [
      {
        "id": "abcdefg",
        "identifiers": [
          {
            "identifierType": {
              "id": "issn",
              "label": "ISSN",
              "type": "IdentifierType"
              },
            "value": "1089-3938",
            "type": "Identifier"
          }
        ],
        "title": "Perspectives in Continental philosophy series",
        "type": "Work"
      }
    ],
    "type": "Work"
  },
  {  // Second 830 with slighly different information
    "title": "Fordham perspectives in continental philosophy",
    "type": "Work"
  },
 {   // 830 & 773 contain the same information
    "title": "ACLS Humanities E-Book.",
    "type": "Work"
  }
]
```
- [2125597](https://search.wellcomelibrary.org/iii/encore/record/C__Rb2125597?lang=eng&suite=cobalt&marcData=Y)
  490 with ISSN + 830 and 773. There are 1037 bibs that have the same ISSN in a serie statement but
  with different volume subfield.
```yaml
"partOf": [
  {   // 490 +830 contain duplicated info
    "partOf": [
      {
        "id": "abcdefg",
        "identifiers": [
          {
            "identifierType": {
              "id": "issn",
              "label": "ISSN",
              "type": "IdentifierType"
            },
            "value": "1064-3745",
            "type": "Identifier"
          }
        ],
        "title": "Methods in Molecular Biology, Methods and Protocols",
        "type": "Work"
      }
    ],
    "type": "Work"
  },
  {   // 773 
    "title": "Springer eBooks",
    "title": "Work"
  }
]
```
- [3001878](https://search.wellcomelibrary.org/iii/encore/record/C__Rb3001878?lang=eng&suite=cobalt&marcData=Y)
  Only 830 with no 490/440 or 773
```yaml
"partOf": [
    {
        "title": "Adamson Collection Wellcome Library", // subfield $a concatenated with $p
        "type": "Work"
    }
]
```
- [1110225](https://search.wellcomelibrary.org/iii/encore/record/C__Rb1110225?lang=eng&suite=cobalt&marcData=Y)
Serie statement in 440 with only the title
```yaml
"partOf": [
    {
        "title": "Monographs on inorganic and physical chemistry",
        "type": "Work"
    }
]
```
- [1204561](https://search.wellcomelibrary.org/iii/encore/record/C__Rb1204561?lang=eng&suite=cobalt&marcData=Y) 440 with id
```yaml
"partOf": [
  {
    "title": "Brill's studies in intellectual history; v. 13",
    "partOf": [
      {
        "id": "abcdefgh",
        "identifiers": [
          {
            "identifierType": {
              "id": "issn",
              "label": "ISSN",
              "type": "IdentifierType"
            },
            "value": "0920-8607",
            "type": "Identifier"
          }
        ],
        "title": "Brill's studies in intellectual history",
        "type": "Work"
      }
    ],
    "type": "Work"
  }
]
```
- [2301867](https://search.wellcomelibrary.org/iii/encore/record/C__Rb2301867?lang=eng&suite=cobalt&marcData=Y) 
  773 not overlapping with series and no id. 
```yaml
"partOf": [
    {
        "title": "Eighteenth Century collections online",
        "type": "Work"
    }
]
```
- [1186777](https://search.wellcomelibrary.org/iii/encore/record/C__Rb1186777?lang=eng&suite=cobalt&marcData=Y) 
  773 with an id in subfield $w which links to another Work in our library (see example below) 
```yaml
"partOf": [
   {
    "title": "Basil Hood. Photograph album; page 9",   
    "partOf": [
      {
        "id": "abcdefgh",
        "identifiers": [
          {
            // identifier from $w
            "identifierType": {
              "id": "???",
              "label": "???",
              "type": "IdentifierType"
            },
            "value": "(Wcat)9175i",
            "type": "Identifier"
          }
        ],
        "title": "Basil Hood. Photograph album",
        "type": "Work"
      }
    ], 
    "type": "Work"
  }
]
```
- [1172977](https://search.wellcomelibrary.org/iii/encore/record/C__Rb1172977?lang=eng&suite=cobalt&marcData=Y) 
  774 with ids (related to above 773)
```yaml
"parts": [
    {
        "id": "abcdefgh1",
        "title": "Charing Cross Hospital: a portrait of house surgeons. Photograph, 1906.",
        "referenceNumber": "Page 5",
        "totalParts": 0,
        "totalDescendentParts": 0,
        "type": "Work"
    },
    {
        "id": "abcdefgh2",
        "title": "Charing Cross Hospital: a portrait of house surgeons. Photograph, 1906.",
        "referenceNumber": "Page 6",
        "totalParts": 0,
        "totalDescendentParts": 0,
        "type": "Work"
    },
    {
        "id": "abcdefgh3",
        "title": "Charing Cross Hospital: a portrait of house surgeons. Photograph, 1906.",
        "referenceNumber": "Page 7",
        "totalParts": 0,
        "totalDescendentParts": 0,
        "type": "Work"
    },
    ...
]
```

- [3017508](https://search.wellcomelibrary.org/iii/encore/record/C__Rb3017508?lang=eng&suite=cobalt&marcData=Y) 
  774 no ids
```yaml
"parts": [
    {
        "title": "Lists of plants collected in January 1885.",
        "physicalDescription": "30 p.; 34 x 21 cm",
        "totalParts": 0,
        "totalDescendentParts": 0,
        "type": "Work"
    },

]
```
