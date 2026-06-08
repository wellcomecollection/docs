# Incident retro - registration
**Incident from:** 2026-06-05

**Incident until:** 2026-06-07

**Retro held:** 2026-06-08


- [Timeline](#timeline)
- [Analysis of causes](#analysis-of-causes)
- [Actions](#actions)

## Timeline

See [https://wellcome.slack.com/archives/C01FBFSDLUA/p1770206278034739 ](https://wellcome.slack.com/archives/CQ720BG02/p1780829906678559)

5 June 2026

#wc-platform-alerts: <br>
1.30 and 4.00 alerts in alerts channel, put it down to testing rather than genuine issue

7 June 2026

11.58 RK Looking at a possible identity issue. I can sign in alright, register a new account but I'm not getting verification or forgot password emails.

I wonder if something got changed accidentally in Agnes' update last week.

If this is a problem it means sign ups aren't working at the moment, investigating. 

12.21 RK My demo stuff is completely separate from the current system, so I don't think that can be the culprit.

13.08 RK Ok, i've got a temp fix in for this identity issue.
```
  "details": {
    "email_type": "verify_email",
    "notification_type": "verify_email",
    "to": "[email address]",
    "error": "Error sending email: Invalid login: 535 Authentication Credentials Invalid"
  },
```

Is the error in Auth0, so this made me go and check the SMTP user credentials.

These are derived cryptographically from IAM user credentials: https://docs.aws.amazon.com/ses/latest/dg/smtp-credentials.html 

13.20 RK When I looked at these the username was ##SMTP_USER## ,  which is obviously not an IAM Access Key ID. Speculating that the terraform update had borked setting these somehow, I created a new set of IAM credentials, re-derived the password and updated the settings.

I am getting registration e-mails when testing in prod again, so I think that this issue has been temporarily resolved.

The impact will have been that new users would have been unable to register fully and that users wishing to reset their passwords could not.

This would have been since midday Friday when the last change was applied by @Agnes. I approved this PR and thumbs'ed up the change.

In real terms this looks like 8 actual users were impacted from the logs.

(a) we should not have made this change on a Friday, (b) we should have a manual test script that involves ensuring that emails get sent in prod after deployment (I think automated tests in stage might not catch this because they do not use the same SMTP, we send real e-mails but use mailtrap.io so we can catch them in testing!), and (c) this is what happens when we don't make changes to a service for ages then work under pressure. 

---
Permanent fix put in 8/6/26 am by rerunning and applying TF in stage and prod.

## Analysis of causes

What happened that we didn’t anticipate?

Don’t know what happened: Friday - key ended up in wrong field in stage and prod.

Why didn’t our safeguards catch this?

We should have a manual test script that involves ensuring that emails get sent in prod after deployment (I think automated tests in stage might not catch this because they do not use the same SMTP, we send real e-mails but use mailtrap.io so we can catch them in testing!)

How to test ID changes

Smoke tests exist but not that thorough: doesn’t check an email has been sent, for example. <br>
Some situations are tested but not all. <br>
Emails don’t work locally, don’t have a dev tenant.


## Actions

**AG - for planning**
- Verify that errors are in 3rd party code, not our code
- For noisy alerts, choose which Auth0 errors to be alerted on

**RK - for planning**
- Document what to do when testing, including testing that emails are sent


Folio changes:

- Dev tenant with same set up to work with locally running version of the site? / Add automated e2e tests
