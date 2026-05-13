# RFC 087: wellcomecollection.org in kiosk mode

We will be offering two experiences in the museum via iPads. We want to use the website for those as it means content stays up-to-date and our styles and components can be used, removing the need to build something new and having to maintain it. This iPad experience will display the website in what we'll call "Kiosk mode".

Lauren has created Notion pages with more information about these experiences, I won't re-explain them here, so have a read through. The links are underneath the relevant headings. I then only talk about technical work and requirements.

## Reading room stories
[Notion documentation](https://www.notion.so/wellcometrust/Digital-stories-in-the-Reading-Room-2646687658a1804384e9fbf5db6bdd86()

### Dev work considerations
- New Curated listing page (in Prismic and in code)
- Block access to page outside of Kiosk mode ("no index" meta tag and return a 404)
- The Stories' breadcrumbs should be different in Kiosk mode and link to the Curated listing page instead of the Stories listing page.
- HotJar survey to be added conditionally to Kiosk mode

## Exhibition-specific curated content
[Notion documentation: kick-off](https://www.notion.so/wellcometrust/T-R-in-exhibition-digital-engagement-kick-off-3576687658a1807b9fb2c88f221bb6be)
[Notion documentation](https://www.notion.so/wellcometrust/Digital-engagement-in-Tenderness-Rage-35e6687658a18097aa32dae82b7508f0)

### Dev work considerations
- Create new page in Prismic and in the code. Is it part of an "Exhibition hub"? For example, in Exhibition guides alongside BSL and Audio guides ([see here](https://wellcomecollection.org/guides/exhibitions/in-plain-sight))? 
- New pages are to be available to users outside of the museum/on their phones. In that case, it's not in Kiosk mode and looks like a real part of the website (footer, header, etc.).
- Breadcrumbs don't need to change for now (UX question to decide on later)
- Kiosk mode: Add content warning about how not all content is suitable for children (where?)

## Requirements for Kiosk mode

- "Reset to homepage" function after XX seconds of inactivity.
- Remove most of the footer, the newsletter sign-up, search and login functions. Potentially could keep a minimal header, TBC.
- External links removed
- Ability to identify iPad ID (e.g. "iPad1 - Reading Room") for analytics (this is TBC actually, Mankeet to confirm)
- QR codes to be made available on those pages
- Cookies to be accepted MANUALLY by VE.

## Toggles or URL param?

In the codebase, we need a way to recognise that the website is in Kiosk mode. That could be done a few different ways, but the need is to be able to:

1. Recognise that the pages should look and behave differently 
2. Make the device ID (e.g. "iPad1 - Reading Room") available in GA.
3. Remove the cookie banner and assign consent automatically
4. Add HotJar conditionally for Reading room

### Toggle
I originally considered a toggle as it's my reflex, but it might not fit perfectly here. It would work for anything that's conditional, but if we want to identify the device ID through the same means as changing the website behaviour, it doesn't allow for it. Toggle values are "true" and "false" only. So we'd have to find a different solution for that.

### URL params
We already use those for QR codes in Exhibitions, but they only serve to set a cookie for the user's guide preference (BSL vs Audio). 
The advantage is not having to interact with the Dashboard at all at set-up time and is therefore slightly easier to reset. But does it make it more fragile to start with? How much is the user able to play with the URL? Is it also more fragile throughout page navigation where we sometimes remove query params that aren't valid (e.g. search)? I'm worried it's a bit flimsy and requires more safeguarding at various point in the codebase. 

### Cookie that's not a classic toggle

I'm thinking we could perhaps use a new cookie type (still made available in Dash somehow) that is not a classic feature flag toggle, but a cookie that holds an object with values we want to use. For example:

`WC_kioskMode={"device":"RR-Ipad1"}`

That would allow us to add the device ID to the dataLayer / see if Mankeet can just fetch it from the cookies.

Could be a new section in Dash that uses a `select` type input?

This, I think, is useful over a classic Toggle only if we need extra data to exist in the value. If we don't care about tracking the iPad ID, maybe it's not that much more useful?

## Questions
- Are the staff likely to change the iPads around? because if we identify "iPad1 - Reading Room" as is, and then it dies and gets replaced, that data needs to be re-added somehow. (Lauren said this would only be done by AV and we could let them know about this requirement).