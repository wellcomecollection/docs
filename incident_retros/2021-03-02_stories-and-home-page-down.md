# Incident retro - stories and home page down 

**Incident from:** 2021-03-02

**Incident till:** 2021-03-02

**Retro held:** 2021-03-03

- [Timeline](#timeline)
- [Analysis of causes](#analysis-of-causes)
- [Actions](#actions)

## Timeline

2 March 2021

See https://wellcome.slack.com/archives/C3TQSF63C/p1614686143200300
https://wellcome.slack.com/archives/C01FBFSDLUA/p1614686253045200

11.55 updown alerts for:
Front End Homepage
Front End Stories
Front End Articles

12.00 NP can still see home page; JP cannot

12.00 AC confirms they can’t get to https://wellcomecollection.org/articles/Wcj2kSgAAB-3C4Uj not available (I think this is the same URL as checked by Updown)

12.01 AC can get to some stories but not others

12.03 AC suggests rolling back to the release from 11:20

12.03 JP: I don’t really understand enough about the wc.org architecture to know but I guess the issue is with the content app

12.05 AC: notably, CI is failing for the latest commit https://buildkite.com/wellcomecollection/experience/builds/1963

12.05 JP restarted the content app

12.07 agreed on rollback

12.08 AC We are rolling back to 5762fe6e-a3b1-40b1-bf51-c399cd2df35c

12.12 deployment done but not back up

12.22 RK, AC, JP, GE, DMc, AN voice called in Slack


12.30 DMc (in #wc-experience) There was a typo in ‘contibutor’ which Prismic was erroring with. Updating this on prismic.io now (but so far doesn’t appear to have solved the problem)

Discussion about changing the model or the code

12.52 Updown still down alerts
Front End Homepage
Front End Stories
Front End Articles

12.56 Where we’re at - contibutor has made its way into the Prismic schema and we’re going to stick with it for now to get a fix
That means updating the graph query to use that spelling and keeping the Schema in the Prismic JSON editor that way too
Use ‘contibutor’ typo in graph query - https://github.com/wellcomecollection/wellcomecollection.org/pull/6164 

1.00 https://buildkite.com/wellcomecollection/experience/builds/1966 

1.02 JG: Once the build is done, the tests are quite quick.
We just need to pass the deploy catalogue (ecr image) step, and I can deploy to stage.

1.17 JG: Deploying to stage. Probably 10 - 25 from now

1.21 JG: stage seems up.

1.23 JG deploying to prod

1.28 Updown recovery:
Front End Homepage
Front End Stories
Front End Articles


## Analysis of causes

Schemas in Prismic and generated by devs had got out of sync. Possibly was updated by devs but not updated in Prismic.

There was no way to rollback to a previous version of the schema that was in Prismic.


## Actions

**Gareth E**
- Document process for updating the schema
- Add contributor / save something on Prismic / deploy fix in the app / remove contibutor / save something on Prismic
- Investigate weekly backups so they can be used for this sort of problem in future
- Investigate a paid option that will give a development environment (Prismic is currently on the Platinum plan)

**David**
- Look into Prismic error handling

**Robert**
- Investigate why errors slipped through CloudFront

