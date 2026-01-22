# RFC 082: Curated Collections x Prismic

_“Theme” and “Concept” used interchangeably in this document._

As we're increasingly connecting Collections to Content management (Prismic), we are having a lot of conversations that can tend to get muddled together. We thought it best to separate concerns. There are a few things to address, from selection process to actual solution implementation, and we wanted to start documenting them. 

I very much welcome all input, and we’ll eventually be clear on what issues need fixing and how they can best be addressed. 

- Lauren had [her own brain-dump here](https://wellcomecloud-my.sharepoint.com/:w:/r/personal/l_baily_wellcome_ac_uk/_layouts/15/Doc.aspx?sourcedoc=%7Bf4e37b91-233b-4df6-85b9-f8631b2e4c53%7D&action=edit&wdPid=14f53129) which is interesting context. 
- This document is created from [this file](https://wellcomecloud-my.sharepoint.com/:w:/r/personal/r_cantin_wellcome_ac_uk/Documents/Curated%20Catalogue%20results%20x%20Prismic.docx?d=w6485e321e91d4475905024dc89d391e3&csf=1&web=1&e=O70JWS) which we'll stop evolving and use this RFC instead.

With the work being done on thematic browsing, we are aware that we won't be able to curate ALL theme pages, but we still need to mitigate risk (e.g. offensive images, wrong description).
 
​​
**Here are the various issues we are aiming to solutionise:**
1. How to curate which images are shown on a theme card?
2. How to curate the teaser text of a theme card?
3. How to select curated works and concepts?
4. How and where to list selected works and concepts?
5. How to display said lists?
6. If the content is curated through a CMS, how do we re-use it across the site?
7. If the content is curated through a CMS, how do we ensure we don't create a ton of dead content?

**Questions to answer:**
1. Could we only use an approved list of themes?


## 1. How to curate which images are shown on a theme card?
### Why do we need to be able to do this?
We could find that the default images are not fitting for a Theme card. For example;
- If a person card, it's the wrong person or the work of said person.
- It's a sensitive image
- There are no images

The current goal is to have 4 images per card, 1 if a person card. 
If no image is specified in the concept response, the current back-up query fetches 4 images, no matter the type of card, no matter the size of the image.

## 2. How to curate the teaser text of a theme card?
### Why do we need to be able to do this?
The sourced description could be wrong (e.g. "Gulf of America/Mexico") or distracting/ininteresting/unnecessary (e.g. "Tropical medicine: medicine specialty").

If "wrong", it carries reputational risk.  

### What is a teaser text?
We have determined that the Theme card text could be different from the Concept page text and is therefore NOT the same as the Sourced Description.


## 2.5 Curation issues
A main issue with points 1 and 2 is the process of curation:

1. A CSV is created/edited with all the required information. 
2. A script is run (by Platform devs) which adds said information to our Concept index. 
3. Experience devs manually change hard-coded IDs in the codebase. Using these IDs, the Concept API is called and provides the required information. 
4. Deployments to prod are then required to display the changes. 

This process is difficult and the CSV method is a pain point: copy and pasting work IDs takes time and they can easily get muddled; re-check process is manual; same issue for images; and difficult to manage in Excel for reordering. 

One solution for it would be to build a tool to facilitate those pain points and enhance ownership of curation for people outside our team. 

Sticking to this method (vs curating in a CMS) would mean that the Concepts API is THE source of truth for everything, including “display label”, “teaser text” and “hero images”. It would mean only IDs are provided in Prismic and everything is fetched from there. Wellcome Authority descriptions have already been added that way. 

If we stick to the Concepts index being the one source of truth for all content, it makes it very easy to 1) keep FE queries to a minimum, 2) re-use concepts across the site and 3) removes the "dead content in the CMS" concern. It's many of us' favourite solution but the issue is manpower to get it done.

## 3. How to select curated works and concepts?
Where do Editorial/Collections colleagues browse our themes and works to find what they find interesting?


## 4. How and where to list selected works and concepts?
### Works

Four recently digitised works are featured on the CLP ([New online](https://wellcomecollection.org/collections)). 

We get the relevant IDs from Prismic [in a fragile and hacky way](https://github.com/wellcomecollection/wellcomecollection.org/blob/main/content/webapp/pages/collections/index.tsx#L110-L151) that depends on nothing in the Text slice changing aside from the IDs.  

### Concepts
Curated concepts ([Browse by theme](https://wellcomecollection.org/collections)) are currently hard-coded IDs in the code, which is not efficient, requires deployments for updates and takes ownership away from Editorial. 

### Solutions ideas

This heavily depends on WHERE the curation happens. We need to answer points 1 and 2 first. If it happens in Prismic vs if the Concepts API is the source of truth, it makes this point more or less complex to answer.

1. **We create a new Slice that makes this process more secure and more intuitive**
Ideally, this slice would also serve for Themes. For now, I’m only thinking about a way to identify the Slice better in the code (an ID field?) and then a repeatable Text field that would allow for an infinite number of IDs, links or Integration fields to be provided. A select field would also be required to indicate which endpoint is to be used (concept or work) We could then use that to fetch the relevant content. This also addresses ISSUE 3 in Featured Themes.

2. **We create a new Content type that can be linked to**
Intending to use [content relationships](https://prismic.io/docs/fields/content-relationship) in Prismic, we add a Concept custom type in Prismic that can be used to augment data from the Concept API. 
This custom type has a "Concept ID" field, "image" fields, and a "teaser description" field.In the Prismic page that references them, we have lists that can EITHER contain:
- Linked Concept Document (through content relationships) OR 
- A string referencing the Concept API. 
The onus would be on Editors whether the Concept response is good enough or requires curation through Prismic. If the latter, then they create a Concept document with the required information and chose the Linked Concept document option. 
I'm not sure we can easily represent this in the UI at the moment (the Linked document vs an ID string), so if we want to explore this option, we'll need to investigate how to do it.

3. **We explore Prismic offerings to work directly with the API.**
[The Integration fields feature](https://prismic.io/docs/fields/integration) with the [“Pull data from an API” technique](https://prismic.io/docs/fields/integration#pull-data-from-an-api) was tested by Gareth a while ago and it didn’t prove to be up to the task. It queries the provided APIs every 30minutes and pulls its data – our indexes are way too big for this to be efficient, and we currently block queries after 10,000 results. What we should investigate next is the [“Push data to Prismic” method](https://prismic.io/docs/fields/integration#push-data-to-prismic). Costs and limits will have to be explored. 

4. **Use a separate CMS that integrates with our APIs better**
We find a CMS that handles the Curated Catalogue results, one that integrates with our APIs better. This brings up a lot more questions but could be interesting to explore since Prismic has proven not to be up to par with our needs and we’re likely to continue doing Curated Collections features.  

## 5. How to display said lists?
## 6. If the content is curated through a CMS, how do we re-use it across the site?
## 7. If the content is curated through a CMS, how do we ensure we don't create a ton of dead content?
For all of the above, it heavily depends on WHERE the curation happens. We need to answer points 1 and 2 first. If it happens in Prismic vs if the Concepts API is the source of truth, it makes this point more or less complex to answer.
