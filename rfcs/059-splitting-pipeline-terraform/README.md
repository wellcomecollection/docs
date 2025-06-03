# RFC 059: Splitting the catalogue pipeline Terraform

This RFC proposes a change to how we manage the Terraform for instances of the catalogue pipeline.

**Last modified:** 2023-07-03T10:39:33+01:00

## Background

We run multiple instances of the catalogue pipeline.
We always have at least one pipeline which is populating the currently-live search index, but we may have more than one pipeline running at a time.
Running multiple pipelines means we can try experiments or breaking changes in a new pipeline, and their data is isolated from the live search index (and the public API).

However, we manage every pipeline in a single Terraform configuration, and this breaks some of the isolation.
If you're trying to change one pipeline, you can inadvertently change another pipeline -- and this has caused a broken API on several occasions.

We'd like to extend the isolation to Terraform, and keep each pipeline in a different configuration.
That way, you can only modify one pipeline at a time, and you know exactly what you're changing.

This RFC describes what that looks like in slightly more detail.

## Desirable properties

*   It should be easy to find the pipeline you want to work in.

*   It should be easy to create new pipelines.

*   Each pipeline should have its own Terraform state file and label.
    This should be specified in as few places as possible, to reduce the risk of inconsistency, e.g. a pipeline whose label is `2001-01-01` but the state file is named `2002-02-02`.

*   This should make sense to somebody who's already an experienced Terraform user – commands like `plan`, `apply`, `import` should all work as they expect (modulo our `run_terraform.sh` wrapper).
    You shouldn't need to learn a new tool to work with the pipeline Terraform.

## The proposal

We create per-pipeline folders in the `terraform` directory, something like:

```
.
└─ terraform/
    ├─ 2001-01-01/
    │   ├─ main.tf
    │   └─ run_terraform.sh
    ├─ 2002-02-02/
    │   ├─ main.tf
    │   └─ run_terraform.sh
    └─ modules/
        └─ ...
```

Each per-pipeline folder contains:

*   A single Terraform file that refers to a shared pipeline module in the `modules` directory

*   A `run_terraform.sh` wrapper which injects the Elastic Cloud secrets, and the name of the current pipeline as a Terraform variable.
    This gets read from the folder name, so it should be possible to use the same copy of `main.tf` across different pipelines.

What this should look like for developers:

*   For a pre-existing pipeline, you `cd` into the folder and run `run_terraform.sh` as usual.

*   If you want to create a new pipeline, copy an existing folder and rename it.
    When you `cd` into that folder, you run `run_terraform.sh init` to start the new pipeline and then plan/apply as usual.

## Implementation details

*   **Partial configuration.**
    We can use [partial configuration] for Terraform backends to create a different state file for each pipeline.
    The `run_terraform.sh` script can read the name of the current folder, and pass the pipeline date in as a variable.

*   **Auto-deleting old copies of the `.terraform` folder.**
    When you copy an existing pipeline folder, you'll get the `.terraform` folder.

    We'll want to delete this folder in the `run_terraform.sh` script if it points to the wrong state file, to avoid Terraform trying to be "helpful" and inadvertently breaking a different pipeline.
    This is best understood with a worked example:

    > I create a pipeline `2001-01-01`, then I copy the folder to create `2002-02-02`.
    >
    > When I run `run_terraform.sh init` in the `2002-02-02` folder, it notices that the state in `.terraform` points at `s3://…/2001-01-01.tfstate`, but now I'm trying to keep state in `s3://…/2002-02-02.tfstate`.
    >
    > It offers to migrate the state to the new location; if I say yes, it will copy the state and then try to destroy the resources labelled `2001-01-01` on the next plan/apply.
    >
    > It would be better if our script knew that this was a different pipeline, and that we can't reuse the `.terraform` folder.

*   The per-pipeline state files should be in a dedicated prefix, so they can be easily identified, e.g.

    ```
    s3://…/catalogue-pipeline/pipeline/2001-01-01.tfstate
    s3://…/catalogue-pipeline/pipeline/2002-02-02.tfstate
    s3://…/catalogue-pipeline/pipeline/2003-03-03.tfstate
    ```

[partial configuration]: https://developer.hashicorp.com/terraform/language/settings/backends/configuration#partial-configuration

## Rejected approaches

*   **Creating an entirely custom tool.**
    We don't want developers to have to learn a new tool just to work on the catalogue pipeline Terraform -- it should be possible to create a familiar workflow with `run_terraform.sh` that's easier for everyone to learn.

*   **Terraform features: using workspaces, running a script with -chdir.**
    These are both Terraform features that might enable the sort of process we want, but we don't use them anywhere in the platform so they're not a familiar workflow for us.
    Using separate folders should be easier.
