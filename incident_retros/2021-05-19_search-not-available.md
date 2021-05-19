# Incident retro - search not available 

**Incident from:** 2021-05-19

**Incident till:** 2021-05-19

**Retro held:** 2021-05-19

- [Timeline](#timeline)
- [Analysis of causes](#analysis-of-causes)
- [Actions](#actions)

## Timeline

See https://wellcome.slack.com/archives/C01FBFSDLUA/p1621414892000600

18 May 2021 
JG noticed stacks infra in Cloudfront; RK created a PR 176 to remove it. 

19 May 2021

Morning

RK PR applied in user-facing stack, needed TF change to apply it.
Checked collection straight away and saw it wasn’t working

9.59 ALERT DOWN messages for 
- Images API Search
- Works API Search
- Front End Works Search (Origin)
- Front End Single Work Page (Origin)
- Images API Single Image
- Works API Single Work
- Wellcome Images Redirect
- Front End Single Work Page (Cached)
- Front End Works Search (Cached)

10.01 AC: no requests are being routed to the API (requests to the search API had dropped off in the logging cluster)

10.01 RK: Applying https://github.com/wellcomecollection/platform-infrastructure/pull/176 seems to have borked something

10.02 questions about the tf plan

10.02 RK: I am reverting to main and re-applying [didn’t do this in the end]

10.04 RK: specifically it was the critical/user_facing portion. See code at https://wellcome.slack.com/archives/C01FBFSDLUA/p1621415062003600

10.04 JP: where did catalogue_api_delta go?

10.06 AC: Did you check to see if there was a clean plan/apply before you started your changes in the PR?
this required an upgrade of TF from pre 0.12 so doing that occluded an easy diff
makes sense
but putting this diff in the PR would defo have avoided this issue

10.07 NP sent out comms to say search wasn’t available, and being worked on

10.08 JP: 99% sure that the issue is with the catalogue_api_delta origin

catalogue_api is currently pointing at catalogue.api.wellcomecollection.org, which no longer has anything behind it

I touched it about 3 weeks ago

did the state move?

10.09 AC [should it be at] critical/user_facing?
RK: this is what i modified
JP posted links to tf  https://wellcome.slack.com/archives/C01FBFSDLUA/p1621415399009700 

10.10 AC If you did touch it last month Jamie, it seems like the Terraform has gone walkabout
could this be to do with a branch renaming, maybe?

RK: I have manually updated the origin to point at that domain
looks like the lights are coming on again

RECOVERY messages sent for:
- Front End Works Search (Origin)
- Front End Single Work Page (Origin)
- Images API Single Image
- Wellcome Images Redirect
- Works API Single Work
- Front End Single Work Page (Cached)
- Images API Search
- Works API Search
- Front End Works Search (Cached)

10.11 JP: The tf code on main is correct… so where has the state gone?

10.12 RK: suffice to say I should have posted the bloody diff in the PR and got that reviewed before going gonzo

10.13 NP sent out comms to say the issue is fixed

10.14 AC: We have that CloudFront distro defined in two places

10.21 AC: 
A couple of notes from Jamie and my conversation:
- We started putting TerraformConfigurationURL as a tag on resources, then stops. Revisiting that would have caught this issue when it tried to change.
- Applying the change in the cloudfront directory might break things; our proposed fix is to revise things by hand until the plan delta is zero, and then remove this distro from user_facing.





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

