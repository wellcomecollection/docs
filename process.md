# Process

**This is a DRAFT, still under consideration by the team**

We follow the OKR process, see the [2019/2020 Delivery Plan](https://wellcomecloud.sharepoint.com/sites/wc2/DE/RoadMaps/Delivery%20Plans/Delivery%20Plan%202019-20%20Digital%20Engagement.pdf?csf=1&e=WUG2dI&cid=56bdefa5-c5d4-44a1-99e7-96a6975d10fc)

Delivery over process - do not follow these guidelines if they prevent you from delivering value as defined by our objectives.

## Rituals

* _Quarterly planning_: Higher level planning happening once a quarter to decide product changes to meet objectives.
* _Fortnightly refinement_: Bringing higher level issues into scope for work, creating sub-issues for that work.
* _Fortnightly retrospectives_: Reflecting on work in the previous fornight, what worked, what didn't, how to optimise.
* _Ad-hoc retrospectives_: Retrospectives focussed on incidents or topics of special interest.

## Projects

Projects are quarterly iterations of the projects [available in Github](https://github.com/wellcometrust/platform/projects).

Issues are erased or recycled on a quarterly basis.

## Projects, Issues & Pull Requests \(PRs\)

Projects, Issues & PRs overlap in GitHub, here is how we think about them:

* Issues & PRs are both _change requests_.
* A PR is the unit of deployment, i.e. PRs should be deployable in isolation \(where possible\).
* PRs reference a set of git commits which in totality describe a coherent functional change.
* Issues reference one or more PRs which together describe a coherent functional change.
* Github Projects contain Issues _or_ PRs which transition through defined states towards _done_.

Project state:

* _no state assigned_: unassigned PRs / issues serve as a record of intended upcoming work \(subject to quarterly erasure\).
* **Triage** \(assigned to a project but _stateless_\): awaiting assignment at backlog refinement.
* **To do**: available to be worked on before the next refinement cycle
* **In progress**: actively being worked on right now
* **Done**: released! Meets the specification for done \(see below\).

## Issue / PR requirements

All change requests should have in general:

* What is the benefit of this change \(and for who\) e.g. In order to make searches better for users
* What is the change functionally e.g. We've ordered searches by date
* What is the change A brief overview of the implemention where useful e.g. This is an update to the `ElasticFlarp GargleMap` in `object FleebChunker`.
* Relationships to other changes e.g. Depends on \#123, required for \#456

For example:

```text
In order to make searches better for users
We've ordered searches by date
By implementing an update to the `ElasticFlarp GargleMap` in `object FleebChunker`

Depends on #123, required for #456
```

## Definition of done

You do not need to enumerate these in PRs, but you must be cognisant of them when closing PRs.

To be **done** they require:

* A code review from a non-pairing peer
* An iminent deployment plan 

  i.e. Code has been excercised in a production matching environment

* Testing as appropriate:
  * Acceptance criteria: high level testing functional change.
  * Regression testing \(practically this probably means running the existing test suite\)
  * Smoke tests \(when this change is deployed - does the system it has been deployed to still function as expected\)
* Documentation as appropriate
* Review with UX or Product as appropriate

PRs are merged by one of those who worked on the change.

Changes **should** be deployed immediately, or if they are not there **must** be a clear timescale indicated on the PR.

