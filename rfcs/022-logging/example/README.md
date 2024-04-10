# Logging example

This is an example TF stack demonstrating the principles described in this RFC.

## Usage

### Setup

You will need to create the stack and populate the ECR repositories.

```
# Create the stack
terraform apply
```

### View logs

When running successfully you will see logs flowing into the `fluent-bit` index at [logging.wellcomecollection.org](https://logging.wellcomecollection.org/).

## Features

This repo demonstrates using the Fluent Bit Elasticsearch output plugin to log to our an existing ES Cluster. 

It is necessary to build a custom version of the AWS Fluent Bit image to install our config (see the [fluentbit Dockerfile](fluentbit/Dockerfile)).

We makes use of the modify filter plugin to append environment variable tags to logs exported (to annotate service, image etc).

ES credentials for Fluent Bit are loaded from secrets manager.