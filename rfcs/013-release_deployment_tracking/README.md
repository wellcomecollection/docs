# RFC 013: Release & Deployment tracking

**Last updated: 24 January 2019.**

## Background

We have multiple projects that are themselves composed of multiple services, which can deploy into multiple environments (e.g. production/staging).

Folk are regularly making changes, building updated services and deploying them into the appropriate environments. Keeping track of what is deployed where, by who and why is essential to working effectively.

In general the build/release/deployment process can be described as follows:

![Simple overview](simple_flow.png)

More specifically including a high level view of infrastructure includes:

- A build environment to build artifacts, e.g. Travis
- An artifact store to store things, e.g. ECR
- A database to keep track of what should be released where e.g. DynamoDB
- A Deployment environment to run things in, e.g. ECS

![Infrastructure overvier](high_level_infra.png)

### Glossary

In order that we can talk about the numerous concepts flying about here, we'll define some terms and visualise how they fit together:

- **project:** A high level abstraction, consisting of one or more **service set**'s. Practically this might indicate whole product and should be a single git repository, e.g. the "catalogue" project.

- **service set:** A functional grouping of **services** within a project. e.g. all the services for the catalogue pipeline. You can have multiple per project, for example in the catalogue project, you've got pipeline, api and adapters.

- **service:** Performs a distinct function within a **project**, practically it may be composed of a few closely related containers. e.g. id_minter, requests API, Front-end content app.

- **environment:** Where you deploy your **services** when you want them to run! e.g. staging, production

- **build environment:** Where you build artifacts to deploy, for example CircleCI, Travis, or your local machine (if tooling allows).

- **build:** The process of creating a **build artifact** for a single **service**

- **build artifact:** A deployable _thing_ for a single **service**, practically this is a container image stored in ECR.

- **release hash:** Metadata uniquely identifying a **build artifact**, practically this will be a git ref. 

- **release:** Metadata indicating the intention to deploy a particular **build artifact** at a given **release hash**. Generally part of a **release set**.

- **release set:** A set of **build artifacts** at particular **release hashes** based on a **service set** template that is intended to be released into an **environment** together.

- **deployment:** A deployed **service**.
- **deployment set:** A set of deployed **services** created from a **release set** that has been deployed into an **environment**.

![Terms](terms.png)

## What we do now

See the documentation on [version 1](v1/README.md).

### Problems with the current approach

- It is not clear how to release a single service
- In order to actually deploy something there are multiple steps:
  - Create a release using the CLI tool
  - Deploy a release using the CLI tool
  - Run `terraform apply` to _actually_ update the running services
- Release/Deploy descriptions are not well used / hidden
- Poor visibility of what is actually deployed

### Proposed Solution

We intend to address the problems described above my improving on the existing CLI tool.

We will:

- Provide complete documentation with examples for the updated CLI tool
- Provide "single step" deployment capability in the CLI tool
- Remove the requirement to run `terraform apply` to update existing services
- Provide a web dashboard which shows a current state of releases & deployments
- Extract "descriptions" for releases from commit messages

#### Metadata

.wellcome_project
values in SSM
values in terraform

#### CLI Tool



#### Dashboard



![Terms](proposed_wip.png)
