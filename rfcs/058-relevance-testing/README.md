# RFC 57: Relevance testing

**Status:** Draft
**Last updated:** 2023-06-02

This RFC describes how and why we might write a new version of _rank_, our relevance testing tool.

## Background

We develop and test the relevance of our search results using a tool called _rank_. By making sure that our queries return the expected results for a set of known, indicative search terms, we can be confident that search is performing as intended.

Rank began as a browser-based UI for displaying a few simple tests which were run against the elasticsearch [ranking evaluation API](https://www.elastic.co/guide/en/elasticsearch/reference/current/search-rank-eval.html). It was written in next.js and typescript, deployed on vercel, and stored a lot of its tests and configuration as json.

These days, rank no longer has any kind of browser interface. Instead, rank is a CLI tool which allow developers to run a much broader range of search relevance tests, with utilities for managing the testing data and infrastructure. Ad-hoc experiments can be run locally by developers, while the tests are also run automatically in CI on a regular basis, with alerts set up for any regressions in search quality.

Rank is still written in typescript, and uses a lot of the same code as the original browser-based version.

It's taken us a while to figure out what rank is and how it should be used, and in that time, we've built up a lot of technical debt in the tooling.

Now that rank's purpose is more stable and its direction of travel is clearer, we should take the opportunity to rewrite some of the more problematic parts of its codebase.

## Components of the rank ecosystem

### Environments (CI and local)

Rank can be run locally to measure the effect that experimental mappings or queries will have on search quality.

We also run rank tests in CI to make sure that drift in the underlying dataset won't cause a regression in search quality or invalidate our tests.

This pattern works well. We should keep it!

### Elasticsearch cluster

Testing indices are held in a dedicated `rank` cluster, away from our production cluster. The test indices are snapshots of the production data, intermittently copied over from production clusters with [CCR](https://www.elastic.co/guide/en/elasticsearch/reference/current/xpack-ccr.html).

The rank cluster is kept separate so that tests can be run without worrying about expensive or long-running queries affecting production services.

Like the rest of our clusters, the rank cluster is defined and managed in terraform.

Again, this structure is good and we should keep it!

### CLI

The CLI is where the majority of rank's technical debt has built up, and where there is the most potential for improvement.

While javascript/typescript is an appropriate language for making straightforward rank eval API requests from a browser, it's not a great choice for writing CLIs or performing any complicated manipulation of the responses.

Data manipulation is cumbersome in typescript, and we've inherited a lot of the original code from the browser-based version of rank (for example, the way in which requests are bundled using [search templates](https://www.elastic.co/guide/en/elasticsearch/reference/current/search-template.html) currently makes it _harder_ to run batches of requests, instead of easier!).

We should rewrite rank's CLI and testing backbone in python, using the [elasticsearch python client](https://elasticsearch-py.readthedocs.io/en/v8.8.0/), [pytest](https://docs.pytest.org/en/7.3.x/), and [typer](https://typer.tiangolo.com/).

Typer includes a lot of the functionality that we've had to build ourselves in typescript (argument/option parsing and prompting, etc), and goes further in many cases (for example, it can [automatically generate --help](https://typer.tiangolo.com/tutorial/commands/help/) and full [static docs](https://typer.tiangolo.com/typer-cli/#generate-docs-with-typer-cli) for the CLI).

Moving to python will also give us access to data science libraries like [pandas](https://pandas.pydata.org/) and [numpy](https://numpy.org/), making it easier to develop more complex analyses of the test results.

Users should be able to install the rank CLI with `pip` from a local `pyproject.toml` (ie it shouldn't need to be published to registries like pypi). The CLI should run with a top-level `rank` command.

### Test configuration

Tests are currently formatted as json, and live in a `data` directory alongside `mappings`, `queries`, and `terms` (common search terms from real users, collected from the reporting cluster). At test time, we read these json documents, map them into some rigidly defined test structures, and then run them against the target index. The test results are then written to stdout.

These tests aren't data, and shouldn't exist as static files which are read by some smart test-constructing code. Test logic is over-abstracted, making it difficult to write new tests which are expressive of a test's intention, or how they're being scored.

We should instead be writing tests _as_ code, more tightly coupled with the test-runner. Each test should be expressive of the intent of the test, and of how its pass/failure is being calculated.

Pytest's [parametrised tests](https://docs.pytest.org/en/7.1.x/example/parametrize.html) and [fixtures](https://docs.pytest.org/en/6.2.x/fixture.html) might help us achieve this plain-language test-writing style.

### Rank eval API requests

Our testing needs have developed over time, and we rarely use elasticsearch's rank eval API in the way that it's supposed to be used. In many cases, the requests we use to analyse quality are straightforward `search` requests.

The outputs of our tests are often more binary than the rank eval API's responses, and we're discarding information about scoring which might be useful.
In other cases, we've extended our code to test things which the API doesn't support, eg relative positions of expected results.

These differences are hard to understand from the code, and are not well documented. A new implementation should be clearer about where those divergences are.

### Test indices

At the moment, we're able to test against indices copied from the catalogue API, ie `works` and `images`. We'd like to be able to test against other types of content like articles, exhibitions, events, functional content, and concepts.

These source indices live in different clusters, so supporting cross cluster replication into rank from multiple clusters in future would be necessary.

### Test outputs

We know that optimising search relevance is a game of compromises, and that we're unlikely to be able to satisfy every search intention perfectly. In other words, we expect some of our tests to fail every time, even when search quality is good.

For example, we might run a test for a new candidate mapping/query where document `abc` is expected to appear as the first result. A new version of the index might cause it to appear as the second result instead. The current version of rank would consider this a failure, and would alert us to the regression.

To keep things moving in cases where we're satisfied with the overall search quality, users can currently set a `knownFailure` flag on individual tests, allowing the full suite to pass as a whole even when individual tests fail.

`knownFailure`s are a useful but ugly bandage over an interesting problem. They obscure the severity of each failure during experiments, and make it harder to evaluate the development of search relevance over time.

While the example above might represent a minor degradation in search quality for one intention, it's not something we would normally consider a catastrophic failure. If the same change led to an improvement in search quality for a different set of intentions, we might still want to deploy it.

The scoring and passing of tests should be more nuanced, and should be able to account for the _ideal_ and _worst-case_ scenarios for each test.

We should still be alerted to any degradations in individual or overall scores in CI, and we should be able to set extreme thresholds for each test which would cause rank to fail.

NB This would represent a meaningful (but incomplete) step towards a proper [NDCG](https://en.wikipedia.org/wiki/Discounted_cumulative_gain) testing implementation, for which we currently don't have the data.

## Features

Having established the problems with the current rank CLI, we can start to think about what we'd like to be able to do with a new version.

- Setup and index management
  - Copy a production index to the rank cluster (without affecting production search)
  - Create a new index in the rank cluster with a given mapping, using data from a copied production index
  - Update candidate index config in the rank cluster
  - Check the progress of a reindex
  - Delete an index in the rank cluster
  - Fetch copies of the index config for a production index
  - Fetch copies of the queries which run in production search

- Local testing and experimentation
  - Run rank tests, outputting an overall pass/fail result along with a summary of the individual tests
  - Run an individual test, or a subset of tests
  - Run a search with a candidate query against a candidate index, outputting formatted results on the command line
  - Compare the speed of candidate queries against production queries

- CI testing
  - Run all tests in CI, outputting a pass/fail status with a summary of the individual tests

### CLI command tree

The following is a rough tree structure of the CLI commands which we'd like to support in v2.

```
rank
├── index
│   ├── list
│   ├── create
│   ├── update
│   ├── delete
│   ├── get
│   └── replicate
├── task
│   ├── check
│   └── delete
├── search
│   ├── get-terms
│   └── compare
└── test
    ├── run
    └── list
```

See [examples](./examples.md) for some examples of how these commands might be used.
