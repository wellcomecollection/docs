# Incident retro - search not available

**Incident from:** 2021-07-27

**Incident until:** 2021-07-27

**Retro held:** 2021-07-29

- [Timeline](#timeline)
- [Analysis of causes](#analysis-of-causes)
- [Actions](#actions)

## Timeline

27 July 2021

See https://wellcome.slack.com/archives/C01FBFSDLUA/p1627393042010200 

14.37 Updown alert DOWN for:
- Front End Works Search (Origin)
- Works API Single Work
- Works API Search
- Images API Single Image
- Images API Search
- Front End Single Work Page (Origin)
- Front End Single Work Page (Cached)
- Front End Works Search (Cached)
- Wellcome Images Redirect

JP asked if anyone knew what was going on

JG: I just ran the user script
RK: which one?
 
14:38 Does that update existing users
./scripts/create_elastic_users_catalogue.py
https://github.com/wellcomecollection/catalogue-api/blob/main/terraform/shared/scripts/create_elastic_users_catalogue.py

14.39 JP: it does [update existing users]; it’s an elastic auth error

`Sending HTTP 500 from ElasticsearchErrorHandler$ (Unknown error; ElasticError(security_exception,unable to authenticate user [search] for REST request`

RK: cycling the api services will cause them to come back with the new secrets?

14.40 JG: That should work
Or we can try update the passowrd, but I am not sure where from.
Happy to unless someone else is doing it>?

Done by RK?

14.43 RK: the logs look ok
have to wait for the new tasks to register
JP: I think we need to wait for the target groups to become healthy, no?

14.44 Statuspage alert sent

14: 45 RK did the same for items and staging

14.44 Updown alert UP for:
- Front End Single Work Page (Origin)
- Images API Search
- Front End Works Search (Origin)
- Works API Single Work
- Works API Single Image
- Works API Search
- Wellcome Images Redirect
- Front End Single Work Page (Cached)
- Front End Works Search (Cached)

14.46 JG: Do we know why stage-search is still 3?

RK: because it never got scaled back down?

14.47 Statuspage alert sent - issue resolved

RK: related discussion: https://wellcome.slack.com/archives/C3TQSF63C/p1625487082309500 

> RK: I’m very tempted to remove the terraform script provisioner for the catalogue-api work, as I think there are some situations where it is dangerous. We could for example update the password for search inadvertently by updating a dependent TF resource - that would trigger a password update that running services would not pick up automatically.

that script should prevent you from dropping the old passwords if they exist, or at least prompt you.


## Analysis of causes

- We ran a user script that updated users without fully understanding what the script did, and had stuff in it that would break 

## Actions

**JG**
- https://github.com/wellcomecollection/catalogue-api/pull/212 - DONE
- https://github.com/wellcomecollection/catalogue-api/pull/208 - DONE
- https://github.com/wellcomecollection/catalogue-api/pull/211 - DONE
- Continue to work on the user provisioning so that it works safely as expected, including password rotation

**RK**
- Alerts for requesting and items 

**JP**
- Scale down the stage catalogue API ECS services
- Investigate why desired_count in ECS services does not update ECS




