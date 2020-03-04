# CI/CD

Continuous Integration / Continuous deployment

## Deployment

###  Continuous deployment

When test pass against a build in a CI environment those changes are deployed to production.

We need:
- To be satisfied that tests in CI ensure that a build is promotable to production.
- To build on the release tool to ensure the deploy step can actually trigger deployments.
- To connect tests to deployment!

### Deployment visibility

We want to be able to see who deployed what & when in the recent past.

We should provide an authenticated web dashboard showing deployments
We want to know:
- What was deployed, referencing:
  - The PR that was deployed
  - The tests that have been run against the deployed changes (pre/post deployment)
  - The status of a deployment
- When was a change deployed

### Deployment tool 

The release tooling as currently used is too complicated.

We should have a single step deployment tool that takes a deploy-able artifact from a build and deploys it to an environment.

```
> cd my_project
> wellcome_release_tool deploy build123 staging
Congratulations abc123 (PR123, PR345) deployed to staging!
> 
```

## Continuous integration

In order to ensure that developers are able to work quickly and effectively together we should:

- Reduce build times
- Reduce test times
- Provide clear and understandable, well documented build tooling