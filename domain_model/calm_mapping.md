# Archive catalogue mapping

## Identification

| Calm            | API             | Status |
|:----------------|:----------------|:------:|
| Level           | workType        |   ✅   |
| RefNo           | identifiers     |   ✅   |
| AltRefNo        | identifiers     |   ✅   |
| AltRefNo        | referenceNumber |   ✅   |
| Bnumber         | identifiers     |   ✅   |
| PreviousNumbers | identifiers     |   ✅   |

## Description

| Calm         | API                 | Status |
|:-------------|:--------------------|:------:|
| Title        | title               |   ✅   |
| Description  | description         |   ✅   |
| CreatorName  | contributors        |   ✅   |
| Date         | production          |   ✅   |
| Language     | languages           | In development |
| Extent       | physicalDescription |   ✅   |
| UserWrapped6 | physicalDescription |   ✅   |
| Subject      | subjects            |   ✅   |

## Notes

| Calm                   | API                  | Status |
|:-----------------------|:---------------------|:------:|
| Arrangement            | notes [arrangement]  |   ✅   |
| AdminHistory           | notes [biographical] |   ✅   |
| CustodHistory          | notes [ownership]    |   ✅   |
| Acquisition            | notes [acquisition]  |   ✅   |
| Appraisal              | notes [appraisal]    |   ✅   |
| Accruals               | notes [accruals]     |   ✅   |
| Language               | notes [language]     |   In development   |
| RelatedMaterial        | notes [related]      |   ✅   |
| PublnNote              | notes [publications] |   ✅   |
| UserWrapped4           | notes [finding-aids] |   ✅   |
| Copyright              | notes [copyright]    |   ✅   |
| ReproductionConditions | notes [terms-of-use] |   To be removed by https://github.com/wellcomecollection/platform/issues/4773 |

## Access conditions

On `locations.accessConditions`:

| Calm             | API             | Status |
|:-----------------|:----------------|:------:|
| AccessStatus     | status          |   ✅   |
| AccessConditions | terms           |   ✅   |
| ClosedUntil      | to [closed]     |   ✅   |
| UserDate1        | to [restricted] |   ✅   |
