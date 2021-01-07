# RFC 025: Tagging our Terraform resources

**Last updated: 29 May 2020.**

## Problem statement

We manage our infrastructure in Terraform, but our Terraform configurations are split:

* Across many repositories
* Across multiple directories within each repository

This keeps each configuration small, so it can be planned and applied faster. It also creates a hard gap between unrelated services -- for example, a change in the storage service shouldn't affect the catalogue pipeline.

However, this approach can make it hard to find the definition of any particular resource.

If you're looking at a resource in the console, you should be able to tell:

* Is this resource managed in Terraform?
* If so, where is the corresponding Terraform configuration?

## Solution

We are going to tag resources in a Terraform configuration like so:

```text
tags = {
  TerraformConfigurationURL = "https://github.com/wellcomecollection/:repo_name/:configuration_path"
}
```

The tag will point to a URL where you can find the Terraform configuration. Every resource in a configuration will have the same tag -- this is a clue, rather than an exact file reference.

## Notes

* We are going to tag as many resources as we can do quickly, but the goal is not 100%. Trying to tag every last resource could get very fiddly, and the added value drops off quickly.
* Because we tend to put staging and production resource in separate configurations, these tags will start to give us a way to break down costs among services.
* We are not going to tag resources with a named, responsible individual -- we all have collective responsibility for the platform. If there are resources that only person understands or can maintain, that is a problem we need to fix.

