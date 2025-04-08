# The current state


### The projects

There are 23 non-archived repositories containing Python code.
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
All projects that have tests currently use pytest. There are no differences to consider.

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
