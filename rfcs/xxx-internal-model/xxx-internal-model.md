# Internal model issues & possible ideas

This RFC is more of a summary of a meeting of pipeline devs that we had on Wednesday 18th of August 2021 that a
fully fledged design & architectural decision. The objective is to make the discussion available for future 
reference especially to people not present at the meeting and to future members of the team.

## Problem
The internal model defines how all the information of a work is encoded in the pipeline. This includes "control" fields 
about the state of the work in the pipeline, as well as "data" fields that are only ever 
read by the API when displaying that information.


All the pipeline services (except the id minter) understand the full internal work model. 
This means that we have to deploy the pipeline as a whole if the internal model changes. If the services don't 
understand the same version of the internal model we might end up with errors, or with data loss.

Most services only need to read a handful of fields of the work in order to perform their functions. 
Good examples of that are the matcher or
the router: the router only needs to read the `collectionPath` field of the work and the matcher needs to read
the identifier and the `mergeCandidates`. But, because most services also forward the information across
to next step in the pipeline, they need to be able to deserialise and serialise it again, and for this reason, 
they need to understand the full model.

Typically, this means that we have to deploy an entire new pipeline and run all the data through the new pipeline in a 
reindex. Because this process is moderately cumbersome and because reindexes are expensive, we tend to merge changes 
into main often without deploying them and then deploy a bunch of changes all at the same time in a new 
pipeline when we feel we have enough for a reindex to make sense.
When that happens, we often discover multiple unrelated problems in the pipeline, and we end up having to "babysit" 
the whole reindex.

Our pipeline is made of a significant number of services, and it's simply not unlikely that 
one of them has a bug in the main branch. But because our services need to understand the same internal model version,
there is no way to go back to a previous working release of a service, if that previous release understood a different
internal model. In this case, if a single service is broken, the whole pipeline is broken.

Ideally, we would like to be in a position where each service needs to be redeployed only when there is a 
change in its source code or a change in the internal model _that is relevant for the service business logic_.
Also, ideally we would like to be able to continuously deploy services in the pipeline independently, 
instead of having to deploy the entire pipeline as a monolith.

Another point worth mentioning, is that we will have to extend the pipeline to support concepts graphs and
denormalisation of them into works. The full scope of this work is not clear yet, 
but it's likely that it will increase complexity of the pipeline further,
making the need for individual services continuous deployment greater.


## Possible solutions

Various solutions have been discussed:

**Continuously deploy into the current pipeline _if the internal model has not changed_**

This is the simplest of mitigations strategies, suggested by Alex, and has already been implemented at 
the time of writing.
It doesn't solve the problems if the internal model changes, but,
since most changes in the pipeline don't necessarily affect the internal model, 
it allows us to test in production more code more quickly and it allows us to check how often 
we actually need to redeploy the entire pipeline because of model changes.

**Deserialise only the part of the work that each service needs**

This is what the matcher and the id_minter do in different ways:
- the matcher reads only the fields that it needs to instantiate a `Work` from elasticsearch (ie only the fields 
that don't have a default value + `mergeCandidates`). The reason why the matcher can do that, is because the matcher
doesn't need to serialise the work to send it the merger, it only needs to send ids that the merger retrieves 
from the source index. Most services, however, need to serialise the work into a different index than the one 
they read from.
- The idminter reads the `Work` as a `Json` object rather than a `Work`, but, because the work state changes in the
id minter and that is encoded as a type change in our model, that means that we have to write ugly
logic to change the circe type disriminator. It's ok as long as it's confined in the idminter, but 
it wouldn't be a good idea to propagate that in all services.

**Send deltas across services instead of entire works**

This was suggested by James initially, and it means that each service, instead of applying its change to the work
and send the modified work, would send the _delta_, the change to apply to the work. The responsibility to apply 
that change would then fall to another "aggregation" service. This aggregation service, which could probably be the 
ingestor, would receive the deltas, retrieve the affected work from the source index and apply the deltas
on the work before serialising into the final index.

This would mean that each service only needs to understand the part of the model that it's interested into and
nothing else, meaning that changes to the model that don't affect it, don't force a deploy of a new release.
It also means that changes to the "data" part of the model, that is only read by the API,
potentially don't need a full reindex, but just a "replay" of the deltas on top of the new model.

One problem with this solution is that it gives the greatest gains if we can always reference the work 
in the source index, but this causes issues in the relation embedder, because it doesn't receive ids of individual
works to look up and modify. Instead, it runs its own query on the merged index to fetch the works, and it 
needs to know which works are redirected in the merging process before denormalising. 
It could be difficult to make the relation embedder fetch the correct works from the source index.

This is a more architectural complicated solution, and it has not been flushed out properly,
so we won't act on it until we are sure of the feasibility and the gains that we would get and weather it would
be useful for the upcoming concepts work