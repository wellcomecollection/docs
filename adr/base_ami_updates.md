# Updating Base AMIs in Wellcome Collection AWS Accounts

Last updated: 27/06/24

---

## Context

We use a number of base AMIs in our AWS accounts to provide a consistent starting point for our EC2 instances. These AMIs are based on the latest Amazon Linux 2 releases and must be updated regularly to ensure security and compatibility with our applications.

There are a number of agents installed on these base AMIs, including the SSM agent, all of which need to be able to report their status and health back to our monitoring systems.

## AWS Image Builder

We will use [AWS Image Builder](https://aws.amazon.com/image-builder/) to automate the creation and maintenance of our base AMIs. This service allows us to define a pipeline that builds, tests, and distributes AMIs based on our specifications. This infrastructure is terraformed in the platform account and described here: https://github.com/wellcomecollection/platform-infrastructure/tree/main/images/terraform/image-builder

Images are distributed from the platform account to the other accounts using Image Builder distribution pipelines. This allows us to maintain a single source of truth for our base AMIs while ensuring that all accounts have access to the latest versions.

## AMI Consumers

The following teams and services consume the base AMIs:

- Archivematica Infrastructure: Base AMIs for container hosts and bastion hosts.
- Goobi Infrastructure: Base AMIs for container hosts and bastion hosts.
- Digirati Infrastructure: Base AMIs for container hosts and bastion hosts.

## Decision

We will use AWS Image Builder to automate the creation and maintenance of our base AMIs. This will allow us to:

- Ensure that all base AMIs are built consistently and reliably.
- Reduce the time and effort required to update and maintain base AMIs.
- Improve the security and compliance posture of our EC2 instances by ensuring that they are always running the latest, patched versions of the underlying operating system and software.
- Provide a clear and auditable process for updating base AMIs.

AMIs will be re-built at least every 3 months, or more frequently if security vulnerabilities are identified that require immediate attention. The process will include:

- Updating the base AMI with the latest Amazon Linux 2 release.
- Installing the latest versions of the SSM agent and other required software.
- Running tests to ensure that the AMI is functioning correctly.
- Distributing the updated AMI to all relevant accounts using Image Builder distribution pipelines.
- Ensuring that all EC2 instances using the base AMI are updated to the latest version within a reasonable timeframe, typically within 2 weeks of the new AMI being available.