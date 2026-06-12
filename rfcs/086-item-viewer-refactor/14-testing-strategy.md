# Testing Strategy

[← Back to Index](./README.md)

**Priority:** Automated tests FIRST, manual testing as supplementary safety net.

## Philosophy: Automated Tests Are Primary

**Before writing ANY refactoring code:**
1. Write comprehensive automated tests for current behaviour
2. Verify tests pass (establish baseline)
3. Make refactoring changes
4. Tests still pass (green to green refactoring)
5. (Optional) Run manual testing checklist for extra confidence

**Why automated tests first?**
- Immediate feedback on every change
- No manual clicking through scenarios
- Runs in CI/CD on every commit
- Documents expected behaviour
- Prevents regressions permanently

## Required Automated Test Coverage

### Before Starting Any Phase

You MUST have automated tests covering:

#### Context Unit Tests
**File:** `content/webapp/contexts/ItemViewerContextV2/ItemViewerContextV2.test.tsx`

Test ALL derived values:
- [ ] `currentCanvasIndex` - calculated from `query.canvas` parameter
- [ ] `currentCanvas` - extracted from `transformedManifest.canvases`
- [ ] `mainImageService` - extracted from canvas with fallback handling
- [ ] `hasMultipleCanvases` - true when >1 canvas
- [ ] `isCurrentCanvasRestricted` - uses `hasRestrictedItem()` helper (from `restricted-images` merge)
- [ ] `isFirstCanvas` - true when `currentCanvasIndex === 0`
- [ ] `isLastCanvas` - true when at last canvas
- [ ] `canNavigateNext` - `!isLastCanvas && hasMultipleCanvases`
- [ ] `canNavigatePrevious` - `!isFirstCanvas && hasMultipleCanvases`
- [ ] `hasIiifImageService` - checks for `imageServiceId`
- [ ] `isImageZoomable` - checks if zoom is supported
- [ ] `isWorkBornDigital` - checks `work.production` type
- [ ] `currentProbeServiceId` - extracted from canvas (optional, if added to context)

Test all edge cases:
- [ ] Undefined `transformedManifest`
- [ ] Empty canvases array
- [ ] Canvas without `imageServiceId`
- [ ] Canvas without `probeServiceId` (non-restricted)
- [ ] Canvas with `probeServiceId` (restricted)
- [ ] Invalid canvas index (too high)
- [ ] Null/undefined values

**New (from `restricted-images` merge):**
- [ ] `isCurrentCanvasRestricted` returns true for restricted canvas
- [ ] `isCurrentCanvasRestricted` returns false for non-restricted canvas
- [ ] `currentProbeServiceId` extracted correctly when present
- [ ] `currentProbeServiceId` is undefined when absent

#### Component Integration Tests
**Files:** Component `.refactored.test.tsx` files

Test that components actually consume context values:
- [ ] **`IIIFViewer.refactored.test.tsx`**
  - [ ] Provides `currentCanvas` to children
  - [  ] Provides navigation booleans to children
  - [ ] Provides boolean flags for conditional rendering
  
- [ ] **`ViewerTopBar.refactored.test.tsx`**
  - [ ] Uses `currentCanvas` from context (not calculating)
  - [ ] Uses navigation booleans for button states
  - [ ] Uses `isCurrentCanvasRestricted` for restriction badge
  - [ ] Uses `hasDownloadOptions` for download button
  
- [ ] **`ZoomedImage.refactored.test.tsx`**
  - [ ] Uses `currentCanvas` from context
  - [ ] Uses `mainImageService` from context
  - [ ] Handles empty `mainImageService` correctly

#### Download Options Hook Tests (Phase 2)
**File:** `content/webapp/hooks/useDownloadOptions.test.ts`

Test download option calculations:
- [ ] Returns empty array when no canvas or manifest
- [ ] Includes IIIF image download options
- [ ] Includes canvas image downloads from services
- [ ] Includes canvas rendering downloads (PDFs)
- [ ] Includes manifest-level downloads
- [ ] Includes video/audio downloads
- [ ] Handles ChoiceBody items correctly
- [ ] **Deduplicates downloads with same id** (from `restricted-images` merge)
- [ ] Memoises results correctly
- [ ] Updates when dependencies change

Test edge cases:
- [ ] Multiple downloads with different URLs (all included)
- [ ] Multiple downloads with same URL (only one included after dedup)
- [ ] ChoiceBody in `rendering` array
- [ ] ChoiceBody in `supplementing` array
- [ ] Empty download arrays
- [ ] Restricted downloads for staff vs non-staff users

#### Mock Utilities
**File:** `content/webapp/contexts/ItemViewerContextV2/test-utils.ts`

- [ ] `mockDefaultContext` with proper TypeScript types
- [ ] Helper functions for creating test manifests
- [ ] Helper functions for creating test canvases
- [ ] All mocks properly typed (no `any`)

### Test Examples

See [refactoring-iiif-viewer-context-testing.md](./refactoring-iiif-viewer-context-testing.md) for complete TypeScript test examples.

Quick example:

```typescript
describe('ItemViewerContextV2 - Derived Canvas Data', () => {
  it('should calculate currentCanvasIndex from canvas query param', () => {
    const contextValue: ItemViewerContextV2Props = {
      ...mockDefaultContext,
      query: { canvas: 3, manifest: 1, page: 1, shouldScrollToCanvas: true, query: '' },
      currentCanvasIndex: 2, // canvas=3 to index 2 (1-indexed to 0-indexed)
    };

    render(
      <ItemViewerContextV2.Provider value={contextValue}>
        <ContextValueDisplay />
      </ItemViewerContextV2.Provider>
    );

    expect(screen.getByTestId('currentCanvasIndex')).toHaveTextContent('2');
  });
});
```

## Manual Testing Checklist

**Use this AFTER automated tests pass as an extra safety net.**

### For Each Phase: Core Functionality

- [ ] **Navigate between canvases**
  - [ ] Thumbnails navigation works
  - [ ] Next/Previous buttons work
  - [ ] URL updates with canvas number
  - [ ] Page title updates
  
- [ ] **UI controls**
  - [ ] Sidebar toggle (desktop)
  - [ ] Sidebar toggle (mobile)
  - [ ] Grid view toggle (multi-canvas works only)
  - [ ] Zoom in/out controls
  - [ ] Fullscreen mode
  
- [ ] **Visual appearance**
  - [ ] Layout looks correct
  - [ ] Images load correctly
  - [ ] No console errors
  - [ ] No React warnings

### Different Work Types

Test with these specific work types:

- [ ] **Multi-canvas image work** (`/works/[id]/images`)
  - [ ] Canvas count shows correctly
  - [ ] Grid view available
  - [ ] Navigation between canvases works
  - [ ] Download options appear
  
- [ ] **Single canvas work**
  - [ ] No grid view toggle (should be hidden)
  - [ ] Navigation buttons hidden/disabled
  - [ ] Layout optimised for single canvas
  
- [ ] **Archive items** (`/works/[id]/items`)
  - [ ] Archive tree navigation works
  - [ ] Correct canvas loads from tree selection
  - [ ] Breadcrumb navigation works
  
- [ ] **Restricted access works**
  - [ ] Restriction badge appears
  - [ ] Auth flow works correctly
  - [ ] Restricted content shows after auth
  - [ ] Download disabled for restricted canvas
  
- [ ] **Works with video/audio**
  - [ ] Video player appears in viewer
  - [ ] Audio player appears in viewer
  - [ ] Download options include video/audio
  
- [ ] **Works with downloadable PDFs**
  - [ ] PDF renders in viewer
  - [ ] PDF download option appears
  - [ ] PDF downloads correctly

### User Scenarios Matrix

The table below lists key combinations of work types, authentication states, and access restrictions. Test coverage should span these scenarios to ensure the viewer handles all cases correctly.

**Authentication States:**
- **Logged out** - no authentication
- **Logged in (regular user)** - standard library member  
- **Logged in (restricted access)** - user with restricted content access (same UI, different access level)

**Access Types:**
- ✓ Open access - no restrictions
- 🔒 Restricted - requires authentication with restricted access role
- ⚠️ Content advisory - requires clicking through warning modal (any auth state)

| Work Type | Logged Out | Logged In (Regular) | Logged In (Restricted) | Example Work ID | Notes |
|-----------|-----------|---------------------|------------------------|-----------------|-------|
| **Multi-canvas images** | ✓ Open | ✓ Open | ✓ Open | `a55dcp3h` | Grid view, navigation |
| **Single canvas image** | ✓ Open | ✓ Open | ✓ Open | `b5kqccbb` | No grid/nav controls |
| **Archive items** | ✓ Open | ✓ Open | ✓ Open | `a222zvge` | Tree navigation |
| **Video/audio** | ✓ Open | ✓ Open | ✓ Open | `a9w3qy3j` | In-viewer playback |
| **PDF** | ✓ Open | ✓ Open | ✓ Open | `ndx5vuhy` | In-viewer rendering |
| **Mixed content (born digital)** | ✓ Open | ✓ Open | ✓ Open | `dn9jwck6` | Multiple media types |
| **Content advisory** | ⚠️ Modal | ⚠️ Modal | ⚠️ Modal | `pnud3fzb` | Warning modal required |
| **Restricted whole item** | 🔒 Blocked | 🔒 Blocked | ✓ Access granted | `rp9jnamu` | Auth + role required |
| **Restricted audio** | 🔒 Blocked | 🔒 Blocked | ✓ Access granted | `esd6gs3s` | Auth + role required |
| **Restricted video** | 🔒 Blocked | 🔒 Blocked | ✓ Access granted | `zsgh5y3z` | Auth + role required |
| **Restricted born digital** | 🔒 Blocked | 🔒 Blocked | ✓ Access granted | `my6bzerr` | Auth + role required |

**Note:** The "logged in (restricted)" authentication state only affects **access** (whether content is granted), not **which component renders** — the viewer always renders regardless of auth state.

### Specific Test Works

The following works provide comprehensive coverage for all scenarios from the matrix above.

#### Unrestricted Works (Open Access)

##### Multi-Canvas Image Work
- **Type:** Multi-canvas images (unrestricted)
- **What to test:** Grid view, canvas navigation, thumbnails, all accessible to everyone
- Work page: [prod](https://wellcomecollection.org/works/a55dcp3h) | [dev](https://www-dev.wellcomecollection.org/works/a55dcp3h)
- Items page: [prod](https://wellcomecollection.org/works/a55dcp3h/items) | [dev](https://www-dev.wellcomecollection.org/works/a55dcp3h/items)

**Test with:** Logged out | Logged in (regular) | Logged in (restricted)

##### Single Canvas Image Work
- **Type:** Single canvas image (unrestricted)
- **What to test:** No grid/nav controls, single image display, all accessible to everyone
- Work page: [prod](https://wellcomecollection.org/works/b5kqccbb) | [dev](https://www-dev.wellcomecollection.org/works/b5kqccbb)
- Images page: [prod](https://wellcomecollection.org/works/b5kqccbb/images?id=a22tjkrd&resultPosition=2) | [dev](https://www-dev.wellcomecollection.org/works/b5kqccbb/images?id=a22tjkrd&resultPosition=2)

**Test with:** Logged out | Logged in (regular) | Logged in (restricted)

##### Archive Items
- **Type:** Archive with tree navigation (unrestricted)
- **What to test:** Archive tree, breadcrumbs, canvas selection from tree, all accessible to everyone
- Work page: [prod](https://wellcomecollection.org/works/a222zvge) | [dev](https://www-dev.wellcomecollection.org/works/a222zvge)

**Test with:** Logged out | Logged in (regular) | Logged in (restricted)

##### PDF Work
- **Type:** PDF document (unrestricted)
- **What to test:** PDF rendering in viewer, download options, all accessible to everyone
- Work page: [prod](https://wellcomecollection.org/works/ndx5vuhy) | [dev](https://www-dev.wellcomecollection.org/works/ndx5vuhy)
- Items page: [prod](https://wellcomecollection.org/works/ndx5vuhy/items?shouldScrollToCanvas=true) | [dev](https://www-dev.wellcomecollection.org/works/ndx5vuhy/items?shouldScrollToCanvas=true)

**Test with:** Logged out | Logged in (regular) | Logged in (restricted)

##### Mixed Media (Born Digital)
- **Type:** Mixed content with multiple media types (unrestricted)
- **What to test:** Multiple media types in same viewer, navigation between media, all accessible to everyone
- Work page: [prod](https://wellcomecollection.org/works/dn9jwck6) | [dev](https://www-dev.wellcomecollection.org/works/dn9jwck6)
- Items page: [prod](https://wellcomecollection.org/works/dn9jwck6/items?canvas=20) | [dev](https://www-dev.wellcomecollection.org/works/dn9jwck6/items?canvas=20)

**Test with:** Logged out | Logged in (regular) | Logged in (restricted)

##### Regular Video (Unrestricted)
- **Type:** Open access video
- **What to test:** Video player accessible to all users
- Work page: [prod](https://wellcomecollection.org/works/a9w3qy3j) | [dev](https://www-dev.wellcomecollection.org/works/a9w3qy3j)
- Items page: [prod](https://wellcomecollection.org/works/a9w3qy3j/items) | [dev](https://www-dev.wellcomecollection.org/works/a9w3qy3j/items)

**Test with:** Logged out | Logged in (regular) | Logged in (restricted)

#### Restricted/Special Access Works

##### Content Advisory (Clickthrough Warning Modal)
- **Type:** Restricted/Clickthrough Mix  
- **What to test:** Modal warning appears for all users before accessing items
- Work page: [prod](https://wellcomecollection.org/works/pnud3fzb) | [dev](https://www-dev.wellcomecollection.org/works/pnud3fzb)
- Items page: [prod](https://wellcomecollection.org/works/pnud3fzb/items) | [dev](https://www-dev.wellcomecollection.org/works/pnud3fzb/items)

**Test with:** Logged out | Logged in (regular) | Logged in (restricted)

##### Restricted Whole Item
- **Type:** Fully restricted content
- **What to test:** Blocked for logged out + regular users; accessible for restricted role
- Work page: [prod](https://wellcomecollection.org/works/rp9jnamu) | [dev](https://www-dev.wellcomecollection.org/works/rp9jnamu)
- Items page: [prod](https://wellcomecollection.org/works/rp9jnamu/items) | [dev](https://www-dev.wellcomecollection.org/works/rp9jnamu/items)

**Test with:** Logged out | Logged in (regular) | Logged in (restricted)

##### Restricted Audio
- **Type:** Restricted audio content
- **What to test:** Audio player only appears for restricted role users
- Work page: [prod](https://wellcomecollection.org/works/esd6gs3s) | [dev](https://www-dev.wellcomecollection.org/works/esd6gs3s)
- Items page: [prod](https://wellcomecollection.org/works/esd6gs3s/items) | [dev](https://www-dev.wellcomecollection.org/works/esd6gs3s/items)

**Test with:** Logged out | Logged in (regular) | Logged in (restricted)

##### Restricted Video
- **Type:** Restricted video content
- **What to test:** Video player only appears for restricted role users
- Work page: [prod](https://wellcomecollection.org/works/zsgh5y3z) | [dev](https://www-dev.wellcomecollection.org/works/zsgh5y3z)
- Items page: [prod](https://wellcomecollection.org/works/zsgh5y3z/items) | [dev](https://www-dev.wellcomecollection.org/works/zsgh5y3z/items)

**Test with:** Logged out | Logged in (regular) | Logged in (restricted)

##### Restricted Born Digital
- **Type:** Restricted born digital/mixed content
- **What to test:** Mixed media (PDF/video/audio) only accessible for restricted role
- Work page: [prod](https://wellcomecollection.org/works/my6bzerr) | [dev](https://www-dev.wellcomecollection.org/works/my6bzerr)
- Items page: [prod](https://wellcomecollection.org/works/my6bzerr/items) | [dev](https://www-dev.wellcomecollection.org/works/my6bzerr/items)

**Test with:** Logged out | Logged in (regular) | Logged in (restricted)

### Edge Cases

- [ ] **Works with no manifest**
  - [ ] Error message displays gracefully
  - [ ] No JavaScript errors
  
- [ ] **Works with JavaScript disabled (progressive enhancement)**
  - [ ] NoScriptImage component renders on server
  - [ ] Image is visible without JavaScript enabled
  - [ ] OCR text is accessible (check view source)
  - [ ] Page doesn't appear broken
  
- [ ] **Works with empty canvases**
  - [ ] Handles gracefully
  - [ ] No infinite loops or crashes
  
- [ ] **Missing image services**
  - [ ] Falls back to alternative rendering
  - [ ] No broken images
  
- [ ] **Invalid canvas numbers**
  - [ ] `/works/[id]/items?canvas=999` redirects or shows error
  - [ ] No crashes
  
- [ ] **Canvas without imageServiceId**
  - [ ] Still renders (uses alternative)
  - [ ] Zoom controls hidden
  - [ ] No console errors

### Normalisation-Specific Tests

These are critical when normalising variant implementations:

#### Test `currentCanvas` Normalisation

Different components previously calculated `currentCanvas` differently. Verify they all work:

| Component | Previous Implementation | What to Test |
|-----------|------------------------|--------------|
| `ViewerTopBar` | `canvases?.[index]` | Download options appear, canvas title shows |
| `ZoomedImage` | `transformedManifest?.canvases[index]` | Zoom shows correct canvas image |
| `MainViewer` | May calculate independently | Canvas scrolling works, canvas displays correctly |
| `Thumbnails` | Used `queryParamToArrayIndex` directly | Correct thumbnail highlighted |

**Key question:** Verify the `|| ''` fallback only exists where genuinely needed.

| Component | Previous Implementation | What to Test |
|-----------|------------------------|--------------|
| `IIIFViewer` | No `\|\| ''` fallback | `iiifImageTemplate` handles undefined correctly |
| `ZoomedImage` | Had `\|\| ''` fallback | Verify `convertRequestUriToInfoUri` still works |

**Test both:**
1. Canvas WITH `imageServiceId` - zoom should work
2. Canvas WITHOUT `imageServiceId` - should fall back gracefully, no errors

**Critical:** Test on all supported browsers BEFORE releasing.

- [ ] **Chrome/Edge** (latest)
  - [ ] All core functionality
  - [ ] Zoom controls
  - [ ] Fullscreen
  - [ ] Downloads
  
- [ ] **Firefox** (latest)
  - [ ] All core functionality
  - [ ] Check for Firefox-specific quirks
  
- [ ] **Safari** (latest macOS)
  - [ ] All core functionality
  - [ ] Image rendering
  - [ ] Fullscreen API differences
  
- [ ] **Mobile Safari** (iOS)
  - [ ] Sidebar toggle works
  - [ ] Touch navigation
  - [ ] Pinch to zoom
  - [ ] Fullscreen on mobile
  
- [ ] **Mobile Chrome** (Android)
  - [ ] Sidebar toggle works
  - [ ] Touch navigation
  - [ ] Downloads work

### Performance Testing

- [ ] **Large manifests** (100+ canvases)
  - [ ] Page loads within 3 seconds
  - [ ] No lag when navigating
  - [ ] Thumbnails load smoothly
  
- [ ] **React DevTools Profiler**
  - [ ] Check for unnecessary re-renders
  - [ ] Verify memoization works
  - [ ] Compare before/after performance

### Comparison Testing (Legacy vs Refactored)

**Most important test:** Side-by-side comparison.

For each work type listed above:
1. Test with `iiifViewerRefactored` flag OFF (legacy)
2. Note behaviour, take screenshots
3. Test with `iiifViewerRefactored` flag ON (refactored)
4. Verify IDENTICAL behaviour and appearance
5. Document any differences (should be zero)

## Test Work IDs

See the **User Scenarios Matrix** and **Specific Test Works** sections above for a comprehensive list of test works covering all combinations of work types, authentication states, and access restrictions.

All test scenarios now have example work IDs:
- ✅ Multi-canvas images: `a55dcp3h`
- ✅ Single canvas: `b5kqccbb`
- ✅ Archive items: `a222zvge`
- ✅ PDF: `ndx5vuhy`
- ✅ Mixed media (born digital): `dn9jwck6`
- ✅ Video/audio: `a9w3qy3j`
- ✅ Content advisory: `pnud3fzb`
- ✅ Restricted works: `rp9jnamu`, `esd6gs3s`, `zsgh5y3z`, `my6bzerr`

## When Manual Testing Finds Issues

If manual testing reveals a bug that automated tests didn't catch:

1. **Write an automated test for the bug FIRST**
2. Verify the test fails (reproduces the bug)
3. Fix the bug
4. Verify the test passes
5. Add test to permanent test suite

This prevents the bug from reoccurring and improves test coverage.

## Success Criteria

Before marking a phase complete:

**Required:**
- [ ] All automated tests pass with flag OFF (legacy)
- [ ] All automated tests pass with flag ON (refactored)
- [ ] TypeScript compiles with no errors
- [ ] No console warnings or errors
- [ ] Test coverage >80% for new code

**Highly Recommended:**
- [ ] Manual testing checklist completed
- [ ] Tested on all browsers
- [ ] Comparison testing shows identical behaviour
- [ ] Performance profiling shows no regressions

---

**See also:**
- [refactoring-iiif-viewer-context-testing.md](./refactoring-iiif-viewer-context-testing.md) - Complete TypeScript test examples
- [04-test-first-approach.md](./04-test-first-approach.md) - Why we test first
- [13-migration-checklist.md](./13-migration-checklist.md) - Per-phase checklists

---

**Next:** [Risks & Success Metrics](./15-risks-and-success.md)
