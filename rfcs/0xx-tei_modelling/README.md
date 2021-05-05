# TEI Modelling

TEI is a standard for describing sources in any script or language. It is used at Wellcome to 
describe manuscripts in non-latin languages. 

This RFC explores how to represent the information contained in TEI files in our Work model. 

### TEI cataloguing mapping
## Identification
| TEI| API |
| ----------- | ----------- |
| msIdentifier/idno | identifiers |
| msIdentifier/idno | ReferenceNumber |
| msIdentifier/altIdentifier | identifiers |
## Description
| TEI| API |
| ----------- | ----------- |
| titleStmt/title | title |
| mscontents/summary | description |
## Notes
| TEI| API |
| ----------- | ----------- |
|textLang	| notes [language]	|
## Access Conditions?
| TEI| API |
| ----------- | ----------- |
|	|	|
## Parts

| TEI | API |
| ------|---|
|msContents/fileDesc| parts |
## Examples

- [Javanese_10](https://github.com/wellcomecollection/wellcome-collection-tei/blob/master/Javanese/Javanese_10.xml)
```yaml
{
  "id": "abcdefgh",
  "identifiers": [
    {
      "identifierType": {
        "id": "sierra-system-number",
        "label": "Sierra system number",
        "type": "IdentifierType"
      },
      "value": "b30464298",
      "type": "Identifier"
    },
    {
      "identifierType": {
        "id": "sierra-identifier",
        "label": "Sierra identifier",
        "type": "IdentifierType"
      },
      "value": "3046429",
      "type": "Identifier"
    },
    {
      "identifierType": {
        "id": "tei-identifier",
        "label": "TEI identifier",
        "type": "IdentifierType"
      },
      "value": "Javanese_10",
      "type": "Identifier"
    }
  ],
  "languages": [
    {
      "id": "jv",
      "label": "Javanese",
      "type": "Language"
    }
  ],
  "referenceNumber": "Wellcome Javanese 10",
  "description": "Fragments, mainly on mysticism and divination.",
  "physicalDescription": "Javanese paper.",
  "parts": [
    ???
  ],
  "type": "Work"
}
```

- [Wellcome_Batak_36960](https://github.com/wellcomecollection/wellcome-collection-tei/blob/master/Batak/Batak_36960.xml)
```yaml
{
  "id": "abcdefgh",
  "identifiers": [
    {
      "identifierType": {
        "id": "sierra-system-number",
        "label": "Sierra system number",
        "type": "IdentifierType"
      },
      "value": "b30697232",
      "type": "Identifier"
    },
    {
      "identifierType": {
        "id": "sierra-identifier",
        "label": "Sierra identifier",
        "type": "IdentifierType"
      },
      "value": "3069723",
      "type": "Identifier"
    },
    {
      "identifierType": {
        "id": "tei-identifier",
        "label": "TEI identifier",
        "type": "IdentifierType"
      },
      "value": "Wellcome_Batak_36960",
      "type": "Identifier"
    }
  ],
  "languages": [
    {
      "id": "btx",
      "label": "Karo-Batak",
      "type": "Language"
    }
  ],
  "referenceNumber": "MS Batak 36960",
  "description": "11 bamboo strips with inscriptions in Karo-Batak orthography, threaded on a string. 
                  Used for divination from the numerical value of syllables.
                  One strip has the syllabary with an indication of the numerical value of each syllable, the other ten have texts such as: 
                  if the value is one, two, etc. an offering of . . . should be brought in order to assure luck.",
  "physicalDescription": "???",
  "parts": [
    {
       
    }
  ],
  "type": "Work"
}
```

- [Wellcome_Malay_3](https://github.com/wellcomecollection/wellcome-collection-tei/blob/master/Malay/Wellcome_MS_Malay_3.xml)
```yaml
{
  "id": "abcdefgh",
  "identifiers": [
    {
      "identifierType": {
        "id": "sierra-system-number",
        "label": "Sierra system number",
        "type": "IdentifierType"
      },
      "value": "b14850151",
      "type": "Identifier"
    },
    {
      "identifierType": {
        "id": "sierra-identifier",
        "label": "Sierra identifier",
        "type": "IdentifierType"
      },
      "value": "1485015",
      "type": "Identifier"
    },
    {
      "identifierType": {
        "id": "tei-identifier",
        "label": "TEI identifier",
        "type": "IdentifierType"
      },
      "value": "Wellcome_Malay_3",
      "type": "Identifier"
    }
  ],
  "languages": [
    {
      "id": "ms",
      "label": "Malay",
      "type": "Language"
    }
  ],
  "referenceNumber": "Wellcome Malay 3",
  "description": "Charms and demonology. Though the term \"demonology\" is used in the manuscript itself, the creatures being described are known in Malay as \"hantu\",
  which differs from the Western conception of demons in that the term is commonly used to describe spirits and mythological creatures in general, both
  malicious and not. Though some may also be called demons or syaitan in the Islamic sense, not all hantu are necessarily demonic.",
  "physicalDescription": "Multiple manuscript parts collected in one volume.",
  "parts": [
    {
       
    }
  ],
  "type": "Work"
}
```