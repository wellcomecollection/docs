## Pipeline merging
### What should the pipeline be doing?

A few cases to remind ourselves what the behaviour of the whole pipeline should be when merging things:

- A:1 -> B:1 if A:1 is the canonical results in:
    - A:1 merged with B:1
    - B:1 redirected to A:1
 
- A:1 -> B:1 -> C:1 if A:1 is the canonical results in:
    - A:1 merged with B:1 and C:1
    - B1: redirected to A:1
    - C:1 redirected to A:1
 
 - assuming the previous case has happened, an update comes for B:2 which no longer links to C:1:
    - A:1 merged to B:2
    - B:2 redirected to A:1
    - C:1 no longer redirected 

### How this currently works

#### Matcher
The matcher receives individual works and updates stores the state of the graph.

- It receives A:1 which says that A:1 -> B:1
    - it stores the link A:1 -> B1
    - it stores A:1 and B:1 as belonging to the same component AB
    - it sends `[[A:1, B:1]]` to the merger
- It receives B:1 -> C:1
    - it stores the link B:1 -> C:1
    - Updates A:1, B:1 And C:1 as belonging to ABC
    - it sends `[[A:1, B:1, C:1]]` to the merger
 - It receives B:2 breaking the link to C:1
    - it stores B:2 with no links removing the link to C:1
    - Updates A:1, B:2 ad belonging to AB
    - it sends `[[A:1,B:2],[C:1]]` to the merger

#### Merger
The merger reads the ids and versions received by the matcher from the recorder store 
and decides if and how to merge based on internal rules. If it decides to merge it updates the works as:
- Fills `numberOfSources` field on the work selected as target with the number of works merged into it
- Modifies all the other works as redirected poiting to the target

if it decides not to merge, it sends the works unchanged

##### Previous behaviour
At some point (ie probably a few weeks ago) the merger used to send a `merged` boolean flag
 to the ingestor that basically indicated if the work had been tampered with by the merger.

#### Ingestor
Because updates to works can get to the ingestor out of order, the ingestor assigns a version 
to each work. Works are ingested if they're version is greater or equal than the one already present 
in the index.
 
The version is calculated as based on the transformer version and the number of 
sources: `transformerVersion*1000 + numberOfSources`.

This means that 
- a new `transformerVersion` always gets ingested
- a work for the same `transformerVersion` and more sources gets ingested if there 
are already works with the same `transformerVersion` but less sources

##### Previous behaviour
The ingestor used to calculate the version as `transformerVersion * 10 + (merged?1:0)`
This meant that 
- a new `transformerVersion` always got ingested
- an out of order updates from the merger for the same `transformerVersion` might have been ingested 
incorrectly cause they would have all the same elastic search version
- unlink kind of worked because `merged` would have been set to `true` so, given 
elastic search greater or equal than versioning, the unlinked version would have been 
ingested (provided no message out of order issues)


### Problems

There are a number of issues with the current approach:
- We need to multiply `transformerVersion` by 1000 to make it take precedence 
over `numberOfSources` because `numberOfSources` can be quite high (650 is the recorded max).
 If we don't do that we run into data consistency problems in the index. 
 As we add more sources we will find ourselves incrementing this number regularly
- The unliking case only works if the update that causes the unlink is on the target work,
 therefore incrementing `transformerVersion`. If, as in the example above, the update is on a
  work that gets redirected to the target, it won't be reflected in the API
- The ingestor is responsible for figuring out the version based on information passed on
 by the merger. This causes coupling between the merger and the ingestor. The ingestor is 
 currently aware of merging happening at some point, which it shouldn't be. It also makes the 
 versioning logic very hard to follow and modify

### Discarded ideas

Jamie and I came up with multiple ideas to tweak the current behaviour, each one with some problems:
- Go back to the `merged` flag: it has issues with multiple sources and it has issues 
with images versioning because image versions are derived from works
- Add unlink in the version function like 
`(transformerVersion * 10000) + (unlinked?1:0)*1000 + numberOfSources`: 
bleurgh and also when something is ingested as unlinked it's impossible to override 
it unless the `transformerVersion` changes
- Use something like the sum of all `transformerVersion`s of all works sent by the matcher: 
this would succeed in unlinking, but again would fail to add a work to a group 
that was the result of a previous unlink operation


### Solution proposed

The solution suggested by Nic is that we pass through in the work a field with the timestamp 
of the last update.
The merger should then use the maximum of the timestamps of all works sent by the matcher 
as the version for each of the works.
The ingestor should use greater than versioning instead of greater or equal.
 
The updated timestamp needs to be recorded in the adapter in different ways depending on the source:
- Sierra: the sierra API already provides a timestamp with down to the second granularity 
for each update and the Sierra adapter already stores it in the Sierra VHS. The sierra transfomer can 
read this value and copy it into the work. 
- Miro: Miro data doesn't change so can just set it to zero in the transformer
- Calm: Calm data has a `retrievedAt` field in the Calm VHS. It comes from the HTTP header 
of the response from the Calm API. Because of this a lot of Calm records have the same timestamp
 of when the first harvest was done. This could cause consistency issues if none of the works in 
 the group has a more recent updated date because all of the updates sent by the merger will have 
 the same version. 
 There is also a `Modified` field which indicates when the record was modified in Calm, but it has a 
 down to the day granularity. The proposal is to use `retrievedAt` and revisit if we find issues.
- METS: there is currently no info about when a bag was created/updated in the adapter store. 
However, this is provided by the storage service in the `createdDate` field in the bag response, so we can change the adapter to read and store this. This requires an adapter change and a VHS migration
