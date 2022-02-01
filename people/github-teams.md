# How our GitHub organisation is managed

In general, we assign repository permissions to [teams in our organisation][teams], not individual users.

This has several benefits:

-   Adding a user to a team is a single operation that gives them access to all the relevant repos, rather than adding them to each repo individually.
    Similar for removing access when somebody leaves.

-   Everyone in a team will have consistent permissions, rather than a mishmash of individual permissions.

-   Team names are more widely understood, and so easier to reason about and know if permissions are correct.

    e.g. if you see Jane Bloggs has access to a repo, you may not know who that is or whether that's right – but you would know who the "Digital Editorial" team is, even if you don't work on that team.

Typically we give Maintainer status to at least one person who actually works on that team, so they can add/remove team members without getting a GitHub admin involved.

[teams]: https://github.com/orgs/wellcomecollection/teams
