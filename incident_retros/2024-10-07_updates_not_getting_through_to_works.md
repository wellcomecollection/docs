# Incident retro - users cannot login to their accounts on wellcomecollection.org

**Incident from:** 2024-10-07

**Incident until:** 2024-10-10

**Retro held:** 2024-10-11


- [Timeline](#timeline)
- [Analysis of causes](#analysis-of-causes)
- [Actions](#actions)

## Timeline

### Monday 7 October 2024

See https://wellcome.slack.com/archives/C02ANCYL90E/p1728486497236829

14.10 A catalogue-pipeline PR updating the Flyway package to version 7 is merged to main, triggering a deploy process. The id_minter service stops working shortly after.

### Wednesday 9 October 2024

11.03 NC mentioned that edits to a Sierra record from 7 October are not yet showing up on our site in #wc-platform-feedback

RK checked dashboard and saw no problem with DL queue

~ 14.00 AR also reported updates not showing

RK checked his previous work with id minter

16.09 RK id minter has 1.09k messages on the queue - oldest message was from ~14.00 on Mon 7 Oct

16.13 RK updates are piling up at the id_minter [as a result of bumping flywaydb from 4.2 to 10.18]

RK increased the window for the queue to 14 days from 24 hours

Thu 10 October 2024

10.30ish Deploy delayed by failing ingestor images tests

11.50 Deployed PR to reconfigure to Flyway to use the previous schema version table name<br>
DL queue messages consumed and processed

## Analysis of causes

Flyway stores its own table in the database for tracking schema changes. In version 4, the default name for this table was schema_version. However, in version 5, the default changed to flyway_schema_history.

We recently updated to Flyway 7, which resulted in Flyway not being able to find this table (because it was looking for the new default name). 

PR deploy delayed by failing tests

Messages had been there for a day which shouldn’t happen

ID minter service wasn’t stable


## Actions

**RK**
- Manually re-run updates to pick up changes from Mon 7 afternoon for specific items if requested (in progress)

**TBC - take to next planning**
- Run a reindex to pick up changes from Mon 7 afternoon
- Update monitoring so this isn’t missed again
    - Surface date of oldest message
    - Show the status of deployment service

