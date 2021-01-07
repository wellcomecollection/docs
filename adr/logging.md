# Logging

Last updated: 29/06/20

Our logging implementation arises from the discussion in the [logging RFC](../rfcs/022-logging/).

To remove log routing logic from our application containers we use [AWS Firelens](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/using_firelens.html) to transport logs from our ECS tasks directly to Elasticsearch.

Logs can be searched at [logging.wellcomecollection.org](https://logging.wellcomecollection.org) using Kibana. You will require a Wellcome account to sign in via Azure AD.

Custom configuration required for the fluentbit "sidecar" container required by Firelens can be found [here](https://github.com/wellcomecollection/platform-infrastructure/tree/master/containers/fluentbit).

The fluentbit "sidecar" container requires a set of secrets \(Elasticsearch access details\), and these are preset in the [firelens module](https://github.com/wellcomecollection/terraform-aws-ecs-service/tree/v2.6.3/modules/firelens) for our ECS services.

The Elasticsearch secrets are provisioned into an AWS account from the [platform-infrastructure](https://github.com/wellcomecollection/platform-infrastructure/blob/master/critical/back_end/secrets.tf) repository.

