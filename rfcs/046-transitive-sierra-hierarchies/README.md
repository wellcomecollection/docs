# Transitive hierarchies in Sierra

## The problem

This RFC originates from [this issue](https://github.com/wellcomecollection/platform/issues/5479).

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

A new stage, operating on works-merged (both read and write), triggered by the Router on encountering a document with 
a collectionPath and a sourceIdentifier with an identifierType of sierra-system-number.

The new stage will:

* Take the first and last segments of the path
  * e.g. given a path, `root/branch/leaf` - it will use `root`, and `leaf`.
* Run a wildcard search for records whose last segment matches the first segment of this record.
  * e.g. `*/root`
  * This should only match one record, if there are more, log an error and do nothing.
* Replace the first segment in this record with the collectionPath of that record.
* Run a term search for records with a collectionPath matching the last segment
  * collectionPath is a path_hierarchy, so in the example above, this will match any records with a path that start with `leaf`
* Replace the first segment in those collectionPath, with this record's collectionPath
  * e.g. a path `leaf/1/2` would become `root/branch/leaf/1/2`

## Other Candidate Solutions

I have considered trying to squeeze this into the behaviour of other stages.  The two most obvious places are 
the transformer, and the relation embedder.

It is inappropriate to place this in the transformer, because transformers operate on a single input document to 
produce a single output document.  This behaviour requires multiple inputs, and can have multiple outputs.

It is inappropriate to place this in the relation embedder, because it would add inappropriate complexity to an otherwise 
stable application that is good at turning a full path into a hierarchy. We would need to add behaviour to 
match the right partial paths and to sum up depth values.

Modifying the collectionPath in the database appears to be the simplest way to achieve this.

## Worked example
The transformer constructs a path by concatenating the `w` subfield in a `773` field, with the value of the document's
own `001` field.  It will also create a path from just the `001` field if the document has `774` fields in it.

Given the documents in the introduction, after the transformer, we will have the following collectionPaths:

1. 3303244i
2. 3303244i/3288731i
3. 3288731i/534631i

Before the relationEmbedder, we want `3288731i/534631i` to be `3303244i/3288731i/534631i`.  There are six scenarios
to consider.

* 1,2,3
* 1,3,2
* 2,3,1
* 2,1,3
* 3,1,2
* 3,2,1

Whenever the actual root is encountered, there is no change, because the job of this application is to replace 
a segment of path with the path from the root to that segment.

This means that out of those six scenarios, there are really only two - 
* 2,1
* 1,2

### 1,2
`3303244i/3288731i` is encountered, root is `3303244i` leaf is `3288731i`, no change
`3288731i/534631i` is encountered, root is `3288731i`, `*/3288731i` returns `3303244i/3288731i`, it becomes `3303244i/3288731i/534631i`

### 2,1
`3288731i/534631i` is encountered, root is `3288731i`, leaf is `534631i` no change.
`3303244i/3288731i` is encountered, leaf is `3288731i`, which returns the `3288731i/534631i` record and changes it to `3303244i/3288731i/534631i`

### What about deeper hierarchies?

This is only expected to have to work on 3-level hierarchies, but the same pattern follows.  
If there are 4 levels, then there are 6 possibilities (because the arrival of the root document does not matter).

Given a full path: 0/1/2/3, the paths in each document will be:
* 0
* 0/1
* 1/2 (which needs to become 0/1/2 before the relation embedder)
* 2/3 (which needs to become 0/1/2/3 before the relation embedder)

#### 1,2,3
`0/1` - no change
`1/2` - `*1` finds `0/1`, this becomes `0/1/2`
`2/3` - `*2` finds `0/1/2`, this becomes `0/1/2/3`

#### 1,3,2
`0/1` - no change
`2/3` - `*2` finds nothing, `3` finds nothing
`1/2` - `*1` finds `0/1`, this becomes `0/1/2`, `2` finds `2/3` and changes it to `0/1/2/3`

#### 2,3,1
`1/2` - no change
`2/3` - `*2` finds `1/2` this becomes `1/2/3`
`0/1` - `1` finds `1/2/3` and changes it to `0/1/2/3`

#### 2,1,3
`1/2` - no change
`0/1` - `1` finds `1/2` and changes it to `0/1/2`
`2/3` - `*2` finds `0/1/2` this becomes `0/1/2/3`

#### 3,1,2
`2/3` - no change
`0/1` - `*0` finds nothing, `1` finds nothing
`1/2` - `*1` finds `0/1`, this becomes `0/1/2`, `2` finds `2/3`, and changes it to `0/1/2/3`

#### 3,2,1
`2/3` - no change
`1/2` - `*1` finds nothing, `2` finds `2/3` and changes it to `1/2/3`
`0/1` - `1` finds `1/2/3` and changes it to `0/1/2/3`

## In depth rationales

### Reading and writing to the same DB

Existing stages progress the state of a document and move it to a new database. However, this stage will read and 
write from works-merged.

By operating on the same database, and not progressing state, we can avoid having to change the behaviour of the 
downstream stage, and we will not have to pull-then-push data that does not change.  The most common case will be
that data will not change, so this approach would be more efficient than the existing approach.



