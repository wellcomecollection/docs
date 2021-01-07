# Searching with the CALM API

### 16 December 2019, Alex Chan

This has some notes on using the CALM API, and an example script for searching all the records in the CALM catalogue.

## Motivation

As part of the born-digital content migration, I had a collection of directories on the V drive with accession-like numbers, and I wanted to get a list of all the accession numbers in CALM, so I could match the directories to accession numbers:

```text
AAUICW_2185 ~> AAUICW accession 2185?
AAUNAM_2213 ~> AAUNAM accession 2213?
AAUNAM_2254 ~> AAUNAM accession 2254?
```

Exporting a list of accession numbers from the CALM GUI would have been tricky \(I don't have access to CALM on my Mac\), so I tried using the CALM API to export the data.

What is an accession/accession number? &gt; In archives practice, an \*accession\* is all the material that gets collected at one time from a single source. &gt; The \*accession identifier\* is the unique identifier given to that batch of material. &gt; &gt; At Wellcome, the accession identifier is made of two parts: the \*accession number\* \(sequential, currently up to 2551\) and a \*collection reference\* \(such as WT, PPMTW, SANCT\).

In the storage service, we are going to use the _accession number_ as the identifier \(with the collection reference included in the package, in case there's a typo in the accession number\). This is to avoid ambiguity between catalogue references and accession references \(e.g. `WT/1` vs. `WT accession 1`\).

At some point, we may start storing born digital accessions with Sierra o-numbers \(`o12345678`\), and the bare accession number plays nicer with that system.

## Resources

* The docs for Wellcome's CALM API installation are available at [http://archives.wellcomelibrary.org/CalmAPI/help/index.htm](http://archives.wellcomelibrary.org/CalmAPI/help/index.htm) \(externally visible\) or [http://wt-calm/CalmAPI/help/index.htm](http://wt-calm/CalmAPI/help/index.htm) \(internal only\).
* You can check the status of the API at [http://wt-calm/CalmAPI/](http://wt-calm/CalmAPI/).
* Talk to Library Systems for credentials to access the API.

## Searching the API

Useful pieces for searching the API:

* **Make a Search request using the SOAP API.**

  Example request/responses are here: [http://archives.wellcomelibrary.org/CalmAPI/help/example\_search.htm](http://archives.wellcomelibrary.org/CalmAPI/help/example_search.htm) This returns an XML response that tells you how many results there are.

  I know you can search the "Catalog", "Accessn", "Locations" and "Persons" databases; there might be more I'm unaware of. There are lots of databases in CALM, but not all of them are populated. Look in the CALM GUI for ideas of what else you can search!

  The wildcard `*` is a useful search term: it return everything.

  Example Python code \`\`\`python \# base\_api\_url \(str\): base API URL, e.g. 'http://wt-calm' \# database \(str\): which database do you want to search? \# search\_term \(str\): what are you searching for? sess = requests.Session\(\) resp = sess.post\( f"{base\_api\_url}/CalmAPI/ContentService.asmx", headers={ "SOAPAction": "http://ds.co.uk/cs/webservices/Search", "Content-Type": "text/xml; charset=utf-8" }, auth=auth, data=f"""{database}DC{term} """.strip\(\) \) root = ET.fromstring\(resp.text\) \# The XML returned is of the form \# \# \# \# \#N \# \# \# \# \# and the value in SearchResult tells us how many results there were. \# \# See http://wt-calm/CalmAPI/ContentService.asmx?op=Search \# search\_result = root.find\( "./" "{http://www.w3.org/2003/05/soap-envelope}Body/" "{http://ds.co.uk/cs/webservices/}SearchResponse/" "{http://ds.co.uk/cs/webservices/}SearchResult" \) \`\`\`

* **Make an Overview request to get a summary of the results.**

  I haven't tried this, but it lets you get a slice of the results. For example, _"tell me the title of results 1 to 10"_. In the Catalog database, one of those fields is `"Modified"`, so you could check the modified field of every record, and use that to decide which records to get a detailed view of.

* **Make a SummaryHeader request to get all the fields on an individual item.**

  This allows you to get a detailed view of a single result in a given session. For example, _"tell me everything about the first search result"_.

  Example Python code \`\`\`python for hit\_lst\_pos in range\(hit\_count\): \# See http://wt-calm/CalmAPI/ContentService.asmx?op=SummaryHeader summary\_header\_resp = sess.post\( f"{base\_api\_url}/CalmAPI/ContentService.asmx", headers={ "SOAPAction": "http://ds.co.uk/cs/webservices/SummaryHeader", "Content-Type": "text/xml; charset=utf-8" }, auth=auth, data=f"""{database}{hit\_lst\_pos} """.strip\(\) \) \# The response XML is of the form: \# \# \# \# \# \#string \# \# \# \# result\_root = ET.fromstring\(summary\_header\_resp.content\) result\_string = result\_root.find\( "./" "{http://schemas.xmlsoap.org/soap/envelope/}Body/" "{http://ds.co.uk/cs/webservices/}SummaryHeaderResponse/" "{http://ds.co.uk/cs/webservices/}SummaryHeaderResult" \).text \# The result is of the form: \# \# \#Component \# \# ... \# \# summary\_root = ET.fromstring\(result\_string\).find\(".//Summary"\) yield summary\_root \`\`\`

The Search request is attached to a persistent "session" -- somehow the API knows you want the results from a given Search request \(cookies, maybe\). I was using a persistent `requests.Session()` in Python and that seemed to work fine.

Two possible approaches:

* **I want to get everything.**

  Make a Search request with database `Catalog` and search term `*`. That tells you how many results there are, then iterate from `0 to (hit count – 1)` \(the results are 0-indexed\), and call SummaryHeader for each.

* **I want to get recently updated stuff.**

  You don't want to make a SummaryHeader request for each record -- that's slow and unnecessary.

  Make a Search request with database `Catalog` and search term `*`. Iterate over that number in batches with Overview, inspecting the Modified field. For records that have been modified recently, call SummaryHeader to get the full record.

## Candy bag of other thoughts

* The CALM API is _only_ available over HTTP, not HTTPS. We should fix that if we want to use it over the public Internet.
* The CALM API returns results as XML, but the script below serialises them as JSON. This is fine for experiments, but be careful if using this data in anger. For example, I've seen CALM return XML of the form:

  ```markup
  <?xml version="1.0" encoding="ISO-8859-1"?><SummaryList><Summary>
    <AltRefNo>LE/MON/1</AltRefNo>
    ...
  </xml>
  ```

  and

  ```markup
  <?xml version="1.0" encoding="ISO-8859-1"?><SummaryList><Summary>
    <AltRefNo>LE/MON/1</AltRefNo>
    <AltRefNo>LE/MON/1</AltRefNo>
    ...
  </xml>
  ```

  One would serialise to JSON as a string, the other a list.

  This might indicate an error somewhere in CALM that we want to fix \(and now we have the API, we can find all those places!\)

* AFAICT, the CALM API is read-only -- so there's less risk of a coding error triggering irreparable damage to the CALM database. \(I thought I'd seen that written down somewhere, but I can't find the reference now.\)

## I want code! 🤓

Look at the Python script [`2019-12-16_searching_with_the_calm_api.py`](https://github.com/wellcomecollection/docs/tree/cd5ed3da218cb0fee0b1e0d34fb45bb46d568c6d/research/code/2019-12-16_searching_with_the_calm_api.py).

It implements the "I want to get everything" search described above.

