# RFC 086: IIIF Viewer Context Refactoring

**Status:** Phases 0-6 complete. Phase 7 (cleanup) is blocked on the `itemViewerRefactor` toggle being defaulted to ON for 1+ week.  
**Estimated effort:** 14-17 hours  
**Last modified:** 2026-09-15T10:31:29+00:00

## Purpose
This folder contains a comprehensive plan to refactor the IIIF Viewer context to eliminate code duplication and centralise derived state calculations.

**Key principle:** Write automated tests BEFORE refactoring (test-first approach), then use manual testing for extra confidence.

## Names in these documents vs the code

The phase documents were written before implementation, and use provisional names the code doesn't match. Translate as follows when following them:

| In these documents | In the code |
|---|---|
| `contexts/ItemViewerContextV2/` | `content/webapp/contexts/ItemViewerContext/refactored.tsx`, with `legacy.tsx` beside it and `index.tsx` selecting between the two on the toggle |
| `Component.legacy.tsx` / `Component.refactored.tsx` | `IIIFViewer/legacy/Component.tsx` / `IIIFViewer/refactored/Component.tsx` - directories, not filename suffixes |
| `iiifViewerRefactored` toggle | `itemViewerRefactor` |

`currentCanvasIndex` also never went onto the context: it would duplicate `query.canvas`, which is already there. Several documents list it as a context value - Phase 6 in particular is written on the assumption that it exists.

## Table of Contents

### Understanding the Problem
- [01 - Overview](./01-overview.md) - Problem statement, current architecture, and duplication examples
- [02 - Normalisation Strategy](./02-normalisation-strategy.md) - Why and how we normalise variant implementations
- [03 - Naming Conventions](./03-naming-conventions.md) - Crystal-clear boolean naming patterns

### Approach
- [04 - Test-First Methodology](./04-test-first-approach.md) - **Write tests BEFORE refactoring** (automated tests are priority)
- [05 - Feature Flag Strategy](./05-feature-flag-strategy.md) - Safe rollout with feature flags

### Implementation Phases
- [06 - Phase 0: Type Audit](./06-phase-0-type-audit.md) (1-1.5 hours) - Do this first: Fix implicit `any` types & validate against official specs
- [07 - Phase 1: Feature Flag Setup](./07-phase-1-feature-flag.md) (1 hour)
- [08 - Phase 2: Split MainViewer Components](./08-phase-2-split-components.md) (3-4 hours) - Split before context refactoring
- [09 - Phase 3: Canvas Data](./09-phase-3-canvas-data.md) (6-7 hours) - **Includes comprehensive automated tests**
- [10 - Phase 4: Download Logic](./10-phase-4-download-logic.md) (2 hours)
- [11 - Phase 5: Restriction Status](./11-phase-5-restriction-status.md) (1 hour)
- [12 - Phase 6: Duplicate Index Calls](./12-phase-6-duplicate-calls.md) (30 mins)
- [13 - Phase 7: Cleanup](./13-phase-7-cleanup.md) (1-2 hours)

### Reference
- [13 - Migration Checklist](./13-migration-checklist.md) - Step-by-step checklist for each phase
- [14 - Testing Strategy](./14-testing-strategy.md) - **Automated tests (priority) + manual testing checklist**
- [15 - Risks & Success Metrics](./15-risks-and-success.md) - Risk mitigation and success criteria
- [16 - Future Improvements](./16-future-improvements.md) - Post-refactor architectural improvements
- [Testing Guide](./refactoring-iiif-viewer-context-testing.md) - Detailed test examples with TypeScript types

## Quick Navigation

### I want to understand the refactoring
Start with [01-overview.md](./01-overview.md)

### I want to implement Phase 3
Read [09-phase-3-canvas-data.md](./09-phase-3-canvas-data.md) and [Testing Guide](./refactoring-iiif-viewer-context-testing.md)

### I want to see test examples
Go to [Testing Guide](./refactoring-iiif-viewer-context-testing.md) for complete TypeScript test examples

### I want the testing checklist
See [14-testing-strategy.md](./14-testing-strategy.md) for automated test requirements and manual testing checklist

## Key Principles

1. **Fix types first** - Audit and fix all types before refactoring (Phase 0)
2. **Automated tests BEFORE refactoring** - Build comprehensive test coverage first
3. **Feature flag everything** - Safe rollout with instant rollback capability
4. **Crystal-clear naming** - Use `is...`, `has...`, `can...`, `should...` patterns for booleans
5. **Test-first workflow** - Green to Green refactoring (tests pass before and after)
6. **Manual tests as backup** - Comprehensive checklist for extra confidence
7. **Context for shared state only** - Only add to context if used by 2+ components or likely to be needed soon
8. **Hooks for complex logic** - Extract to custom hooks for testability, even if only used once
9. **Split components with drastically different modes** - See [Future Improvements](./16-future-improvements.md) for details

## Progress Tracking

Tickets are in [wellcomecollection.org](https://github.com/wellcomecollection/wellcomecollection.org).

- [x] Phase 0: Type Audit - [#12982](https://github.com/wellcomecollection/wellcomecollection.org/issues/12982)
- [x] Phase 1: Feature Flag Setup - [#12983](https://github.com/wellcomecollection/wellcomecollection.org/issues/12983)
- [x] Phase 2: Split MainViewer Components - [#12985](https://github.com/wellcomecollection/wellcomecollection.org/issues/12985)
- [x] Phase 3: Canvas Data (with automated tests) - [#12986](https://github.com/wellcomecollection/wellcomecollection.org/issues/12986)
- [x] Phase 4: Download Logic - [#12987](https://github.com/wellcomecollection/wellcomecollection.org/issues/12987)
- [x] Phase 5: Restriction Status - [#13412](https://github.com/wellcomecollection/wellcomecollection.org/pull/13412)
- [x] Phase 6: Duplicate Calls - [#12989](https://github.com/wellcomecollection/wellcomecollection.org/issues/12989)
- [ ] Phase 7: Cleanup - [#12990](https://github.com/wellcomecollection/wellcomecollection.org/issues/12990), waiting on the toggle being defaulted to ON

Two tickets sit outside the phase structure: [#12984](https://github.com/wellcomecollection/wellcomecollection.org/issues/12984) (review and add tests) ran alongside Phases 0-2, and [#13329](https://github.com/wellcomecollection/wellcomecollection.org/issues/13329) (readability/normalisation pass) alongside Phase 3. Out-of-scope findings picked up along the way are collected in [#13273](https://github.com/wellcomecollection/wellcomecollection.org/issues/13273), which includes items to clear before the toggle can go on publicly.

---

**Related Documentation:**
- [AGENTS.md](../../AGENTS.md) - Development guidelines (British English, coding standards)
- [.github/copilot-instructions.md](../../.github/copilot-instructions.md) - PR review guidelines
