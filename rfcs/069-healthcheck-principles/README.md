# RFC 050: Service health-check principles

This RFC explores how we should implement health-checks in our services, specifically around services that have HTTP interactions / are serviced by load-balancers that implement health-checking.

## Background

At the moment the health-check endpoints for our services report either OK (20x response) or not (anything else). This status in impactful in 2 modes of operation:

1. **During deployment:** When new tasks are bought up during a deployment of a new change, the ECS deployment system (via the load balancer) uses these to check if that task is healthy and can serve request.

    - **If it passes for all tasks:** the deployment succeeds.
    - **If it fails consistently:** the deployment fails and this failure is not exposed to consumers.

    **Note:** In the past many of our services have not been well protected by health checks because they only checked for a HTTP OK response from nginx (reverse proxy in front of the app), or rely only on establishing a successful TCP connection. They do not check the application itself is able to serve HTTP requests as it would in normal operation.

2. **Instability in an existing deployment:** When an existing task part of a stable deployment with previously healthy tasks starts failing.

    If the health checks for a task fail as part of a stable deployment that task will be taken out of service and a new task launched to replace it. This can result in the following outcomes:

      - **Ephemeral issue:** If the health check for the new task succeeds it sticks around and continues to serve traffic. The problem has been "resolved", e.g. by restarting we refreshed some state that had become invalid.
        
        Alarms may not go off unless we have metrics that record the problem, or the failed requests meet the existing threshold to alert.

      - **Task cycling:** If the failure cannot be rectified by a task relaunch (i.e. is not caused by some state held by the running task) the next task will also fail and so on. 
      
        Alarms will go off because our up-time checks will report we can't serve requests. We'll serve confusing cloudfront errors to users.

      - **Zombie tasks:** If the application fails to serve requests but reports successful health checks.
      
        We will see up-time alerts, and may serve slightly less confusing errors to users if these come from the app. We have seen this on `wellcomecollection.org` when onward requests for content from Prismic have failed because of an issue with their service.
  

## Proposal

Health checks that indicate if an error requires a task restart and record metrics that can be alarmed on if it does, and that the service itself can react to in the case a restart would not be useful. For example:

- `wellcomecollection.org` notices that Prismic (or Content API, Catalogue API) requests are failing, records metrics to trigger alarsm and adds a notice to the UI that we know there's a problem and are looking at it, but continues to report a 2xx health check to the ALB so it doesn't restart.

- Items API notices that it can't talk to Sierra, records metrics that cause alarms to go off but reports healthy to the ALB so it can continue to serve items requests that don't require a call to sierra.

- Works API notices it can't talk to Elasticsearch, might as well give up and restart as no useful work can get done and this might be down to a change as part of a deployment breaking things that we don't want to go out.

[Current work to add health-checks is naive](https://github.com/wellcomecollection/wellcomecollection.org/issues/10545), i.e. they don't check anything else apart from that the app itself has started and if they fail a task is restarted. 

We could have something smarter that checks the critical functionality of the application, and only reports unhealthy where that critical function cannot be fulfilled. 

This could be implemented simply by:

- Health checks which exercise a single critical happy path e.g. make a request to Elasticsearch.

A more complicated solution could include:

- Probes that check behavior of the service
- Scheduled internal health-check that checks on the status of probes and makes a decision as to whether a restart is required, and sends metrics on failure where this isn't already the case
- External health check endpoint that reports 2xx or not based on internal health-check decision and gives the status of the probes so a dev (or other system) can read them and react
