# Incident Response Protocol


## What's an incident?

An incident is defined here as a severe immediate or short-term potential degredation in the user-facing performance of our services.

Some examples might be:

- Traffic to `wellcomecollection.org` or some part of the site not being served as expected, e.g. "Whats on?" being unavailable or incorrect
- Search APIs being unavailable or serving incorrect data
- A security compromise such as credentials being exposed on the public internet.

An incident must be worked on as soon as possible to mitigate loss of service to users and minimise reputational damage.

## Reporting an incident

An potential incident might be reported in lots of ways (tweet from a user, report from a developer) but should be funneled to a delivery manager to assess the damage and decide whether to call the issue an "incident" or prioritise work via other channels.

There are some situations where a person decides that it is best to initiate the protocol themselves without a delivery manager at first. When this happens, ensure that the delivery manager is informed that this has happened. Some examples of where this might happen

* The incident is small enough to get a rapid fix out
* A delivery manager is unavailable

## Roles

### Incident lead

When it's clear an incident has occured the person responsible is the most senior developer who is available to respond. Who that is can be worked out via Slack in the #wc-platform channel, this person is now the "incident lead" until they pass that role on explicitly to someone else. It is not expected that the most senior developer lead on all incidents, and that role should be handed to the person best placed to lead on a solution.

The incident lead should announce in #wc-platform that an incident has occured, ensuring that the relevant delivery manager is aware of the situation   (and agrees to continue where appropriate). A new Slack channel should be created for that incident, started with description of the problem and what is known at that time.

The incident lead should pull in whoever they need to understand and resolve the problem. All those involved in resolving the incident should report their progress in the shared incident channel. When someone is no longer able to assist or has stopped helping that should also be made clear.

### Supporting colleague

If an incident lead requests your help to resolve an issue, please assist as required reporting your progress in the shared Slack channel. If you are unable to assist or are no longer working on the problem please also make that clear.

### Delivery manager

It's the role of the delivery manager to identify whether a reported issue qualifies as an incident and to mediate the reponse as appropriate. For example a delivery manager may say "we can deal with this later", or "we can call this resolved when X happens".

The delivery manager is responsible for communicating the issue with stakeholders, by taking that action themselves or delegating it as appropriate.

The delivery manager can declare an incident resolved and decide who to prioritise any upcoming work related to it. For example the delivery manager may co-ordinate any clean-up work or schedule a post-mortem for that incident.

## Resolving an Incident

An incident is resolved when the user-facing issue has been resolved or mitigated as far as possible. It's up to a delivery manager to declare/approve an incident resolved, again there may be situations where this is so obvious as to be unnecessary.

In most cases an incident requires a retrospective
