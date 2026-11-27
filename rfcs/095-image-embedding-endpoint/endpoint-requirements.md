# Requirements for the image embedding endpoint

This document lists what the catalogue pipeline needs from an endpoint that serves SigLIP 2 image embeddings. It accompanies [RFC 095](README.md), which describes how the pipeline uses the endpoint and caches its output. It is written for the team that will host the endpoint, and it is a starting point for agreement.

Each requirement is marked **Must** or **Should**. A Must is something the pipeline design depends on. A Should is a preference we can work around, and the workaround is given.

Numbers marked _proposed_ are our suggestion and are open to change once we can measure against a test endpoint.

## How we will use it

The pipeline embeds each image once per model and stores the result in a cache. That shapes the load.

| Phase | Volume | Pattern |
| --- | --- | --- |
| First fill | About 127,000 images, once per model version | A single job, run at a rate we agree, that can be paused and resumed |
| Normal running | Images that are new to the collection, which we expect to be a small number per day and have not yet measured | A scheduled batch job every 15 minutes that calls the endpoint only when there are new images |
| Reindex | None | A reindex reads from the cache and does not call the endpoint |

Nothing in the pipeline waits on a person, so latency in the usual sense does not matter to us. Correctness, stable versions and predictable failure behaviour matter much more.

## The model and its output

| Requirement | Level | Why |
| --- | --- | --- |
| The model is `google/siglip2-base-patch16-224` at a pinned Hugging Face revision. | Must | Our evaluation and reference vectors use this checkpoint. The NaFlex variants have a different input and produce different vectors. |
| The output for each image is one vector of 768 float32 values from the image tower's pooled output. | Must | This is what our index mapping will be built for. |
| The vector is L2-normalised, with a norm within 0.001 of 1 (_proposed_). | Should | Our index uses dot product similarity, which needs unit length. If the endpoint returns the raw output, we normalise it ourselves, and need to be told that it is raw. |
| The same image bytes give the same vector on every call, whatever else is in the batch, to a cosine similarity of at least 0.9999 (_proposed_). | Must | We cache the first answer and never ask again. A result that depends on batch composition would make the cache arbitrary. |
| The vectors agree with the PyTorch fp32 reference closely enough that search results are equivalent. We propose a mean cosine similarity of at least 0.999 and at least 95% overlap in the ten nearest neighbours, measured on a few thousand of our images (_proposed_). | Must | We hold reference vectors for the collection and will run this comparison ourselves. It is how we will find out what ONNX export and any quantisation cost. |

## Image handling

| Requirement | Level | Why |
| --- | --- | --- |
| The endpoint accepts JPEG bytes. | Must | We send thumbnails of at most 400 pixels on the long side, with a median size of 38 KB and a largest observed size of 114 KB. |
| The endpoint does the preprocessing: a bilinear resize straight to 224 by 224 with no crop or padding, a rescale by 1/255, and normalisation with a mean and standard deviation of 0.5. | Should | These are the checkpoint's own values. One implementation on the endpoint means every caller gets the same vector. If the endpoint takes pixel tensors, we do this ourselves and need the expected tensor layout. |
| Greyscale and CMYK images are converted to RGB, and EXIF orientation is applied. | Should | Our thumbnails include both. If the endpoint does not do this, we convert before sending. |
| The preprocessing is documented, including the resampling filter. | Must | A different filter or a centre crop gives different vectors, and we could not tell from the output alone. |

## Request and response

| Requirement | Level | Why |
| --- | --- | --- |
| One request can carry a batch of images. We expect to send up to 30, which is about 2.3 MB at our 99th percentile size. | Should | SageMaker limits a request to 6 MB and a response to 60 seconds. If the endpoint takes one image per request, we send requests concurrently and rely on server-side batching. |
| Each image in a request carries an identifier we choose, and the response returns it with the result. | Should | It lets us detect a response whose items are out of order. Without it we rely on order being preserved, and need that guaranteed. |
| Each image in a batch has its own status. An image that cannot be decoded is reported as failed and the others succeed. | Should | One corrupt thumbnail should not fail 29 good ones. Without this we split a failed batch and retry until we isolate the image. |
| An input problem (an undecodable image, an oversized payload) is distinguishable from a server problem. | Must | We skip and report the first and retry the second. Retrying a bad image forever would block the images queued behind it. |
| The limits are documented: the largest batch, the largest payload and the largest image. | Must | So that we size requests correctly and do not find the limits through failures. |
| The response format is documented and stable for a model version. JSON arrays or base64-encoded float32 are both fine. | Must | We validate every vector before storing it. |

## Versions

These requirements matter most to us. Vectors from two versions of a model cannot be mixed in one search index, so each of our pipelines is pinned to one version for its whole life.

| Requirement | Level | Why |
| --- | --- | --- |
| Every response reports a model version. | Should | We compare it with the version the pipeline is configured for and stop if they differ. If the response cannot carry a version, the endpoint name stands in for it, and a named endpoint must then never be redeployed with a different model. |
| The version identifies the checkpoint revision, the export precision (fp32, fp16 or int8) and the preprocessing. A change to any of them is a new version. | Must | Each of these changes the vectors. |
| A deployed version does not change in place. A new export or quantisation is deployed alongside the old one. | Must | A change underneath a running pipeline would put two vector spaces in one index. |
| An old version keeps serving until we confirm that no pipeline uses it. | Must | Moving to a new version means filling a cache and reindexing, which takes us days to weeks, and the old pipeline is live throughout. |
| We are told in advance when a new version is planned and when an old one is to be retired. We propose four weeks' notice of a retirement (_proposed_). | Must | We need time to fill the cache and reindex. |

## Access

| Requirement | Level | Why |
| --- | --- | --- |
| The pipeline can call the endpoint from a different AWS account and region through the public SageMaker runtime API. | Must | The pipeline is in eu-west-1 in the platform account. The endpoint will be in eu-west-2 in the hosting team's account. |
| Authorisation is an IAM role in the hosting account that allows `sagemaker:InvokeEndpoint` on the image embedding endpoints, which our task assumes. | Should | It needs no shared network. We are open to another route if the hosting team prefers one. |
| The role trusts our account with a condition on the calling role's name pattern, and does not name a single role. | Should | Our task role is recreated with a new name for each pipeline. Naming it would mean a change on the hosting side every time. |
| No private network path is required. | Should | The images are public catalogue thumbnails. If a private path is required by policy, we need to know early, because it adds infrastructure on both sides. |
| There is an endpoint we can call for testing before production use. | Must | For the comparison against our reference vectors and for load testing. It can be the same endpoint. |

## Capacity and availability

| Requirement | Level | Why |
| --- | --- | --- |
| The first fill can run at a sustained 5 images a second or more (_proposed_). | Should | That fills the cache in about seven hours. A lower rate is acceptable if we know it, since the job can run over several days. |
| We are told the request rate to stay under, and the endpoint signals throttling in a way we can distinguish from failure. | Must | We limit our own concurrency and back off. We would rather be told a limit than find it. |
| If the endpoint scales to zero, we are told, along with the expected time to start. We propose that a cold start completes within 10 minutes (_proposed_). | Must | A real-time endpoint that has scaled to zero rejects requests until an instance is up. Our client retries for longer than the start time, so it needs to know what that is. |
| Short outages are acceptable. | | Our client retries for several minutes, and a failed batch can be run again later. Only images that are new to the collection are delayed. |
| We are told about planned downtime and have a named contact or channel for incidents. | Must | An outage longer than our retry window fails a pipeline run and raises an alarm on our side. We need to know whether to wait or to act. |
| The endpoint is synchronous. | Must | The pipeline calls it and waits for the answer. See also the section on text embedding. |

We do not need low latency, high availability or autoscaling for bursts.

## Later: embedding search queries

This is outside the first use and is not a requirement now. We would like to avoid choices that rule it out.

- The model's text tower would let us embed a search query and compare it with image vectors. That is a request-time call from the search API, so it would need low latency and high availability, which the batch use does not.
- An asynchronous SageMaker endpoint accepts only asynchronous calls, so it could not serve this.
- The text and image towers have to come from the same checkpoint and version for their vectors to be comparable.
- The text tower expects lowercased input, padded or truncated to 64 tokens.

## How we will check the endpoint

Once a test endpoint exists we will run these checks and share the results.

- Embed a few thousand images and compare with our reference vectors: cosine similarity per image and overlap in the ten nearest neighbours.
- Embed the same images twice, alone and in batches of different sizes, and compare the results with each other.
- Send greyscale, CMYK, rotated and corrupt JPEGs and record what comes back.
- Run 12 concurrent clients to find the sustained throughput and the throttling behaviour.
- Measure the cold-start time, if the endpoint scales to zero.

## Still to agree

- Which of the Should items the endpoint will meet, and which we work around.
- The thresholds marked as proposed.
- Who pays for the endpoint, and whether other teams are expected to use it.
