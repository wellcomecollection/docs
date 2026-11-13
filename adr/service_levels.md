# Service levels

Last updated: 13/11/26

---

This records the support hours we offer for Wellcome Collection services, which user journeys must work, and how we set and track availability targets. The support position is decided, and the availability targets below were agreed on 13 November 2026.

Tracked in [platform#6794](https://github.com/wellcomecollection/platform/issues/6794).

## Support hours

We support our services during UK office hours, 9am to 5pm on weekdays. This is a deliberate position, accepted by the Head of Digital Experience and Engagement as an owned risk.

Outside office hours, support is best effort. If a service goes down on a Sunday it may stay down until Monday. We may make exceptions where leaving an incident unresolved carries a significant security or privacy risk, a significant financial risk, or a significant reputational risk. If an incident like that cannot be fixed quickly and safely, we take the affected service offline until the next working day. The handbook page on [out-of-hours support](https://github.com/wellcomecollection/developer-handbook/blob/main/incident-management/out-of-hours-support.md) gives examples of each.

## User journeys that must work

The journeys that must work are the ones our [LogicMonitor checks](logicmonitor.md) test. Each check requests a page or API response and raises an alert after two consecutive failures. They cover:

- content pages on wellcomecollection.org: the homepage, stories, what's on, visit us, and a story, an event, an exhibition and a visual story
- search and catalogue pages: collections, works search, a work, images search, an image and a concept, plus robots.txt
- the catalogue API: works and images, both search and single record
- images: a file on i.wellcomecollection.org and the DLCS health endpoint

A check passes when the page responds. It does not check the page content.

Sign-in, account pages, item requesting, the content API and IIIF image and presentation requests are not checked today.

The check definitions live in the [`wellcome-devops` repository](https://github.com/wellcometrust/wellcome-devops/tree/main/infrastructure/monitoring_logicmonitor) (private). When a journey is added or removed there, update this list.

## Availability targets

Each target is a service level objective (SLO) declared in the `manifest.yml` of the repository that owns the service. Backplane (internal), our developer portal, reads those files, so the manifest is the record of each target, its owner and its window. Backplane checks that the declarations are valid today, and tracking each SLO against its error budget is planned. Once the targets are agreed this page will point at the manifests rather than repeat the numbers.

We measure availability as the share of requests not answered with a server error (a 5xx response), over a rolling 28-day window. Client errors such as 404s count as good.

### Targets

| Service | Repository | Measured at | Target | Measured, 90 days | Lowest 28-day window |
|---|---|---|---|---|---|
| Website | wellcomecollection.org | load balancer, content app | 99.5%, agreed | 99.9256% | 99.7344% |
| Account pages | wellcomecollection.org | load balancer, identity app | 99.95%, agreed | 99.9980% | 99.9943% |
| Catalogue API | catalogue-api | API gateway | 99.5%, agreed | 99.8988% | 99.6343% |
| Identity API | identity | API gateway | 99.5%, agreed | 99.8163% | 99.6488% |

The website's SLO is measured at the content load balancer. We also measured the CDN across all paths (99.9832% over 90 days, lowest 28-day window 99.9166%) and did not choose it. That figure is approximate, because CDN error counts are estimated from the error rate CloudWatch publishes.

No target is set for catalogue-pipeline. It is a batch pipeline with no request-based measure, and a freshness measure would need a metric we have not yet identified.

### How these were measured

The figures come from hourly CloudWatch request and 5xx counts from 15 August to 13 November 2026, the same calculation as the load balancer availability template in Backplane's specification. Load balancer figures count errors from our applications only, which leaves out errors the load balancer generates for traffic that did not come through the CDN.

Each target was set as the highest of 99%, 99.5%, 99.9% and 99.95% that every rolling 28-day window in the 90 days met.

Most of the errors in the period came from one incident on Sunday 13 September 2026, when the catalogue API returned server errors for about five hours. With a 99.9% target the website and catalogue API would have missed in 45% of 28-day windows, all because of that incident. During office hours the website and catalogue API both measured above 99.99%.

The identity API handles about 960 requests a day, so a handful of errors moves its figure a lot. Its measure also misses sign-in failures caused upstream: the four-hour sign-in outage on 28 September 2026 produced almost no 5xx responses.

Statuspage is not used as a measure because it does not record every incident or its full duration.
