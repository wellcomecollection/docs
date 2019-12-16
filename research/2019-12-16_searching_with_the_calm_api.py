#!/usr/bin/env python
# -*- encoding: utf-8

import collections
import getpass
import json
import xml.etree.ElementTree as ET

import inquirer
import requests


def get_search_results_for(base_api_url, database, search_query, auth):
    sess = requests.Session()

    resp = sess.post(
        f"{base_api_url}/CalmAPI/ContentService.asmx",
        headers={
            "SOAPAction": "http://ds.co.uk/cs/webservices/Search",
            "Content-Type": "text/xml; charset=utf-8"
        },
        auth=auth,
        data=f"""
        <?xml version="1.0" encoding="utf-8"?>
        <soap12:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap12="http://www.w3.org/2003/05/soap-envelope">
          <soap12:Body>
            <Search xmlns="http://ds.co.uk/cs/webservices/">
              <dbname>{database}</dbname>
              <elementSet>DC</elementSet>
              <expr>{search_query}</expr>
            </Search>
          </soap12:Body>
        </soap12:Envelope>
        """.strip()
    )

    root = ET.fromstring(resp.text)

    # The XML returned is of the form
    #
    # <soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope" ...>
    #   <soap:Body>
    #     <SearchResponse xmlns="http://ds.co.uk/cs/webservices/">
    #       <SearchResult>N</SearchResult>
    #     </SearchResponse>
    #   </soap:Body>
    # </soap:Envelope>
    #
    # and the value in SearchResult tells us how many results there were.
    #
    # See http://wt-calm/CalmAPI/ContentService.asmx?op=Search
    #
    search_result = root.find(
        "./"
        "{http://www.w3.org/2003/05/soap-envelope}Body/"
        "{http://ds.co.uk/cs/webservices/}SearchResponse/"
        "{http://ds.co.uk/cs/webservices/}SearchResult"
    )

    if search_result is None:
        raise ValueError("No result in initial result from Calm API!")

    hit_count = int(search_result.text)

    print(
        f"Found {hit_count} result{'s' if hit_count != 1 else ''} for {search_query!r}!"
    )

    for hit_lst_pos in range(hit_count):
        # See http://wt-calm/CalmAPI/ContentService.asmx?op=SummaryHeader
        summary_header_resp = sess.post(
            f"{base_api_url}/CalmAPI/ContentService.asmx",
            headers={
                "SOAPAction": "http://ds.co.uk/cs/webservices/SummaryHeader",
                "Content-Type": "text/xml; charset=utf-8"
            },
            auth=auth,
            data=f"""
            <?xml version="1.0" encoding="utf-8"?>
            <soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
              <soap:Body>
                <SummaryHeader xmlns="http://ds.co.uk/cs/webservices/">
                  <dbname>{database}</dbname>
                  <HitLstPos>{hit_lst_pos}</HitLstPos>
                </SummaryHeader>
              </soap:Body>
            </soap:Envelope>
            """.strip()
        )

        # The response XML is of the form:
        #
        #     <?xml version="1.0" encoding="utf-8"?>
        #     <soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" ...>
        #       <soap:Body>
        #         <SummaryHeaderResponse xmlns="http://ds.co.uk/cs/webservices/">
        #           <SummaryHeaderResult>string</SummaryHeaderResult>
        #         </SummaryHeaderResponse>
        #       </soap:Body>
        #     </soap:Envelope>
        #
        result_root = ET.fromstring(summary_header_resp.content)

        result_string = result_root.find(
            "./"
            "{http://schemas.xmlsoap.org/soap/envelope/}Body/"
            "{http://ds.co.uk/cs/webservices/}SummaryHeaderResponse/"
            "{http://ds.co.uk/cs/webservices/}SummaryHeaderResult"
        ).text

        # The result is of the form:
        #
        #     <?xml version="1.0" encoding="ISO-8859-1"?><SummaryList><Summary>
        #       <RecordType>Component</RecordType>
        #       <IDENTITY></IDENTITY>
        #       ...
        #     </Summary></SummaryList>
        #
        summary_root = ET.fromstring(result_string).find(".//Summary")
        summary = collections.defaultdict(list)

        for child in summary_root:
            if child.text is not None:
                summary[child.tag].append(child.text)

        for k, v in summary.items():
            if len(v) == 1:
                summary[k] = v[0]

        yield dict(summary)


if __name__ == "__main__":
    questions = [
        inquirer.Text("search_query", message="What do you want to search for?"),
        inquirer.List(
            "database",
            message="Which database do you want to search?",
            choices=["Catalog", "Accessn", "Locations"],
        ),
    ]

    answers = inquirer.prompt(questions)

    username = input("Calm username: ")
    password = getpass.getpass("Calm password: ")
    auth = (username, password)

    for summary in get_search_results_for(
        base_api_url="http://wt-calm/",
        database=answers["database"],
        search_query=answers["search_query"],
        auth=auth
    ):
        print(json.dumps(summary))
