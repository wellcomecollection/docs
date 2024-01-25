# RFC 050: Service healthcheck principles

## Background

At the moment the healthcheck endpoints for our services report either ok (20x response) or not (anything else). This has 2 places of impact, with varying effects:

when new tasks are bought up during a deployment of a new change, the ECS deployment system (via the load balancer) uses these to check if that task is healthy and can serve request.

- If it passes for all tasks i.e. the change doesn't consistently break the service the deployment succeeds.
- If it fails consistently, the deployment fails and this failure is not exposed to consumers.

At the moment wellcomecollection.org specifically is not well protected by the health checks because they don't check the app itself is healthy before serving traffic.

The 2nd way health checks have impact is:
- when an existing task part of a stable deployment with previously healthy tasks starts failing.
  - if the healthchecks for a task fail as part of a stable deployment that task will be taken out of service and a new task launched to replace it.
    - If the failure cannot be rectified by a task relaunch (i.e. is not caused by some state held by the running task) the next task will also fail and so on. Alarms will go off because our updown checks will report we can't serve requests. We'll serve confusing cloudfront errors to users.
  - If the healthcheck succeeds it sticks around and continues to serve traffic.
    - This is business as usual most of the time.
    - If the application fails to serve requests but reports successful health checks, we will see updown alerts, and may serve slightly less confusing errors to users if these come from the app. I think this is the case with the most recent prismic errors.
    - In the case that the new succeeding task replaces a previously failing task, e.g. by restarting it refreshed some credentials that had expired this is positive as the restart fixed a real problem. Alarms may not go off unless we have metrics that record the problem, or the failed requests meet the existing threshold to alert.

## Proposal

Perhaps we could have health checks that discern if an error requires a task restart and record metrics that can be alarmed on if it does, and that the service itself can react to rather than just restarting. e.g.
- wellcomecollection.org notices that prismic (or content-api, catalogue-api) requests are failing, and can add a notice to the UI that we know there's a problem and are looking at it, but continues to report a 2xx health check so it doesn't restart.
- items api notices that it can't talk to sierra, records metrics that cause alarms to go off but reports healthy so it can continue to serve items requests that don't require a call to sierra
- works api notices it can't talk to elasticsearch, might as well give up and restart as no useful work can get done and this might be down to a change as part of a deployment breaking things that we don't want to go out

At the moment the healthchecks i'm adding are all naive, i.e. they don't check anything else apart from that the app itself has started and if they fail a task is restarted, but we could have something smarter that consists of:
- probes that check behaviour of the service
- scheduled internal healthcheck that checks on the status of probes and makes a decision as to whether a restart is required, and sends metrics on failure where this isn't already the case
- external healthcheck endpoint that reports 2xx or not based on internal health-check decision and gives the status of the probes so a dev (or other system) can read them and react
