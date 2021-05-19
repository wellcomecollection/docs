# Incident retro - search not available 

**Incident from:** 2021-05-19

**Incident till:** 2021-05-19

**Retro held:** 2021-05-19

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




## Analysis of causes

The TF to describe infrastructure was in two stacks; you can change one without changing the other. Duplication of state without changing in both places caused the problem.

Plans for TF changes can be confusing


## Actions

**Team**
- Always collaboratively change critical infrastructure:
- TF diff
- Work collaboratively in person or via screen sharing remotely


**Robert**
- Remove the duplication of the stacks
- Add tags showing the TF configuration URL to key resources/TF state file
https://github.com/search?type=Code&q=org:wellcomecollection+terraformconfigurationurl
- Look at getting rid of platforminfrastructure/critical

