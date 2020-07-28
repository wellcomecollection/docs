# RFC 021: Data science in the pipeline

**Status:** 🏗 Draft 🚧

**Last updated:** 2020/07/28

## Motivation

We want to augment works and images with data inferred from them using data science techniques: for example, feature vectors and colour palettes for images.

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

These suggest 3 types of distinct, but loosely coupled, services:

- **Inferrer**: A Python service that provides a synchronous API (most likely RESTful HTTP) that consumes whatever is needed to infer the new data, which it outputs. There can be multiple different inferrers.
- **Inference Manager**: A Scala service that lives in the existing pipeline and contains "the usual" Wellcome message-passing, Akka, etc logic & libraries. It performs any work that is required by all of the inferrers, synchronously calls all of them and attaches the new data from them to the work/image (by populating a field) before passing it along. There is one inference manager for all the inferrers.
- **Model Trainer**: A Python service that can consume records from the catalogue index in bulk in order to train a model, and outputs/stores a persistent representation of this model for an *inferrer* to use. There is **optionally** one model trainer for each inferrer.

The usage of these services would look like this:

![An architecture diagram for data science services](https://user-images.githubusercontent.com/4429247/88694368-5bde8d00-d0f8-11ea-8d0b-4b1c7687877b.png)

#### Implementation details

- The inferrers and inference manager exist in one task definition (and therefore on one host).
- Non-trivial results of the shared work that the manager might perform (eg, images that it downloads and that are required by all of the inferrers) are stored as artifacts in an EBS volume attached to the host and mounted in both the manager and inferrer tasks. In this case, the request to the inferrers from the manager would include a local filesystem path to the artifacts.
- The model trainer is run as a standalone one-off ECS task from a local script.
- The inferrer loads the model from S3 when it starts. Inferrer instances will be short-lived (as they'll scale to zero when not in use) so triggering a restart or loading a new model by other means is not necessary.

### Questions & drawbacks

> How do we deal with the fact that different inferrers have to live on one host but may have differing compute requirements? *Potential answer: if that requirement is GPU, use elastic inference rather than GPU instance classes*.

> Should DS APIs be open to the public?

> Should model artefacts be open to the public?

> Should DS inferrers work only for things we know (ie feature vectors can be inferred only for images within the WC ecosystem, by passing an image ID) or with any content (ie feature vectors can be inferred for any image, by passing a publicly accessible URI)

> It seems like we'll have to reinfer on every existing work/image when a model is retrained, which will significantly add to the expense of retraining based on the above considerations about network requests etc. Is this necessarily the case?
