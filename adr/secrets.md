# Secrets

Last updated: 29/06/20

---

There are various places we deal with secrets in the platform.

## AWS Credentials

Wellcome Collection AWS accounts are part of the wider Wellcome Trust AWS Organisation.

### Root accounts

Root accounts require MFA access, credentials are stored in Password Manager Pro, and accounts described in Confluence. This service is only accessible to authorised users within the Wellcome network (or with Global Protect). 

All root accounts require use of the hardware MFA key stored within a firesafe on Wellcome premises.

### Developer access

Developers **should not** use IAM accounts to access AWS.

Developer access to AWS requires a special "Wellcome Cloud" account requested from the Digital department. A normal Wellcome account is not sufficient.

Access to assume particular roles within a Wellcome Collection AWS account is then made by updating an Azure AWS SSO application within the Azure console.

IAM roles and federated access is provisioned via terraform.

Further information is available in the [platform-infrastructure repository](https://github.com/wellcomecollection/platform-infrastructure/tree/master/accounts)

### Machine accounts

Where a service outside of AWS requires some access to Wellcome Collection AWS resources it is acceptable to provision an IAM user to do so. 

Permissions provided to IAM users should follow the [principle of least privilege](https://en.wikipedia.org/wiki/Principle_of_least_privilege). 

IAM users and their roles / permissions must always be provisioned in terraform.

Thought should be given as to how to rotate credentials if necessary.

#### Continuous Integration

A subset of Machine accounts, we provision AWS access for Travis CI to publish artifacts via the [platform-infrastructure repo](https://github.com/wellcomecollection/platform-infrastructure/tree/master/builds).

## SSH Keys

There is currently not an approved mechanism for distributing SSH keys. These are shared between developers when required.

## ECS

ECS tasks should load secrets from [AWS SecretsManager via SSM](https://docs.aws.amazon.com/systems-manager/latest/userguide/integration-ps-secretsmanager.html).

You should use the provided [container_definition](https://github.com/wellcomecollection/terraform-aws-ecs-service/tree/v2.6.3/modules/container_definition) terraform modules to facilitate this.

## Terraform

Terraform variables should be loaded from [SSM Parameter store](https://docs.aws.amazon.com/systems-manager/latest/userguide/systems-manager-parameter-store.html), _not a .tfvars file_. Secrets should never be stored in terraform state but referenced via a [SecretsManager](https://aws.amazon.com/secrets-manager/) path.