# Capacity and performance

Last updated: 23/11/26

---

This records how we size our services, who decides, the baselines we hold, and how we find capacity risk before it becomes an incident. It answers assessment rows AWS-33 to AWS-36 from the Digital & Technology (D&T) service management assessment of October 2026. Tracked under [platform#6790](https://github.com/wellcomecollection/platform/issues/6790).

## Fixed task counts on public services

The website and the public APIs run a fixed number of ECS tasks, set in Terraform. The content app runs 6 tasks and the catalogue API runs 3 each of search, items and concepts. The identity API runs 3. This is deliberate. CloudFront caching absorbs most changes in demand, and the load that has hurt these services has come from bots and scrapers, which autoscaling on CPU would follow rather than stop. In September 2026 we declined autoscaling for the search API as too complex for what it would buy ([platform-infrastructure#547](https://github.com/wellcomecollection/platform-infrastructure/issues/547)).

Back-end workers scale on queue depth. Their bounds are in Terraform and change through reviewed pull requests, as the [change model](change_model.md) describes.

Moving a task count or an Elastic Cloud deployment within the [scaling bounds](change_model.md#scaling-bounds) is a standard change. Anything beyond them, including adding autoscaling to a public service, is a normal change.

## Who decides

| Decision | Who decides |
|---|---|
| Task counts, memory and CPU for a service | Lead engineer of the owning team |
| Elastic Cloud cluster sizing | The platform team, with the lead engineer accountable |
| Spend above an account's monthly budget | Head of Digital Experience and Engagement, as in [service ownership](service_ownership.md) |

## Baselines

The availability targets in [service levels](service_levels.md) are our performance baseline for the services that have one. The alarm thresholds that [alert routing](alert_routing.md) describes, on latency, 5xx rates and queue age, are the point at which we act. We do not keep separate capacity baselines for each service.

## Load testing

A new public service, or a change that is expected to raise load on an existing one, is load tested before it goes live. The test is recorded on the service's issue with the request rate reached. The Identifiers API test in October 2026 (400 requests a second) is the model.

## Demand and early warning

Each quarter, alongside the [service ownership](service_ownership.md) review, the lead engineers look at request and cost trends per account and at Elastic Cloud cluster use, and note any known event that will change load, such as an exhibition opening or a catalogue cutover. The review is recorded as an issue on the platform board.

Capacity risks we accept are recorded on the issue where the decision was made, with the label `accepted-risk`.

## Related documentation

- [Service levels](service_levels.md)
- [Change model](change_model.md)
- [Service ownership](service_ownership.md)
- [Alert routing and severity](alert_routing.md)
