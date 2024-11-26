# RFC 065: Library Data Link Explorer


# Library Data Link Explorer

## Overview

This RFC outlines the plan for the Library Data Link Explorer web application. This tool will enable Collections Information colleagues the ability to view and debug work relationships independently, potentially replacing the workflow of requesting a developer-run script to produce a matcher graph .dot file. 

![Example DOT Notation Graph](https://hackmd.io/_uploads/ry15cEQmkl.png)
*Example .dot graph returned by Matcher logic.*


**The application will consist of:**

- An API providing an endpoint that utilises existing matcher logic which returns a JSON graph structure for a given work ID.
- A frontend interface that allows users to input a work ID and displays either a graph of connected works or an error message if no relations exist.

### Background Context

The catalogue data on [wellcomecollection.org](https://wellcomecollection.org/search) is created from multiple source systems. Different records in various source systems may refer to a single cultural artefact (referred to as a "work"), and one of the functions of the [catalogue pipeline](https://github.com/wellcomecollection/catalogue-pipeline) is to identify links between these source records and to merge them into single works.

Records may be linked implicitly by sharing common identifiers, but more often the linking data is manually added and managed by colleagues in collections information (CI). This usually takes the form of an identifier for one system being stored in a particular field in another. This can lead to rich and complex tangles of records where the merging logic sometimes leads to results that are unexpected or even non-deterministic.

However, CI colleagues currently have no visibility over how records are linked other than by manually inspecting individual records. Since 2021, our team has maintained a script for visualising the way records are linked (we call these "matcher graphs" after the name of the pipeline service which identifies the links), but this script can only be run by software engineers due to the AWS permissions it requires. Since the source information belongs to Collections Information, we would like them to be able to view these graphs (nodes and edges) themselves.

### How will it work?


1. **User inputs a work ID**: A Collections Information staff member enters an work ID into the application.
2. **API fetches the data**: The API queries Elasticsearch for records linked to the work ID.
3. **Frontend displays the graph**: The frontend renders a visual graph of nodes (works) and edges (relationships), allowing users to explore the connections using a graph library.
4. **Enhanced Collections Information workflow**: This allows Collections Information I colleagues to independently view and explore relationships between records without requiring software engineer assistance, boosting productivity and collaboration.

---

## Backend

- An API endpoint, powered by AWS Lambda to:
    - query Elasticsearch for works, returning matched works of the given work id
    - generate a DOT notation graph for this given work id using matcher logic within the endpoint
    - transform this DOT notation into JSON ready for front end consumption
- Accessed securely using AWS Secrets Manager for credentials for Elasticsearch

### Helpers

- Use the build of the content-api as an example API endpoint
- JSON conversion is not strictly necessary, but useful for better graph libraries
- [existing matcher logic](https://github.com/wellcomecollection/catalogue-pipeline/blob/main/pipeline/matcher_merger/matcher/scripts/getMatcherGraph.ts)

### Technical Considerations

- Frameworks and Dependencies
    - TypeScript
    - aws-lambda
    - ts graphviz for generating dotnotation ready for conversion?
    - AWS SDK for secrets - or is this done in Elasticsearch?
    

---

## Frontend

- A Next.js application that:
    - provides a user interface for CI staff to enter a work id
    - renders the matcher graph dynamically using a graph library (see candidates below)
        - uses nodes and edges to show relationships
    - handle error display when no relationships are present?
    - potentially offer more advanced features than is currently possible (i.e, zoom, node highlighting
- Accessed securely - consider later down the line

---

## Infrastructure and Deployment

- Use GitHub Actions for CI/CD to deploy the backend and frontend
- keeping repositories separate for clarity and modularity between the API/backend logic and frontend application and deployment

---

## Graph Library Candidates

- https://js.cytoscape.org/
- https://www.sigmajs.org/ + [ReactSigma](https://sim51.github.io/react-sigma/) for prebuilt components
- https://github.com/visjs/vis-network
- Graphviz wrappers - https://github.com/magjac/d3-graphviz, https://github.com/mdaines/viz-js

---

## Testing

- Jest for backend logic
- Playwright for API and frontend e2es

---

## Workflow

1. API Development
    1. using the content-api as a guide for structuring the api endpoint
    2. implement the matcher logic within the endpoint
        1. requires cleaning and configuring to both (work) and work with this setup
    3. add transformation logic to convert dot to JSON
    4. secure elasticsearch queries using Secrets Manager
2. Frontend Application build
    1. design base wireframe for working against
    2. set up Next application
    3. integrate API endpoint for dynamic data fetching
    4. render graphs using chosen graph library, giving time to pro/con each
3. Testing 
    1. done alongside these individual steps, to ensure logic is tested via Jest and Playwright
        1. inc. e2es and unit tests
4. Deployment
    1. Using GitHub Actions to automate testing and deployment to production

---

## Project Assessment

I will use this project to build a Project Report as part of my Endpoint Assessment - **Assessment method 1: Work-based project with questioning**
- Project work details from page 6 of the [Software Developer Level 4 Assessment Plan](https://www.instituteforapprenticeships.org/media/5222/st0116_software-developer_l4_ap-for-publication_270521.pdf)

> The apprentice may work as part of a team which could include technical internal or external support however the report will be the apprentice’s own work and will be reflective of their own role and contribution. 

- Any pointers, critique, and helpful suggestions are most welcome! 
    - including review, pair-programming, and planning assistance
- The application itself is not marked, the project report will be used in interview to assess my contributions, work, and understanding of the project and a best-practice workflow
- While inevitably most of the build and code will be mine, assistance and team work is permitted.