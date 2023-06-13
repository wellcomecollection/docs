# Examples of rank CLI usage

All flags in the following commands should be optional, and the CLI should prompt the user for any missing information, allowing them to select from the available options where appropriate.

```
rank
├── index
│   ├── list
│   ├── create
│   ├── update
│   ├── delete
│   ├── get
│   └── ccr
├── task
│   ├── check
│   └── delete
├── search
│   ├── terms
│   └── compare
└── test
    ├── run
    └── list
```

```bash
rank index list
```

List all the indices in the rank cluster.

```bash
rank index create --source <source> --target <target> --config <config>
```

Create a new index in the rank cluster, using data from a copy of a production index (also in the rank cluster), and a locally defined settings/mapping config.

```bash
rank index update --index <index> --config <config> --run
```

Update the settings/mapping config for an existing index in the rank cluster. Should allow the user to run the [update-by-query](https://www.elastic.co/guide/en/elasticsearch/reference/current/docs-update-by-query.html) for all documents immediately, or leave it to be run later.

```bash
rank index delete --index <index>
```

Delete an index in the rank cluster.

```bash
rank index get --index <index>
```

Fetch a copy of the settings/mapping config for an index in the rank cluster.

```bash
rank index ccr --source <source> --target <target>
```

Copy an index from the rank cluster to a production cluster using [cross-cluster replication](https://www.elastic.co/guide/en/elasticsearch/reference/current/ccr-what-is.html).

```bash
rank task check --task <task>
```

Check the progress/status of a reindex or update-by-query task.

```bash
rank task delete --task <task>
```

Cancel a task.

```bash
rank search --index <index> --query <query> --search-terms <searchTerms>
```

Run a search against an index in the rank cluster, outputting formatted results to stdout.

```bash
rank search terms 
```

Fetch a set of real search terms from the reporting cluster for each content type, and write them to a local file.

```bash
rank search compare-query-speed --index <index> --query <query> --terms <terms>
```

Run searches against an index in the rank cluster using a set of real search terms, and compare the speed of the candidate query against the production query.

```bash
rank test run --index <index> --query <query> --test-id <testId>
```

Run a test against an index in the rank cluster. Test ID should be optional, and if not provided, all tests should be run.

```bash
rank test list
```

List the available tests using a modified `pytest --collect-only`
