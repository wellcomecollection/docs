# RFC 070: Python Building and Deployment

Building and deploying Python projects

## Background

Over time, we have created a number of different Python projects.  Some as the main or only application within a 
repository, others as part of a larger whole alongside Scala applications.

Each time, we have written a new build and deployment process for them. For the most part, the process a project 
is born with has stuck, despite us finding better tools or methods when working on later projects. As such, we have
ended up with multiple diverse mechanisms to check, build and deploy them.  Each with different standards and rules.

This RFC proposes to harmonise those projects.  The projects are listed in 
the [Appendix](appendix.md), alongside some description of their differences.

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

### What Can and Cannot Be DRY

Because of the way configuration resolution works in the various build tools (e.g. [for Ruff](https://docs.astral.sh/ruff/configuration/#config-file-discovery))
We do need to define a certain amount of configuration in each project, rather than sharing it across projects, 
and that could become out of date.

### Recommended Toolset

#### Linting/Formatting
[Ruff](https://docs.astral.sh/ruff/) provides the both linting and formatting together,
it has already been used successfully in the Concepts Pipeline.

#### Testing
[pytest](https://docs.pytest.org/) is currently in use in all projects, and there is no need to consider changing that.

#### Dependency Management

[UV](https://github.com/astral-sh/uv).

The most pertinent advantages of UV over other package/dependency managers are the way it simplifies:

1. Treating shared code in the same repository as though it is an installable library
2. Keeping the Python version up to date, and sharing that with other developers

#### CI

Github Actions (This has been discussed elsewhere, and is [already an assumed requirement](../069-catalogue_graph_ingestor#requirements) of new projects)

#### Build and deployment

Although harmonising how applications are to be run is out of scope, there are two methods that 
we currently use. Docker images running on ECS and Zipped packages running on AWS Lambda. Packages
for running in these environments can be built according to the UV [documentation](https://docs.astral.sh/uv/guides/integration/docker/#getting-started) and example code showing their best practice when building
[Docker images](https://github.com/astral-sh/uv-docker-example) and [Lambda Zips](https://docs.astral.sh/uv/guides/integration/aws-lambda/#deploying-a-zip-archive).  This is to be harmonised via some common github actions (see below)

### Specific usage

#### Individual Configuration

Each project is configured as much as possible in its `pyproject.toml`, including defining 
paths to shared modules elsewhere in the repository using pythonpath.

In a UV-based project, a .python-version file defines the python version in use. This should be read and reused where
possible, rather than relying on developers to keep the version number in harmony everywhere in the project.

This also allows docker images and build scripts to read the version, meaning that we can
use common scripts to achieve these tasks.

e.g. - to package up all the requirements of a project into a zip:
```shell
PYTHON_VERSION=$(cat .python-version)
uv export --frozen --no-dev --no-editable -o requirements.txt
uv pip install \
   --no-installer-metadata \
   --no-compile-bytecode \
   --python-platform x86_64-manylinux2014 \
   --python "$PYTHON_VERSION" \
   --target packages \
   -r requirements.txt

cd packages && zip -r ../package.zip .
```
or to create a Docker image using the correct Python version.
```shell
docker build . --build-arg pythonversion=$(cat .python-version) --progress=plain
```
```dockerfile
ARG pythonversion=2.7
FROM python:$pythonversion
ARG pythonversion
RUN echo python version = $pythonversion
```
#### Common Configuration

Although each project will have its own pyproject.toml files, there can also be 
some commonality.

### Common Github Actions

Three Actions are to be defined in the .github repository:

#### Check
A "Python Check" Github Action in the .github repository

This will:
* Default to using a common Python version
  * individual projects may override this if there are compatibility problems
* Be parameterised with
  * path to base of python project
  * whether to care about types
* install requirements with UV
* run ruff
* run pytest
* run mypy if relevant

#### Build

Two Python Build actions 
- one to build and publish Docker Images to ECR
- one to zip a project for use in AWS Lambda (replicating the behaviour [here](https://github.com/wellcomecollection/catalogue-pipeline/blob/6376672ef4338ab9496d4f5b3eb671eefd3e5923/.github/workflows/catalogue-graph-build.yml#L1) in a common fashion)

## Getting there from here

### Converting existing projects

We should convert existing projects to the new common approach, starting with the Catalogue Pipeline inferrers.



### Project Template

Entirely new Python projects are not common, so the work involved in creating
and maintaining a project template is likely to outweigh any advantage it might bring.
