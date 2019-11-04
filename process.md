# Process

**This is a DRAFT, still under consideration by the team**

We follow the OKR process, see the [2019/2020 Delivery Plan](https://wellcomecloud.sharepoint.com/sites/wc2/DE/RoadMaps/Delivery%20Plans/Delivery%20Plan%202019-20%20Digital%20Engagement.pdf?csf=1&e=WUG2dI&cid=56bdefa5-c5d4-44a1-99e7-96a6975d10fc)

Delivery over process - do not follow these guidelines if they prevent you from delivering value as defined by our objectives.

## Projects

Projects are quarterly iterations of the projects [available in Github](https://github.com/wellcometrust/platform/projects).

Issues are binned or recycled on a quarterly basis.

## Pull Requests (PRs)

All Pull Requests should have in general:

- What is the benefit of this change (and for who)
  e.g. In order to make searches better for users
  
- What is the change functionally
  e.g. We've ordered searches by date
  
- What is the change
  e.g. By implementing an update to the `ElasticFlarp GargleMap` in `object FleebChunker`
  
- Relationships to other changes
  e.g. Depends on #123, required for #456

For example:

```
In order to make searches better for users
We've ordered searches by date
By implementing an update to the `ElasticFlarp GargleMap` in `object FleebChunker`

Depends on #123, required for #456
```
 
## Definition of done

You do not need to enumerate these in PRs, but you must be cognisant of them when closing PRs.

To be *done* they require:

- A code review from a non-pairing peer
- An iminent deployment plan 
  i.e. Code has been excercised in a production matching environment
- Testing as appropriate:
  - Acceptance criteria: high level testing functional change.
  - Regression testing (practically this probably means running the existing test suite)
  - Smoke tests (when this change is deployed - does the system it has been deployed to still function as expected)
- Documentation as appropriate
- Review with UX or Product as appropriate

PRs are merged by one of those who worked on the change.

Changes *should* be deployed immediately, or if they are not there *must* be a clear timescale indicated on the PR.
