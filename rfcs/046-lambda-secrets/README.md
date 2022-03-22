# RFC 046: Secrets in Lambda functions

**Status:** Draft

**Last updated:** 22/03/2022

## Context
We have historically used AWS's per-invocation "serverless" environment, Lambda, as a kind of glue between more complex applications or as part of our monitoring stacks. Increasingly, we have been using it for complete applications: most notably, for the Identity API.

With this increased usage, our Lambdas have been running more privileged workloads, and the existing approach to secrets - that is, unencrypted environment variables - has become inadequate. While ECS [provides](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/specifying-sensitive-data-secrets.html) a method for injecting secrets as environment variables at container startup, no such built-in solution exists for Lambda. This RFC proposes one such solution.

#### Desiderata
As a starting point, we'd like any solution to satisfy the following:
- *AWS Secrets Manager* as the source for secrets, to match our current usage and to allow explicit permissions on individual secrets via IAM.
- Secrets are fetched when the Lambda starts: no need to keep them "live".
- Secrets are injected transparently as environment variables: no requirement for additional/custom APIs or clients within runtimes.
- Language-agnostic: our solution will work for Lambdas written in any language.

#### Prior art
1. Lambda includes the feature to [encrypt environment variables at rest](https://docs.aws.amazon.com/lambda/latest/dg/configuration-envvars.html#configuration-envvars-encryption). 

   This doesn't account for getting the secrets into the function configuration (ie Terraform still needs to deal with them), or access control, and if we wanted to encrypt in transit we'd need to add decryption code into the Lambda. :x:

2. AWS propose an architecture to [*"Cache secrets using AWS Lambda extensions"*](https://docs.aws.amazon.com/prescriptive-guidance/latest/patterns/cache-secrets-using-aws-lambda-extensions.html), which reads secret ARNs from a config file and then (HTTP) serves them inside the container runtime. This cache can expire and the secrets will be re-fetched during runtime.

   This requires runtime code to fetch secrets - asynchronously - via HTTP, and if the server isn't a binary then it's dependent on the language of the Lambda runtime. :x:

3. Square's [*"Using AWS Lambda Extensions to Accelerate AWS Secrets Manager Access"*](https://developer.squareup.com/blog/using-aws-lambda-extensions-to-accelerate-aws-secrets-manager-access/) fetches secrets from elsewhere, but then uses a Golang binary in a Lambda [extension](https://docs.aws.amazon.com/lambda/latest/dg/using-extensions.html) to read secret ARNs from a config file and download those secrets to a file in `/tmp` which is shared with the execution environment.

   This is a good solution apart from the proprietary config file and the need to read the secrets from a file in `/tmp`, rather than transparently. :x:

4. Hashicorp provide [a Lambda extension](https://github.com/hashicorp/vault-lambda-extension) which fetches specified secrets from Vault and writes them to a JSON file in `/tmp`.

   This is basically the same as Square's solution, and additionally it uses Vault rather than Secrets Manager. :x:

5. AWS blog post: [*"Creating AWS Lambda environment variables from AWS Secrets Manager"*](https://aws.amazon.com/blogs/compute/creating-aws-lambda-environmental-variables-from-aws-secrets-manager/). This proposes using a Lambda [layer](https://docs.aws.amazon.com/lambda/latest/dg/gettingstarted-concepts.html#gettingstarted-concepts-layer) containing a Golang binary to fetch a given secret ARN, and then uses an init-phase [wrapper script](https://docs.aws.amazon.com/lambda/latest/dg/runtimes-modify.html) to create runtime environment variables from the contents of the secret.

   This solution is limited (it only supports a single secret), and of course we don't write Go, but it's probably the most viable direction.

## Proposal

1. Create a binary which fetches a given list of secrets. Ideally this would be in Typescript: we can try compiling with [pkg](https://www.npmjs.com/package/pkg), despite its disclaimer about serverless environments. Otherwise will require some investigation into Amazon Linux 2 AMI compatibility.
2. Create a wrapper script to run the binary and inject secrets as environment variables. Get the list of secret names from a single JSON-encoded environment variable.
3. Create a Lambda layer containing the above 2 artifacts.
4. Create a Terraform module which references the above layer, constructs the variable containing secret names, provides IAM permissions on the secrets for the Lambda execution role, and provides outputs for configuring a Lambda function.

*Note on Lambda layers/extensions:*

Lambda layers "provide a convenient way to package libraries and other dependencies that you can use with your Lambda functions". Lambda extensions are deployed as layers, and have access to the [Lambda Extensions API](https://docs.aws.amazon.com/lambda/latest/dg/runtimes-extensions-api.html) to hook into the Lambda lifecycle and to in a separate process to the main Lambda code. Using a layer as described above is in effect an extremely simple extension - these aren't really separate features in AWS. While we haven't used layers previously, this is exactly the kind of use case they were designed for.

## Questions and potential issues

- If `pkg` doesn't work for compiling TS to a binary, what else can we use? We haven't yet written in any compiled languages. If this doesn't work, we can always fall back to making this solution Node-only (ie using TS compiled to JS and hence supporting only the Node lambda runtime).
- Is there a way that the Terraform module can wrap an `aws_lambda_function` without having to replicate all its variables? This might make it easier to create "Wellcome" Lambdas, with potential for adding a layer/extension for logging to Elasticsearch later on.