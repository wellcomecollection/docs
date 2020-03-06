# RFC 021: Data science in the pipeline

**Status:** 🏗 Draft 🚧

**Last updated:** 2020/03/06

## Motivation

We want to be augment works and images with data inferred off of them using data science techniques: for example, feature vectors and colour palettes for images.

Currently, we do this by holding both some form of index (usually a set of points in a vector space) as well as a model in a separate service - for example, https://labs.wellcomecollection.org/feature-similarity. This has significant drawbacks: data is duplicated, outdated, patchy, and perhaps most importantly, must be searched as a wholly separate all-or-nothing operation outside of our ES indices.

To resolve this, we want to bring data science services into the pipeline, and use them to augment works/images with data that can be indexed and searched in ES. This RFC details how that might look.

## Proposal

We can write down some desiderata for any proposed solution:

- Data science (DS) logic can be written in Python
- DS services do not know about our data model(s)
- Pipeline services do not know about data science
- DS services do not know about SQS, message passing, the Actor model, etc
- DS models are persistent and separate to DS inferrers
- DS models can be retrained on demand

These suggest 3 distinct, but loosely coupled, services:

- **Inferrer**: A Python service that provides a synchronous API that consumes whatever is needed to infer the new data, which it outputs.
- **Model Trainer**: A Python service that can consume records from the catalogue index in bulk in order to train a model, and outputs/stores a persistent representation of this model for the *inferrer* to use.
- **Inference Manager**: A Scala service that lives in the pipeline and contains "the usual" Wellcome message-passing, Akka, etc logic & libraries, which sychronously calls the `inferrer` and attaches the new data to the work/image before passing it along.

The usage of these services would look like this:

![An architecture diagram for data science services](https://user-images.githubusercontent.com/4429247/76087593-631cc700-5fae-11ea-819f-3545e6dc7c65.png)

#### Implementation details

- The inferrer and inference manager exist in one task definition (and therefore on one host). The inferrer is not marked as essential: crashes are tolerated. Timeouts and other failures are naturally handled by the queue redrive policies.
- The model trainer runs automatically as soon as it starts: it is triggered by an autoscaling policy. Scaling up could be based on regular time intervals, messages in queues, lambdas etc, and scaling down would be done by the trainer itself.
- The inferrer loads the model from S3 when it starts. Inferrer instances will be short-lived (as they'll scale to zero when not in use) so triggering a restart or loading a new model by other means is not necessary.

### Questions & drawbacks

> Are the network requests for (eg) image files going to be very expensive and/or slow? How could we mitigate this?

> How do we deal with wanting to infer several separate things for one piece of content (eg a feature vector _and_ a palette vector for a single image)? A chain of inferrer-manager pairs would be simplest and cleanest, but this would require `n` times as many network requests for images as one inferrer doing all the work.

> Should DS APIs be open to the public?

> Should model artefacts be open to the public?

> Should DS inferrers work only for things we know (ie feature vectors can be inferred only for images within the WC ecosystem, by passing an image ID) or with any content (ie feature vectors can be inferred for any image, by passing a publicly accessible URI)

> It seems like we'll have to reinfer on every existing work/image when a model is retrained, which will significantly add to the expense of retraining based on the above considerations about network requests etc. Is this necessarily the case?
