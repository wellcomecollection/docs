# Phase 6: Eliminate Duplicate Index Calls

[← Back to Index](./README.md)

**Effort:** 30 minutes  
**Risk:** Low  
**Priority:** Medium  
**Status:** Done - [#12989](https://github.com/wellcomecollection/wellcomecollection.org/issues/12989)  
**Previous:** [Phase 5: Restriction Status](./11-phase-5-restriction-status.md)  
**Next:** [Phase 7: Cleanup](./13-phase-7-cleanup.md)  

## Goal

Remove duplicated calculations of "which canvas is currently showing" across components.

## What this phase originally assumed

As planned, this was a find-and-replace: since `currentCanvasIndex` was to be on the context, swap every `queryParamToArrayIndex(query.canvas)` call for it, in `Thumbnails.tsx`, `NoScriptImage.tsx` and `MultipleManifestList.tsx`.

Neither half of that held by the time the phase came round:

- `currentCanvasIndex` was deliberately never added to the context. It would duplicate `query.canvas`, which is already there, and the 1-based canvas number and the 0-based array index are kept as distinct concepts throughout. See the note in [README](./README.md).
- None of the three named files calculate a canvas index any more. `Thumbnails.tsx` calls `queryParamToArrayIndex` on `query.page` and `MultipleManifestList.tsx` on `query.manifest` - different query params, unrelated to the current canvas - and `NoScriptImage.tsx` doesn't call it at all, having moved to the shared `getCanvasesForPage` helper in Phase 3.

So the phase became an audit of the whole `refactored/` directory instead.

## What the audit found

One genuine duplicate, in `GridViewer.tsx`: the memoised `Cell` recalculated `queryParamToArrayIndex(query.canvas)` for its own `aria-current`, once per rendered grid cell, while the parent already calculated the identical value for its scroll-to-row effect. Fixed by calculating it once in `GridViewer` and passing it down through `itemData`, plus a first test for that component.

Four lookalikes were checked and deliberately left alone, being different logic that happens to read similarly:

- `GridViewer`'s `Cell` and `VirtualizedImageViewer`'s `ItemRenderer` each have a local `currentCanvas`, but those are per-cell and per-row canvases from iterating the whole list, not the one current canvas on the context.
- `VirtualizedImageViewer` calls `hasRestrictedItem(canvases[0])`, which is about the first canvas specifically, for a margin adjustment - not the current one.
- `IIIFViewer.tsx` reads `document.fullscreenElement` directly, to skip resize handling while a native video player is fullscreen. That's a different question from the fullscreen toggle state centralised in Phase 3.

## Success Criteria

The criteria as originally written, with what actually happened against each:

- [x] No more `queryParamToArrayIndex(query.canvas)` calls in consuming components - met, though by this point the only one left was the `GridViewer.tsx` duplicate above
- [ ] All components use `currentCanvasIndex` from context - not done, and no longer wanted: the value was deliberately never added to the context
- [x] Test coverage maintained - `GridViewer.test.tsx` added, the component's first test

## Time: ~30 minutes

---

**Next:** [Phase 7: Cleanup](./13-phase-7-cleanup.md)
