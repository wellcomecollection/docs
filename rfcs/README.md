# Request for comments (RFC)

An RFC is a place to discuss possible changes to the Wellcome Collection platform.

---

Please create an RFC if you have an idea about how to make a big change to the way we do things currently and need a place to share that with your colleagues.

The process of creating an RFC, discussing that RFC in a pull request, amending and merging is important to provide a forum for all to contribute to the platform.

When an RFC is merged it provides a guide to implementing that change when it is useful to do so, or provides context to an [Architecture decision record (ADR) document](../adr/README.md).

## Table of contents

<dl>
  <dt>
    <a href="./017-url_design">RFC 017</a>: URL design
  </dt>
  <dd>
    Some principles for how we design URLs.
  </dd>

  <dt>
    <a href="./047-catalogue-api-index-structure">RFC 047</a>: Changing the structure of the Catalogue API index
  </dt>
  <dd>
    Updating the catalogue API to serialise responses from an opaque <code>display</code> field, rather than parsing the internal model structure used by the pipeline.
  </dd>

  <dt>
    <a href="./049-catalogue-api-aggregations-modelling">RFC 049</a>: Changing how aggregations are retrieved by the Catalogue API
  </dt>
  <dd>
    Updating aggregations to match the changes from RFC 047 and to reduce the coupling between the pipeline/API repos.
  </dd>

  <dt>
    <a href="./050-concepts-api">RFC 050</a>: Design considerations for the concepts API
  </dt>
  <dd>
    Some discussion about how we might model subjects and people in the concepts API.
  </dd>

  <dt>
    <a href="./059-059-splitting-pipeline-terraform">RFC 059</a>: Splitting the catalogue pipeline Terraform
  </dt>
  <dd>
    Some changes to the workflow for managing different instances of the catalogue pipeline in Terraform; primarily aimed at improving isolation between different pipelines.
  </dd>
</dl>
