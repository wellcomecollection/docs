# Incident retro - search not available

**Incident from:** 2021-09-20

**Incident until:** 2021-09-20

**Retro held:** 2021-09-22

- [Timeline](#timeline)
- [Analysis of causes](#analysis-of-causes)
- [Actions](#actions)

## Timeline

20 September 2021

See https://wellcome.slack.com/archives/C01FBFSDLUA/p1632152123024700  

16.32 Updown alert for:
Front End Works Search (Origin)
Front End Works Search (Cache)

16.35 DM: I’ve just deployed, but server routing for works is broken. I’ve got the fix and think we should be able to roll forward

16.39 JP yeah tempted to say we roll back for now

16.40 NP put a message about the search issue in #wc-platform-feedback

16.41 DM has a PR https://github.com/wellcomecollection/wellcomecollection.org/pull/7062/files 

16.43 JP I’ve started a rollback here btw; can’t do any harm even if we get that PR in

16.44 JP But I do think we should wait to check stage before promoting [the PR fix]

16.45 Updown recovery for:
Front End Works Search (Origin)
Front End Works Search (Cache)

16.46 NP Okay, looks like I can search again. [Fixed by the rollback, not the PR]
Also said search was working in #wc-platform-feedback

## Analysis of causes

A deployment caused server routing for works to break, and end to end tests didn’t catch the problem on stage.

## Actions

**DM**
- Add render tests for the catalogue app top-level pages [#7063](https://github.com/wellcomecollection/wellcomecollection.org/pull/7063) DONE
- Create a runbook for front end incidents

**JG**
- Investigate why end to end tests didn’t break on all pages





