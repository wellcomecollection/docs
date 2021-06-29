# Incident retro - slow search 

**Incident from:** 2021-06-28

**Incident until:** 2021-06-28

**Retro held:** 2021-06-29

- [Timeline](#timeline)
- [Analysis of causes](#analysis-of-causes)
- [Actions](#actions)

## Timeline

28 June 2021

11.51 AC kicked off reindex into 06-28 index

13.28 Reindex kicked off a second time

Restarted later for a third time

15.16 Alert Down: Front End Works Search (Origin)
Recovery: Front End Works Search (Origin)

CCR was paused, which reduced load on API cluster, which caused the issue to stop

15.21 Comms sent out via status page

Waited 5 mins to check the issue was resolved

15.33 Incident resolved

## Analysis of causes

- Hard to keep an eye on reindexing
- Looked okay in the morning, because the ingestor wasn’t doing anything, which wasn’t obvious
- Cross-cluster replication whilst reindexing
- How easy is it to find performance metrics?

## Actions

**AC**
- Improve the following/unfollowing process

**RK**
- Document the process 
- Include links to performance metrics that work for anyone who needs them

**JG**
- Propagate Elastic alerts to Slack:
    - Alert on CPU load
    - Alert on CCR




