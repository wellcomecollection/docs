# Library management

We have multiple libraries each in its own repo and some of them depend to other forming a chain. In many situatios (but not all) we end up using all these libraries together, so we need them to be split but we also need to know that they can work together.

These are the problems that I find with the current setup:
- Discoverability of what libraries form part of a chain and how are they linked is very poor. It involves jumping across different github projects and it involves knowing the names of these projects cause the released artifacts don’t have the same name as the github repo and we haven’t been consistent in naming of repos and libraries.
- If you’re unlucky enough that a change that you need to make is in one of the libraries at the end of a chain and it requires changing something at the beginning of a chain, you have to release ~ 4 projects (so 4 PRs, 4 travis builds etc). And that’s assuming that when you use those newly relased libraries you don’t find anything that forces you to go back again.
- As they are released individually, there is no way to enforce in CI that our libraries work together at any given time in CI at the moment, even though that is a requirement. So you can (and it has happened) end up with libraries that pass the build but are effectively unusable because they can’t work work with others.

I think these problems are mostly self generated, because we consider these libraries as individual pieces, when they are not.
I think it would be more useful to consider them pieces of an ecosystem and we should release the whole ecosytem every time we release something.

So, I mean:
- One scala-libraries repo (or something like that - whatever)
- One version in the repo
- One declared set of third party dependencies
- Multiple modules within the repo and each module results in an individual artifact that can be imported in our projects
- One change in any of the modules triggers a release which means:
    - increment the version for the whole repo
    - publish a new version of all the modules (even if the change affects only one)

That would
- Improve discoverability of how our libraries connect to one another (and in general of how many we have)
- Enforce that we import the same version of third party libraries everywhere (and make upgrades easier)
- Allow writing integration tests that enforce that they can work together