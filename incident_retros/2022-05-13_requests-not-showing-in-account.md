# Incident retro -  requests not showing in account

**Incident from:** 2022-05-13

**Incident until:** 2022-05-13

**Retro held:** 2022-05-13

- [Timeline](#timeline)
- [Analysis of causes](#analysis-of-causes)
- [Actions](#actions)

## Timeline

13 May 2022

See https://wellcome.slack.com/archives/C01FBFSDLUA/p1652434124540789 

01.33 Viewing, making requests, seeing if something is requestable not available

08.13 AC [notices](https://wellcome.slack.com/archives/CQ720BG02/p1652425989247399) errors in the identity (frontend) app

10.24 AC [notices](https://wellcome.slack.com/archives/C8X9YKM5X/p1652433888903209) 500s from identity API (can’t view item requests) 

10.28 JP: can’t view item requests on prod, nor make a request

10.31 JP checked the API, the authorizer. Neither suspicious

10.37 SSL is the root cause. Attempting to fix by creating a new certificate in the console.

10.47 Cert validation record does exist but not liked by AWS

10.51 AWS Certificate Manager cert validation most likely the underlying cause. JP created the record set.

10.52 “One or more domain names has failed validation due to a certificate authority authentication (CAA) error. Learn more.”

10.52 AC: At some point AWS “forgets” your validation records and stops renewing certs

10.59 JP Fixed. Confirmed by AC/NP



## Analysis of causes
SSL certificate was out of date

SSL certificate wasn’t automatically renewed

Also to be looked at: noisy alerts channel


## Actions

**Jamie**
- Handle identity API proxy errors which don’t have a response [#7970](https://github.com/wellcomecollection/wellcomecollection.org/pull/7970) - DONE

**Alex**
- Add Cloudwatch log URL to alerts to take you to the right account with text added to help with debugging
- Turn on CloudFront logging (with filtering)
