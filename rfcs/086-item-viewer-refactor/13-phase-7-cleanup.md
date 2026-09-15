# Phase 7: Cleanup

[← Back to Index](./README.md)

**Effort:** 1-2 hours  
**Risk:** Low  
**Priority:** Required (after toggle has been defaulted to ON)  
**Status:** Not started - [#12990](https://github.com/wellcomecollection/wellcomecollection.org/issues/12990)  
**Previous:** [Phase 6: Duplicate Index Calls](./12-phase-6-duplicate-calls.md)

## Goal

Clean up feature flag infrastructure after successful adoption. Remove legacy code, promote the refactored tree to be the only one, and finalise the implementation.

## When to Do This

**Only after:**
- Toggle defaulted to ON for 1+ week and PM approved
- No issues reported
- All metrics stable
- Team confidence is high

Note that the toggle can't go on publicly until the temporary badges and console logs are removed - see item 1 of [#13273](https://github.com/wellcomecollection/wellcomecollection.org/issues/13273).

## Steps

The steps below were rewritten once Phases 0-6 were done, because the original ones referenced a file layout that was never built (`ItemViewerContextV2`, `.legacy.tsx`/`.refactored.tsx` filename suffixes). The paths here are the real ones.

### 7.1 Remove the feature flag

**File:** `toggles/webapp/toggles.ts`

```typescript
// DELETE from featureFlags:
{
  id: 'itemViewerRefactor',
  title: 'Item viewer refactor',
  initialValue: false,
  description:
    'Displays the refactored item viewer instead of the current one.',
  type: 'experimental',
},
```

Deploy the toggles package afterwards, so the flag stops being served from `toggles.wellcomecollection.org/toggles.json`.

### 7.2 Delete the legacy viewer and its context

```bash
cd content/webapp
rm -r views/pages/works/work/IIIFViewer/legacy
rm contexts/ItemViewerContext/legacy.tsx
```

Then delete any types that only legacy used.

### 7.3 Promote the refactored viewer

`views/pages/works/work/IIIFViewer/index.tsx` is the `dynamic()` switch between the two trees. It goes, and `refactored/index.tsx` takes its place:

```bash
cd content/webapp/views/pages/works/work/IIIFViewer
rm index.tsx
mv refactored/* .
rmdir refactored
```

### 7.4 Collapse the context

`contexts/ItemViewerContext/index.tsx` is a barrel that picks legacy or refactored on the flag. With legacy gone it has no job: fold `refactored.tsx` into `index.tsx` and delete the barrel's switching logic.

While doing so, remove:

- the `console.log` that reports which context is in use, and the `window.__ivr_context_logged` global declaration that guards it (both marked TODO in the file)
- `isRefactoredContext` from the context type and its default value - the discriminant only existed to narrow the legacy-or-refactored union

### 7.5 Consolidate the import paths

Components currently reach the context two ways, and both need to end up on one path:

```bash
cd content/webapp
grep -rl "contexts/ItemViewerContext'" --include="*.ts" --include="*.tsx" .      # via the barrel
grep -rl "contexts/ItemViewerContext/refactored" --include="*.ts" --include="*.tsx" .
```

At the time of writing that's 32 files on the barrel and 16 importing `refactored` directly.

### 7.6 Simplify the test harness

`test/fixtures/iiif/render.tsx` carries the migration's dual-context machinery: `renderWithContext`'s `useRefactoredContext` option, the `RenderWithContextOptions` discriminated union, `RenderWithRefactoredContextOptions`, and separate legacy/refactored mock context factories. All of that collapses to a single context.

Individual test files then drop the `jest.mock` of `useFeatureFlags` that forces `itemViewerRefactor: true`, and the `useRefactoredContext: true` argument at each call site.

### 7.7 Remove unused props

Identify components that can drop props now that context provides the data.

### 7.8 Type cleanup

Ensure all TypeScript types reflect the final context shape. Remove any temporary types used during migration.

### 7.9 Documentation

- [ ] Update inline comments that describe the legacy/refactored split - `IIIFViewer/index.tsx` and the context barrel both carry explanatory comments that die with them, but others reference the split in passing
- [ ] Remove any "TODO: remove after itemViewerRefactor is fully rolled out" comments
- [ ] Update this RFC's status, and close out [#13273](https://github.com/wellcomecollection/wellcomecollection.org/issues/13273) items that only existed because of the split

## Success Criteria

- [ ] No `legacy/` directory under `IIIFViewer`, and no `legacy.tsx` context
- [ ] No `refactored/` directory - its contents sit directly under `IIIFViewer`
- [ ] Feature flag removed from `toggles.ts` and the toggles package redeployed
- [ ] One import path for the context, no flag-switching barrel
- [ ] No `isRefactoredContext`, and no migration console logs
- [ ] All tests still pass
- [ ] TypeScript compiles with no errors
- [ ] Application runs correctly
- [ ] Code is clean and maintainable

## Time: 1-2 hours

---

The IIIF Viewer context refactoring is complete!

**See also:**
- [15-risks-and-success.md](./15-risks-and-success.md) - Final success metrics
