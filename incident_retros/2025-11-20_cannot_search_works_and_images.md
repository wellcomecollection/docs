# Incident retro - cannot search works and images
**Incident from:** 2025-11-20

**Incident until:** 2025-11-20

**Retro held:** 2025-11-20


- [Timeline](#timeline)
- [Analysis of causes](#analysis-of-causes)
- [Actions](#actions)

## Timeline

20 November 2025

See https://wellcome.slack.com/archives/C02ANCYL90E/p1763628741126199 and 

https://wellcome.slack.com/archives/C01FBFSDLUA/p1763629546557789 

8.48 SB created new works index in production cluster. This cause a secret to get recreated in secrets manager<br>
Logic Monitor alerted about this<br>
08.52 RC reports Works API down. Concepts and Content APIs okay<br>
RK Scala app issue if it's not concepts.<br>
SB I recently applied some terraform adding a new experimental work index. I can't see how that would cause this issue, but I'm mentioning it just in case it's connected<br>
RC LogicMonitor first flagged it at 8:50am

9.06 SB I tested the [works] API locally and it works fine so I don't think it's an ES issue<br>
Actually, it might be an ES issue. From the logs, the service can't authenticate<br>
9.08 SB Actually, it might be an ES issue. From the logs, the service can't authenticate:
```
09:06:47.013 [main-actor-system-pekko.actor.default-dispatcher-12] ERROR w.a.s.e.ElasticsearchErrorHandler$ - Sending HTTP 500 from ElasticsearchErrorHandler$ (Unknown error; ElasticError(security_exception,unable to authenticate with provided credentials and anonymous access is not allowed for this request,None,None,None,List(ElasticError(security_exception,unable to authenticate with provided credentials and anonymous access is not allowed for this request,None,None,None,null,None,None,None,List())),None,None,None,List()))
```
 
9.12 RC Catalogue pipeline repo was modified 28mins ago

9.16 RC All tasks have been restarted now, not that it changed anything: https://eu-west-1.console.aws.amazon.com/ecs/v2/clusters/catalogue-api-2021-04-26/services/prod-items-api/tasks?region=eu-west-1 <br>
SB I also restarted the search API just in case<br>
SB I tested the API key used by the catalogue API and it's valid

9.22 RC API fails in staging too (e.g. https://api-stage.wellcomecollection.org/catalogue/v2/works/a2239muq ) , so just local works @brychtas?<br>
SB Yes, I think so. I can use the API locally, connected to the prod index 

9.26 RC Seems to be back. Not images though<br>
The works tasks were re-restarted 5mins ago (not by me) maybe that helped.

9.28 SB I think it's all back now 

9.29 RC Image search still doesn't work for me<br>
SB I think it takes a while due to caching. It works for me in browser private mode now<br>
RC OK it's cache (i'll clear it)<br>
So all good

SB *Something* we did probably fixed it, but I'm not sure what. Apart from restarting the tasks, I also applied the catalogue-api terraform, which applied an older task definition (I don't know why or how the newer one got created) 

9.32 RK API key got updated at 8:48 this morning. <br>
RC That would be it, it alerted at 8:50.<br>
SB That's likely due to the terraform change I applied, which created a new works index. I don't know why that would cause ES to recreate existing API keys though<br>
RK Presuming there was also a Catalogue pipeline terraform update?<br>
Which possibly created a new version of the key, for some reason - old tasks did not have the correct key, the catalogue-api does not have a mechanism to protect against this, so stopped working until the tasks got restarted.<br>
SB Looking at the version history of the ES secret, the previous version was created on October 9, which is when we created the previous experimental works index.<br>
Is it possible that whenever we create a new works index in the terraform stack, Elasticsearch automatically recreates the API keys?
This would imply that creating new indexes in production stacks is unsafe (edited)<br>
RK Don't know why a new key would have got created, perhaps it's that we should work it out - I can guess that the change was hidden in a pile of terraform churn in any apply output.<br>
We can make the Scala APIs resilient to key rotations in any case.<br>
[The fix:] SB I think it was probably the fact that we restarted the services, which allowed them to grab new API keys from Secrets Manager
RC: I don't think my restarts fixed it. The last ones did. Unless it took 10 minutes.<br>
SB: I tried adding yet another works index (just planning, not applying), and terraform does try to recreate the API key:
(This is buried in a long list of terraform changes, so I missed it.)<br>

9.35 RC Total downtime would be about 35mins

9.36 I think we can call this good - if @brychtas agrees with the root cause, this is unlikely to re-occur unexpectedly.

## Analysis of causes

What happened that we didn't anticipate?<br>
Terraform trying to recreate the API key: Catalogue API key got recreated this morning due to a terraform change that was applied, creating a new works index.

whenever we create a new works index in the terraform stack, Elasticsearch automatically recreates the API keys?<br>
This would imply that creating new indexes in production stacks is unsafe

This one change is hidden in lots of lines output.

Why haven’t we seen this before?<br>
Not previously possible to make new indexes w/in the same cluster

## Actions

**Take to Platform planning**
- Re-apply fix to make Terraform output less verbose / make the info we need more obvious
- Health check improvements

**RK**
Make the API resilient for API key changes - done in https://github.com/wellcomecollection/catalogue-api/pull/871 
