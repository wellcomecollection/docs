# URL Design

URLs are part of the user's online experience--they affect a user's ability to reliably share and reference online resources and discover and interact with the content and services we produce. 

They can also have an impact on the amount of long-term technical debt we carry since getting the URL scheme wrong means we need to maintain redirects for the duration of the site.

We therefore follow the following principles:

1. URLs are designed to be persistent—this is the most important thing to consider when minting new URLs or devising a URL scheme. In practice, this means that URLs MUST NOT include:

    a. reference to specific technology; <br/>
    b. dates unless the URL is about a date; <br/>
    c. status (old/new/draft etc.) <br/>
    d. subject unless the URL is about that subject

2. If a URL changes we SHOULD redirect to a new URL and maintain that redirect forever where a semantically equivalent resource exists;

3. When content is removed and there is no equivalent resource we SHOULD return 410 (HTTP Gone) with a link to an archived copy of the resource.

4. URLs SHOULD be as short as possible but no shorter. Deeply nested URLs have an impact on SEO and long URLs can cause problems when used in emails etc. short URLs are therefore preferable while maintaining sufficient entropy to support future growth.

5. There MUST be one URL per thing and all things have a URL. URLs are there to identify things on the Web and people use URLs to point to those things, this means:

    a. all resources MUST have a unique URL; <br/>
    b. URLs can't be used to identify two or more resources; <br/>
    c. all fragments SHOULD dereference i.e. .../foo#bar should be addressable at .../foo/bar <br/>
    d. fragments (anything after a #) don't count as unique URLs; <br/>
    e. hash-bang URLs (#!) and other techniques that rely on client side JS MUST NOT be used.

6. URLs are globally unique. A user MUST be able to share a URL and anyone, anywhere in the world MUST be able to de reference the same resource.

7. URLs can identify: things, lists of things and forms. Query parameters SHOULD be avoided for anything that’s not a list. 

8. URLs should use nouns (never verbs) - URLs are for identifying things.

9. The base of a URL path should be a plural (e.g. stories) - it identifies the collections of things. The resource can be singular.

10. A resource can be a singleton or a collection e.g. /stories/$storyID (the URL for a story) or /stories/by/formats/$format (the URL for all stories of a specific format)

11. URLs SHOULD be hackable. A user should be able to hack back a URL and get a broader set of resources e.g. it should be possible to hack back the URL for a story: .../stories/$story to .../stories/ and be returned a list of all stories or .../stories/by/formats/ for all story formats or ...stories/by/date/yyyy/mm/dd should hackable to return all stories published on the year, month or day.

12. URLs MUST NOT include any personally identifiable information, tracking parameters nor state.

13. All content MUST be served over https

14. URLs MUST be designed alongside the user interface and given the same level of care as any other UI component (possibly more because they are harder to change). We SHOULD try to have beautiful URLs

We are publishing a website not a book - make links, link between things and make those links hackable (whther or not they are linked to yet).
