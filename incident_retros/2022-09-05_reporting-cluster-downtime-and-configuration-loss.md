# Incident retro -  reporting cluster downtime and configuration loss

**Incident from:** 2022-09-05

**Incident until:** 2022-09-08

**Retro held:** 2022-09-12

- [Timeline](#timeline)
- [Analysis of causes](#analysis-of-causes)
- [Actions](#actions)

## Timeline

See https://wellcome.slack.com/archives/C3TQSF63C/p1611911159323900 and #wc-reporting-cluster-reconfiguration channel

25 August 2022

11.07: Started a rolling upgrade to 8.4.0 on the reporting cluster

13.04: Upgrade failed in unclear “stuck” state - everything still working fine

26th August

14.41: Opened case with Elastic to resolve stuck state

29th August

08.49: Automated maintenance (presumably to resolve state mismatch) failed, but with no adverse effects.

14.28: Advised by Elastic to delete some non-migrated indices

31st August

15.48: Index migration/removal completed, upgrade still failing and Elastic informed.

4th September

04.05: Another automated system maintenance event - moving nodes around. We think this is the event which started the downtime

“Move nodes off of allocator i-0900f7512ca10119c due to routine system maintenance”

5 September

08.20: Another failed automated maintenance event

09.12: High severity ticket raised with Elastic.

09.24: Elastic start manual recreation of cluster

10.27: Cluster recreation successful.

10.49: Kibana node upgrade started by JP (required manual changes in config)

11.08: Kibana upgrade complete

12.38: JP notifies Elastic that while data indices are present, Kibana saved objects have been lost

14.35: Elastic respond, noting short snapshot retention and unassigned indices being lost.

15:23: Elastic confirm configuration loss.

15.56 JP set up #wc-reporting-cluster-reconfiguration and begins reprovisioning application credentials.

17.13 JP I think all application credentials/roles are now reprovisioned


## Analysis of causes

Snapshot policy for the reporting cluster was set to one hour. This has since been changed to 30 days.

The reporting cluster started as a side project/prototype and should have been checked when we came to rely on it.


## Actions

**Jamie**
- Increase reporting cluster snapshot policy to 30 days - done

**For planning**
- Move reporting cluster config into terraform
