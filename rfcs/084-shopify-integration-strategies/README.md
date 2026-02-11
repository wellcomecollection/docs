# Shopify Integration Approaches for Wellcome Collection

**Research Focus:** Evaluating different approaches for integrating Shopify with wellcomecollection.org

## Summary

This research outlines five approaches for integrating Shopify with the Wellcome Collection website, ranging from simple embedded solutions to fully headless implementations. Based on the existing Next.js architecture, the recommended approach is **Option 3: Headless Commerce with Shopify Storefront API**, which provides a balance of brand consistency, technical flexibility, and maintainability.

## Current Technical Context

The Wellcome Collection website is built as a Next.js monorepo with:
- React-based frontend (Next.js 19+)
- Styled-components for styling
- Prismic CMS for content management
- Yarn workspaces architecture
- Strong emphasis on performance optimisation and accessibility

## Integration Approaches

### Option 1: Shopify Buy Button

**Description:** Embeds Shopify products directly into existing pages using JavaScript widgets.

**Implementation:**
- Add Shopify-generated code snippets to relevant pages
- Products display in pop-up or redirect to Shopify checkout
- Minimal development effort required

**Advantages:**
- Quick implementation (hours to days)
- Low cost
- No complex integration required
- Shopify handles all checkout and payment processing
- Suitable for testing e-commerce viability

**Disadvantages:**
- Limited design customisation
- Checkout redirects to Shopify domain breaking brand continuity
- Inconsistent user experience
- Limited control over customer journey
- Not suitable for substantial product catalogues

**Best For:** Testing e-commerce concept, limited product offerings, content-heavy sites with occasional sales

**Sources:**
- [Shopify Buy Button](https://www.shopify.com/buy-button)
- [Buy Button FAQ](https://help.shopify.com/en/manual/online-sales-channels/buy-button/faq)
---

### Option 2: Embedded Shopify Storefront

**Description:** Creates a separate Shopify store accessible via subdomain or integrated section whilst maintaining primary site navigation.

**Implementation:**
- Standard Shopify theme on `shop.wellcomecollection.org` or `/shop` path
- Create custom Liquid theme to match brand
- Link from main site to shop

**Advantages:**
- Full Shopify feature set available
- Extensive app ecosystem
- Proven reliability for e-commerce operations
- Professional checkout experience
- Comprehensive analytics and reporting

**Disadvantages:**
- Inconsistent user experience between main site and shop
- Duplicate navigation/header/footer maintenance
- Users perceive being taken away from main site
- SEO considerations for separate domain/path
- Theme customisation limited by Liquid templating

**Best For:** Organisations prioritising speed to market, those without significant development resources, when complete feature parity with Shopify ecosystem is required

---

### Option 3: Headless Commerce with Shopify Storefront API

**Description:** Uses Shopify as backend commerce engine whilst building custom frontend using Storefront API (GraphQL).

**Implementation:**
- Shopify manages products, inventory, orders, customers
- Custom React components in Next.js fetch data via the Storefront API
- Checkout can be embedded or redirect to Shopify
- Full control over frontend presentation

**Technical Architecture:**
```
Next.js Frontend (wellcomecollection.org)
         ↓
   Storefront API (GraphQL)
         ↓
Shopify Backend (products, orders, inventory)
         ↓
   Shopify Checkout
```

**Key Implementation Details:**
- GraphQL API with no request-count rate limits
- Versioned API updated quarterly
- Public and private access tokens via Headless channel

**Advantages:**
- Complete design control and brand consistency
- Seamless user experience within existing site
- Leverage existing Next.js expertise
- Optimised performance (fetch only required data)
- Scalable architecture
- Aligns with existing strategies (composable, API-first)
- Lends itself to iteration

**Disadvantages:**
- Higher development cost
- Requires Next.js knowledge
- Ongoing maintenance responsibility
- Checkout still redirects to Shopify domain
- More complex than out-of-box solutions

**Development Approach:**
1. Set up Shopify Headless channel and generate API tokens
2. Configure environment variables in Next.js
3. Create GraphQL queries for products, collections, cart
4. Build React components for product display, cart, checkout(?) flow
5. Implement state management for cart functionality
6. Integrate with existing design system/component library
7. Add analytics and tracking

**Best For:** Organisations with development resources, those requiring brand consistency, sites with existing sophisticated frontend, when user experience is paramount

**Sources:**
- [Shopify Headless Commerce](https://www.shopify.com/plus/solutions/headless-commerce)
- [Building with the Storefront API](https://shopify.dev/docs/storefronts/headless/building-with-the-storefront-api)
- [Storefront API Reference](https://shopify.dev/docs/api/storefront/latest)
- [Building Ecommerce Sites with Next.js and Shopify](https://vercel.com/kb/guide/building-ecommerce-sites-with-next-js-and-shopify)
- [Good and Bad of Headless Commerce with Shopify](https://www.plytix.com/blog/headless-commerce-with-shopify)
- [Headless Commerce vs Traditional Commerce](https://www.shopify.com/enterprise/blog/headless-commerce-vs-traditional-commerce)
---

### Option 4: Hydrogen Framework (Shopify's React/Remix Framework)

**Description:** Shopify's official React-based framework specifically built for headless commerce.

**Implementation:**
- Use Hydrogen as frontend framework instead of custom Next.js integration
- Pre-built commerce components and hooks
- Oxygen hosting for global deployment (free with Shopify)
- Optimised for Shopify's commerce patterns

**Advantages:**
- Accelerated development with pre-built components
- Built-in Shopify integrations and best practices
- Optimised for performance at global scale
- Regular updates from Shopify
- Shopify-specific tooling and conventions
- Free global hosting with Oxygen

**Disadvantages:**
- Introduces different framework from existing Next.js
- Would require site migration or dual-framework approach
- Less flexibility for non-commerce features
- Smaller community compared to Next.js
- Oxygen deployment limitations (one storefront per store, limited logging)
- Learning curve for team familiar with Next.js
- Not suitable if requiring extensive customisation beyond e-commerce

**Best For:** New projects, shops with minimal non-commerce content, teams starting fresh without existing frontend constraints

**Sources:**
- [Hydrogen: Shopify's headless commerce framework](https://hydrogen.shopify.dev/)
- [Shopify Headless Commerce: A Complete Guide](https://litextension.com/blog/shopify-headless/)

---

### Option 5: Shopify Plus with Custom Checkout Extensibility

**Description:** Shopify Plus plan with extensive checkout customisation using Checkout UI Extensions.

**Implementation:**
- Shopify Plus subscription (£££)
- Custom checkout steps using UI Extensions API
- Full Shopify feature set with enhanced customisation
- Can maintain brand experience through checkout

**Technical Details:**
- Checkout UI Extensions
- Custom functionality for product offers, fields, loyalty programmes
- Extensions available for information, shipping, payment, order summary steps

**Advantages:**
- Branded checkout experience on Shopify domain
- Access to Plus-only features (scripts, automation, wholesale)
- Dedicated support
- Can customise checkout with UI extensions

**Disadvantages:**
- Significant ongoing cost
- May be over-specification for smaller operations

**Best For:** Large-scale operations, high-volume sales, organisations requiring extensive Shopify app ecosystem, wholesale capabilities

**Sources:**
- [Checkout UI Extensions](https://shopify.dev/docs/api/checkout-ui-extensions/latest)
---

## Key Decision Criteria

### Technical Considerations

**Existing Architecture:**
- Current Next.js implementation favours headless approach
- Styled-components design system can extend to commerce components
- TypeScript throughout supports type-safe API integration

### User Experience Priorities

**Brand Consistency:**
- Requires cohesive UX/UI
- Headless approaches provide seamless integration
- Checkout on Shopify domain is probably acceptable – it is a familiar/trustworthy user flow. Fully customising checkout ourselves (including managing credit card information, shipping, and taxes etc.) feels like it would probably be building in a wealth of future pain

**Customer Journey:**
- Content-to-commerce flow should be natural
- Integration with existing site navigation and search


### Implementation Roadmap

#### Phase 1: Foundation 
- Set up Shopify backend
- Configure Headless channel and API access
- Create product catalogue structure
- Design commerce component architecture

#### Phase 2: Core Features
- Product listing pages
- Product detail pages
- Shopping cart functionality
- Checkout flow (redirect to Shopify)
- Basic search and filtering

#### Phase 3: Enhanced Experience
- Content-product associations in Prismic
- Advanced search and recommendations
- Analytics integration

#### Phase 4: Optimisation
- Performance tuning
- A/B testing
- User feedback incorporation
- Additional features based on usage patterns


## Technical Implementation Notes

It isn’t obvious how to redirect back to wc.org after checkout clicking the ‘Continue shopping’ page, with several unanswered questions from community boards [1](https://community.shopify.com/t/change-continue-shopping-url-on-thank-you-page-headless/403380), [2](https://community.shopify.com/t/change-continue-shopping-url-on-thank-you-page-headless/403380), [3](https://community.shopify.dev/t/headless-shopify-continue-shopping-button-redirects-to-wrong-domain-after-checkout/18950), [4](https://community.shopify.com/t/headless-redirect-after-checkout/397344/3), [5](https://www.reddit.com/r/shopify/comments/1iz2fa0/headless_redirect_after_checkout/), but I made a minimal Liquid theme that just redirects client-side and this seems to work fine.

I haven’t looked much into [integration with existing Prismic content](https://prismic.io/docs/fields/integration#sync-products-from-a-shopify-store) beyond knowing that it exists.

I think/presume additional cookies should be added to the functional/required list in order for cart/checkout functionality to work.

I haven't looked at any Shopify-specific analytics/tracking options.

## Proof of Concept
The [shopify branch](https://github.com/wellcomecollection/wellcomecollection.org/compare/shopify) of the wc.org monorepo contains a minimal proof of concept implementation of Option 3 (Headless Commerce with Storefront API). It demonstrates fetching products and variants from Shopify and displaying them on a Next.js page, with a cart and checkout flow.

<video src="https://private-user-images.githubusercontent.com/1394592/548163612-7e59faa1-d1eb-44f6-8254-25958e22e7a6.mov?jwt=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3NzA4MDYwNjksIm5iZiI6MTc3MDgwNTc2OSwicGF0aCI6Ii8xMzk0NTkyLzU0ODE2MzYxMi03ZTU5ZmFhMS1kMWViLTQ0ZjYtODI1NC0yNTk1OGUyMmU3YTYubW92P1gtQW16LUFsZ29yaXRobT1BV1M0LUhNQUMtU0hBMjU2JlgtQW16LUNyZWRlbnRpYWw9QUtJQVZDT0RZTFNBNTNQUUs0WkElMkYyMDI2MDIxMSUyRnVzLWVhc3QtMSUyRnMzJTJGYXdzNF9yZXF1ZXN0JlgtQW16LURhdGU9MjAyNjAyMTFUMTAyOTI5WiZYLUFtei1FeHBpcmVzPTMwMCZYLUFtei1TaWduYXR1cmU9OWRiM2ZjNTJkMTI3MjlmYjg3OTlmZGMwZWU0MzZkYjE5YzM5ODkwYWRjZTlhYjA1ZGU2NTNjOGY0MzI3ZDE4MyZYLUFtei1TaWduZWRIZWFkZXJzPWhvc3QifQ.DVPpHFjkORy2nRbkSbpKRw_IMQB3ZuEPl_X2RQko-OA" data-canonical-src="https://private-user-images.githubusercontent.com/1394592/548163612-7e59faa1-d1eb-44f6-8254-25958e22e7a6.mov?jwt=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3NzA4MDYwNjksIm5iZiI6MTc3MDgwNTc2OSwicGF0aCI6Ii8xMzk0NTkyLzU0ODE2MzYxMi03ZTU5ZmFhMS1kMWViLTQ0ZjYtODI1NC0yNTk1OGUyMmU3YTYubW92P1gtQW16LUFsZ29yaXRobT1BV1M0LUhNQUMtU0hBMjU2JlgtQW16LUNyZWRlbnRpYWw9QUtJQVZDT0RZTFNBNTNQUUs0WkElMkYyMDI2MDIxMSUyRnVzLWVhc3QtMSUyRnMzJTJGYXdzNF9yZXF1ZXN0JlgtQW16LURhdGU9MjAyNjAyMTFUMTAyOTI5WiZYLUFtei1FeHBpcmVzPTMwMCZYLUFtei1TaWduYXR1cmU9OWRiM2ZjNTJkMTI3MjlmYjg3OTlmZGMwZWU0MzZkYjE5YzM5ODkwYWRjZTlhYjA1ZGU2NTNjOGY0MzI3ZDE4MyZYLUFtei1TaWduZWRIZWFkZXJzPWhvc3QifQ.DVPpHFjkORy2nRbkSbpKRw_IMQB3ZuEPl_X2RQko-OA" controls="controls" muted="muted" class="d-block rounded-bottom-2 border-top width-fit" style="max-height:640px; min-height: 200px">
  </video>

**Sources:**
- [GraphQL Storefront API](https://shopify.dev/docs/api/storefront/latest)
- [GraphiQL explorer](https://shopify.dev/docs/api/usage/api-exploration/admin-graphiql-explorer)
- [Getting Started with GraphQL](https://www.shopify.com/partners/blog/getting-started-with-graphql)
- [Working with Shopify Storefront API](https://medium.com/@sandeeppangeni17/working-with-shopify-storefront-api-graphql-javascript-e02fb89eb682)
---
