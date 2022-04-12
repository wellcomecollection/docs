# Transitive hierarchies in Sierra

## The problem

Most Sierra records that result in a hierarchy (See ../45-sierra-work-relationships), exist in a two-level
hierarchy, i.e. a single parent, and one or more children.  However, there is a desire to represent a deeper hierarchy.

With these two-level Sierra hierarchies, each record is able to independently construct its collectionPath to the root
of the hierarchy, because the root is its parent.

The Fallaize Collection is being catalogued in a more CALM-like fashion, with the top-level 
object providing context, and items are then described in logical groups (which may correspond to physical folders).
For example, "Studio portraits of women" contains some photographs, each of which is a portraits of a woman in a studio.

In this case, the objects know they are in the logical group, and the logical group knows it is in the Fallaize 
collection, but the ends know nothing of each other.

https://search.wellcomelibrary.org/iii/encore/record/C__Rb3303244?lang=eng&marcData=Y

```
774 0  |tA metal and timber box (chest, trunk), once the property
       of E N Fallaize.|w540972i 
774 0  |tStudio portraits of women.|w3288731i 
```

"Studio portraits of women" is part of Fallaize Collection, and contains several individual portraits

https://search.wellcomelibrary.org/iii/encore/record/C__Rb3288731?lang=eng&marcData=Y

```
773 0  |tThe Fallaize Collection.|w3303244i 
774 0  |tA young woman posing naked, in front of a painted 
       backdrop in a photographic studio.|w534631i 
...
```

The individual portraits are part of "Studio portraits of women"

https://search.wellcomelibrary.org/iii/encore/record/C__Rb1531585?lang=eng&marcData=Y
```
773 0  |tStudio portraits of women.|w3288731i 
```

The knowledge that any of these individual portraits is part of the Fallaize Collection can only be known once all three
levels have been ingested by the pipeline.  Because of this, the completion of the hierarchy for these records
needs to be deferred until then.

This is currently only to serve the Fallaize Collection, but may be required by other items in the future, e.g. boxes of
ephemera, where there is currently no clickable journey from an individual object to the series the box is part of.

## Proposed Solution

## Other Candidate Solutions

