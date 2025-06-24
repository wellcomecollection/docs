# Using C4 Model at Container Level for Service Documentation

**Status:** Accepted

**Date:** 2025-06-24

## Context

We need a consistent and clear way to describe our services for both new and existing team members. The goal is to provide a high-level overview of our systems that is easy to understand and maintain. We want a method that can be easily integrated into our existing Markdown-based documentation.

The [C4 model](https://c4model.com/) is a popular and effective way to describe software architecture at different levels of abstraction. It has been successfully adopted by companies like [Spotify](https://engineering.atspotify.com/2022/07/software-visualization-challenge-accepted) to improve their technical documentation.

## Decision

We will adopt the C4 model for documenting our services, specifically focusing on the "Container" level. This provides a useful degree of granularity for newcomers to get an overview of our systems without being overwhelmed by implementation details.

Diagrams will be created using Mermaid.js, allowing them to be embedded directly within our documentation. 

A [service template](../architecture/services/template.md) has been created that includes a placeholder for a C4 container diagram.

This approach is not a replacement for more detailed architecture diagrams that may exist within the repositories of the services they describe. Teams are encouraged to continue maintaining more granular diagrams where they are useful.

## Consequences

- **Clarity and Consistency:** All service documentation will follow a consistent structure, making it easier to understand the architecture of different services.
- **Improved Onboarding:** Newcomers will have a clear starting point for understanding our systems.
- **Version Controllable Diagrams:** Using Mermaid.js means that our architecture diagrams will be stored as text and version controlled alongside our documentation.
- **Scope Limitation:** The C4 container diagrams are intended to provide a high-level overview. They are not meant to capture every implementation detail. More detailed diagrams should be maintained in the relevant service repositories where necessary.
