# RFC 070: Python Building and Deployment

Building and deploying Python projects

## Background

Over time, we have created a number of different Python projects.  Some as the main or only application within a 
repository, others as part of a larger whole alongside Scala applications.

Each time, we have written a new build and deployment process for them. For the most part, the process a project 
is born with has stuck, despite us finding better tools or methods when working on later projects. As such, we have
ended up with multiple diverse mechanisms to check, build and deploy them.  Each with different standards and rules.

This RFC proposes to harmonise those projects.

### Problems

The differences between the projects give rise to various problems

* keeping things up to date - Python itself, dependencies, common settings
* different standards - type checking, introducing previously ignored warnings if we harmonise linting rules
* sharing code in different projects within the same repository
* ensuring all required code and dependencies get deployed
* running the same environment locally and on CI (PYTHONPATH, installed dependencies, Python versions)
* different ways to specify production vs development dependencies

### Out of Scope

Exactly _how_ the applications are run (Lambda, ECS etc.) is a decision to be made at the per-application level.
This RFC does make recommendations on how to ensure that a Python project and all its dependencies are included,
but whether the end result is a container or a zip is up to the target.

### The projects

There are 23 non-archived projects containing Python code.
One is this documentation repository, where an example python file
is included in an RFC.

Of these, nine contain Python only in the form of [a script](https://github.com/wellcomecollection/terraform-aws-api-gateway-responses/blob/a8cfd94351ea6ade8389372660d74ef0e4d26ae5/gha_scripts/create_release.py) executed as part of a Github Action
as part of preparing a release:

* https://github.com/wellcomecollection/terraform-aws-ecs-service
* https://github.com/wellcomecollection/terraform-aws-lambda
* https://github.com/wellcomecollection/terraform-aws-sns-topic
* https://github.com/wellcomecollection/terraform-aws-vhs
* https://github.com/wellcomecollection/terraform-aws-gha-role
* https://github.com/wellcomecollection/terraform-aws-acm-certificate
* https://github.com/wellcomecollection/terraform-aws-api-gateway-responses
* https://github.com/wellcomecollection/terraform-aws-sqs
* https://github.com/wellcomecollection/terraform-aws-secrets

These should be harmonised by removing the duplication.

Four are only currently updated by a Digirati 
* https://github.com/wellcomecollection/iiif-builder
* https://github.com/wellcomecollection/iiif-builder-infrastructure
* https://github.com/wellcomecollection/londons-pulse
* https://github.com/wellcomecollection/pronom-format-map

One is soon to be redundant, we do not typically make changes to the Python in it.
* https://github.com/wellcomecollection/archivematica-infrastructure

That leaves eight repositories to consider 
* https://github.com/wellcomecollection/catalogue-pipeline
* https://github.com/wellcomecollection/storage-service
* https://github.com/wellcomecollection/platform-infrastructure
* https://github.com/wellcomecollection/cost_reporter
* https://github.com/wellcomecollection/rank
* https://github.com/wellcomecollection/editorial-photography-ingest
* https://github.com/wellcomecollection/catalogue-api
* https://github.com/wellcomecollection/sierra_api

In these, the catalogue pipeline repository contains a variety of
Python projects, including  [catalogue-graph](https://github.com/wellcomecollection/catalogue-pipeline/tree/fd516e1d52a41637a4634308734a0d58b6b5e2f6/catalogue_graph),
one of the largest, most modern and comprehensively built; and the much simpler and older 
[inferrer](https://github.com/wellcomecollection/catalogue-pipeline/tree/92727715888204ca82b86cc0fbf478e5ca46f2dc/pipeline/inferrer)
projects.

### Differences

#### No build process
[Cost reporter](https://github.com/wellcomecollection/cost_reporter) has no build process or tests, runs on Python 3.9 in Lambda


[Sierra_api](https://github.com/wellcomecollection/sierra_api) is "meant for quick experiments and exploration", and does not have any build process or deployment


The only Python files in [catalogue-api](https://github.com/wellcomecollection/catalogue-api) are some maintenance scripts. No build process, no tests.

Most of the Python files in [platform-infrastructure](https://github.com/wellcomecollection/platform-infrastructure) are tests themselves.
However, there are also two Lambdas used for alerting. No build process, no tests for the Python itself.
This repository also defines a Docker image designed to harmonise our use of flake8.


#### Dependency Management
[Rank](https://github.com/wellcomecollection/rank) uses [Poetry](https://python-poetry.org)
Most others use requirements files, frozen using pip-compile.

One problem with using requirements files is that there is no consistent way to define and name the 
separate requirements used in production vs. development.  It comes down to ad-hoc filenames like 
`dev_requirements.txt` or `requirements.test.txt`. 

Poetry solves this, as does the more modern [UV](https://docs.astral.sh/uv).

#### Testing
All projects that have tests currently use pytest, so there is no difference there.

#### tox

Python tests in the [Storage Service](https://github.com/wellcomecollection/storage-service) are initiated with Tox.

This is unnecessary as we only run the tests on a single environment configuration

#### Linting

The Catalogue Graph within the [catalogue pipeline](https://github.com/wellcomecollection/catalogue-pipeline) uses Ruff
Other applications use Flake8 (e.g. [editorial photography ingest](https://github.com/wellcomecollection/editorial-photography-ingest))

#### Formatting

The Catalogue Graph within the [catalogue pipeline](https://github.com/wellcomecollection/catalogue-pipeline) uses Ruff

Black [editorial photography ingest](https://github.com/wellcomecollection/editorial-photography-ingest) and [storage service](https://github.com/wellcomecollection/storage-service) both use Black

#### Linting and Formatting Rules
Different projects specify their own rules for formatting and ignoring lint warnings.  
These should be harmonised where possible.

#### Buildkite vs Github Actions
Python tests in the Storage Service and [catalogue pipeline](https://github.com/wellcomecollection/catalogue-pipeline) run on Buildkite, apart from 
the catalogue graph steps which run using Github Actions

#### Type Checking

Only the Catalogue Graph uses strict type checking.

## Harmony

Going forward, all new Python projects will use the following toolchain.  Existing projects should be updated
to use these tools when convenient.

### Tool Use

Linting/formatting: [Ruff](https://github.com/astral-sh/ruff)
Dependency Management: [UV](https://github.com/astral-sh/uv)
Testing: [pytest](https://docs.pytest.org/)
CI: Github Actions (This has been discussed elsewhere, and is [already an assumed requirement](../069-catalogue_graph_ingestor#requirements) of new projects)

### What Can and Cannot Be DRY


### Common Github Action

A Github Action in the .github repository

This will: 
    Default to using a common version, 
        individual projects may override this if there are compatibility problems
    install requirements with UV
    run ruff and 
        be parameterised with 
            path to base of python project
            defaults for python version.
            whether to care about types
            error threshold for warning count
        also having a base set of parameters passed to Ruff regardless of parameters
    run pytest

### Common Shell Script

A common shell script that does the same as the Github Action above.

### Building and Deploying

#### Docker
UV provides [documentation](https://docs.astral.sh/uv/guides/integration/docker/#getting-started) and 
[example code](https://github.com/astral-sh/uv-docker-example) 
showing their best practice when building a Docker image.

#### Lambda (as Zip Archive)
See [UV Documentation](https://docs.astral.sh/uv/guides/integration/aws-lambda/#deploying-a-zip-archive)

### Project Template


TODO: can we also harmonise building a container?
Taking into consideration that 
* some projects won't build a container, 
* some will just be to put a single folder into the container
* some will need to pick up code from multiple folders
* most need to install dependencies (some of which may not be pure Python)
* different base images (e.g. lambda vs ecs)









## Getting there from here
