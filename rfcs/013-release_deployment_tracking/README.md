# RFC 013: Release & Deployment tracking

**Last updated: 24 January 2019.**

## Background

We run a lot of applications. People are regularly making changes and deploying new code. In order that we don't get confused about what code is deployed where we should track what is deployed where, by whom, and for what reason.

The build/release/deployment process can be described as follows:

![Simple overview](simple_flow.png)

A high level view of infrastructure includes:

- A service that creates build artefacts from a given version of the codebase, e.g. creating a Docker image (a *build environment*)
- A store for the created artefacts, e.g. Docker images (an *artefact store*)
- An environment where services can run, e.g. ECS or Kubernetes (a *deployment environment*)
- A database that tracks what version of each application is running

![Infrastructure overvier](high_level_infra.png)

### Glossary

- **project:** The top level, consisting of one or more **service set**'s. This might indicate whole product and should be a single git repository, e.g. the catalogue project.

- **service:** Performs a distinct function within a **project**. e.g. id_minter, requests API, Front-end content app.

- **service set:** A functional grouping of **services** within a project. You can have multiple per project, for example in the catalogue project, you've got pipeline, api and adapters.

- **build:** The process of creating a **build artifact** for a single **service**

- **build artifact:** A deployable _thing_ for a single **service**, e.g. a docker image or zip file.

- **release hash:** Metadata that allows us to work out what version of the code was used to create a given build artifact, e.g. the Git commit hash.

- **release:** Metadata indicating the intention to deploy a particular **build artifact** at a given **release hash**. Generally part of a **release set**.

- **release set:** A set of **build artifacts** at particular **release hashes** based on a **service set** template that is intended to be released into an **environment** together.

- **deployment:** A deployed **service**.

- **environment:** Where you deploy your **release sets** when you want them to run e.g. staging, production.

- **deployment set:** A set of deployed **services** created from a **release set** that has been deployed into an **environment**.

#### How these terms fit together

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

#### Moving away from terraform for deployment

We currently use `terraform apply` to deploy services at a particular release hash. The choice to use terraform was driven by a requirement to describe our task definitions in code. 

Separating service deployment from infrastructure deployment is desirable as infra/service deployments have differing concerns and pace, i.e. high-value infrequent (infra), vs. low-value frequent (deploying new versions of services). 

Running terraform in a CI environment like Travis is also not desirable as giving an automated environment the power to run infrastructure updates needs careful consideration.

#### Why this is hard

An ECS task definition contains configuration for volume mounts, CPU & memory requirements, as well as indicating the container image URI to use when creating tasks.

The container image URI cannot be updated independently from other parameters in a task definition. This makes ignoring a change to the task definition difficult, see this [epic GitHub issue thread](https://github.com/terraform-providers/terraform-provider-aws/issues/632).

When terraform updates a task definition it has a version of the task definition in code to send to ECS, the ECS Service is then updated by terraform to point at that new task definition and a deployment is started in ECS.

However if the task definition is updated and differs from that recorded by the terraform state (which updating the image URI _would_ cause) terraform will attempt to return the task definition to a known state, which would be undesirable.

In order to move away from using `terraform apply` it will be necessary to decouple updating the task definition from deploying updated services.

### Proposed Solution

We intend to address the problems described above my improving on the existing CLI tool.

We will:

- Provide complete documentation with examples for the updated CLI tool
- Provide "single step" deployment capability in the CLI tool
- Remove the requirement to run `terraform apply` to update existing services
- Provide a web dashboard which shows a current state of releases & deployments
- Extract "descriptions" for releases from commit messages

#### General approach

Use consistent image URIs based on tagged environments in task definitions e.g. stage, prod - these will not change - terraform will not update task defs.

Update what those URIs point at, then force a redeployment where the new images referenced will be used.

**TODO** this needs a diagram

#### Register images

A build tags images with their git ref first and that tag pushed to ECR, then tagged with latest and pushed. 

We will provide the ability to do this with the CLI tool so that all the code is one one place _phrase that better_

#### Deploying

Record your intention to deploy which images (by git ref tag AND image digest), to which environment. Create a deployment ID (sequential INT) - new db row. @@need to search by env, date, project@@ 

To deploy copy the image tags you want to deploy to an environment tag and push that to ECR. @@this will probably just be copy out of latest@@ 

Each db row also has the release manifest (like v1) which contains a list of services for each:
 - service to deploy
   - git ref tag to deploy
   - image digest
   - optional deployment id
 
Then force redeployment of the services those images are used in.

Record your deployment IDs in your db.

**TODO**:
    - this needs a diagram
    - be clear environment maps to cluster in ECS

#### CLI Tool

The proposed use of the CLI tool is as follows:

```
release-tool

Usage:
    release-tool deploy (all | <service>) <env> [--project project_name] [--skip_confirm]
    release-tool latest <ecr_uri> <service> [--project project_name] [--env env_name]` 
    release-tool status (all | <service>) <env> [--project project_name]
Options: 
    --project           Project name, default from .weco-project, required where ambiguous 
    --env               Environment name, e.g. prod, stage [default: latest]
    --skip_confirm      Do not ask for confirmation during a deploy (useful in CI)
```

##### deploy

What this is doing!

For example:

```
> release-tool deploy my_service prod

This will deploy:

    my_service_1@hash_1
    my_service_2@hash_1
    my_service_3@hash_1

Do you wish to continue? (y/n) y

Deployment requested.
```

##### latest

What this is doing!

**TODO:** The latest command tags the image at git ref, pushes, then tags latest and pushes.

For example:
```
> release-tool latest account.amazonaws.com/uk.ac.wellcome/bag_register:4246187 bag_register

Updated: /project_name/images/latest/bag_register 
```

###### status

What this is doing!

Note: Should this just be ALL always?

For example:
```
> release-tool status all prod
    
     Last released: 12/02/12 16:32:12
       Released by: Bob Beardly <bob@beardcorp.com>
            Status: IN_PROGRESS

    my_service_1    hash_1     COMPLETE
    my_service_2    hash_1     IN_PROGRESS
    my_service_3    hash_1     IN_PROGRESS

```

#### Metadata

What state needs to be stored, where and what it looks like.

##### Project manifest

We need to know which services deploy where!

```json
{
  "project": {
    "name": "Catalogue",
    "service_sets": [
      {
        "id": "catalogue_pipeline",
        "name": "Catalogue Pipeline",
        "account_id": "1234567890",
        "environments": [
          {
            "id": "stage",
            "name": "Staging",
            "cluster_name": "my_stage_cluster"  
          },
          {
            "id": "prod",
            "name": "Production",
            "cluster_name": "my_prod_cluster"
          }
        ],
        "services": [
          {
            "id": "id_minter",
            "name": "ID Minter",
            "repository_name": "uk.ac.wellcome/id_minter"
          },
          {
            "id": "matcher",
            "name": "Matcher",
            "repository_name": "uk.ac.wellcome/matcher"
          },
          {
            "id": "merger",
            "name": "Merger",
            "repository_name": "uk.ac.wellcome/merger"
          }
        ]
      }
    ]
  }
}
```

This file `.wellcome` should be in the project root.

##### Data store

Deciding on table structure based on what you need to know 

Dynamo DB - give table description

Example:

|project_id (HK)      | release_id (RK)     | release_manifest | environment
|---                  |---                  |---               |---
|my_project           | 1                   | `{"...","..."}`  | prod
|my_project           | 2                   | `{"...","..."}`  | stage
|your_project         | 1                   | `{"...","..."}`  | prod
|your_project         | 2                   | `{"...","..."}`  | stage

This needs a description and WHO.

A release_manifest looks like this:
```json
{
  "service_1": {
    "release_hash": "abcdefg...",
    "image_digest": "sha256:afe605d...",
    "deployment": {
      "service_arn": "arn:service_1",
      "deployment_id": "ecs-svc/4529926..."
    }
  },
  "service_2": {
    "release_hash": "abcdefg...",
    "image_digest": "sha256:afe605d...",
    "deployment": {
      "service_arn": "arn:service_1",
      "deployment_id": "ecs-svc/4529926..."
    }
  }
}
```

the names, e.g. `service_1` map to ECS service names.

**TODO** highlight deployment_id connects to ECS deployments

#### Dashboard

A view on the data store - projects 

Get the most recent entry for a project (highest id), read its' release manifest than ask ECS to describe each service. 

Then you match deployment ID recorded to describe service response.

They could match a deployment (with status):
 - PRIMARY: 
    - len(deployments) == 1 AND runningCount!=desiredCount => YELLOW
      This deployment is unstable.
    - len(deployments) == 1 AND runningCount==desiredCount => GREEN
      This deployment is complete.
    - len(deployments) > 1 => BLUE
      This deployment is rolling out now.
 - ACTIVE:
    - runningCount==desiredCount => GREEN
      This deployment is being replaced. 
 - INACTIVE
    - GREY
      This deployment has being replaced.  
 - Not match any:
    - This deployment is not current

Report pendingCount/runningCount/desiredCount for each.

**TODO:** describe use cases for this

This is kind of like the ECS dashboard that existed previously.
