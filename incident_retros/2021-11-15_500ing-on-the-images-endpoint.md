# Incident retro - 500'ing on the /images endpoint

**Incident from:** 2021-11-15

**Incident until:** 2021-11-15

**Retro held:** 2021-11-17

- [Timeline](#timeline)
- [Analysis of causes](#analysis-of-causes)
- [Actions](#actions)

## Timeline

15 November 2021

See https://wellcome.slack.com/archives/C01FBFSDLUA/p1636992374000200 

PR to add thumbnails to API

16:04 catalogue-api-gateway-5xx-alarm
There were 4.0 errors in the API

Alert repeated every 2-3 minutes until 16.57

16.06 AC We are reliably 500'ing on the /images endpoint: 
https://api.wellcomecollection.org/catalogue/v2/images?aggregations=locations.license,source.genres.label,source.contributors.agent.label&pageSize=25&query=aids 

```,Attempt to decode value on failed cursor, List(DownField(type), DownField(thumbnail), DownField(data), DownField(canonicalWork), DownField(source)))```

I suspect this is my change in internal model to make thumbnail a DigitalLocation – the API still expects that value to be a Location, so it’s looking for a type discriminator in type – but the ingestors are no longer setting that, because they see the type as unambiguous

The fix is to roll the version of internal model in the API
merged a change to add the license aggregation to the /images API

16.07 AFC I deployed the pipeline thinking it wasn’t a breaking change
AC also didn’t think it was a breaking change

16.08 JG We’re still serving OK - assuming it’s because it’s only on some records?
AFC I think it’s on everything that has a thumbnail, so quite a lot (edited) 

Couldn’t roll back because it’s on the pipeline side; have to roll the API forward

16.10 AC I would suggest:
1. Roll the internal model in the API
2. Deploy that

I’m 98% sure that will fix it
And I can explain the issue in a bit more detail in a bit

16.26 AC / AFC Some image queries would return a persistent error
or queries that include those images in the results

16.31 AC We used to model `thumbnail: Location`, so it would be serialised as `{…, "type": "DigitalLocation"}` – this is how the API knows which flavour of Location it should deserialise
Now we model `thumbnail: DigitalLocation` so it doesn’t get serialised by the ingestor with the `"type"` value. Then the API code doesn’t know how to interpret it.

16:31
It’s not fixed yet, but it will be shortly

16.49 AC Fix is rolling out now, alerts should be silencing shortly

16.57 catalogue-api-prod-5xx-alarm
There were 2.0 errors in the API

This was the final alert

17:04 NP No alerts for 5 mins ... all okay now?

17:25 AFC sorry natalie, it’s deployed so I think it’s fixed


## Analysis of causes

The pipeline model had moved ahead of API:
Change in internal model to make thumbnail a DigitalLocation – the API still expects that value to be a Location, so it’s looking for a type discriminator in type – but the ingestors are no longer setting that, because they see the type as unambiguous

## Actions

No actions.
