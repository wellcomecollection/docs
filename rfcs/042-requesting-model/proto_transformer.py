#!/usr/bin/env python

import csv

import humanize
import termcolor


def apply_transformation_rule(row):
    # 1) If the status is "Missing", that beats everything else.
    #
    # We ignore inconsistent information in other fields -- e.g. if the status
    # is "Missing" but the "Opacmsg" is "Online request", we ignore the latter.
    #
    # Speculation: this information is left there in case the item is found
    # later, and only the status field needs to be updated.
    if row["status"] == "Missing":
        return '<status="Unavailable" note="This item is missing" isRequestable=false>'

    # 2) Similar for "Withdrawn" and "On search".
    #
    # There are three items that have status "Withdrawn" but an Opacmsg of
    # "Online request" or "By appointment".  It would be nice to fix these,
    # but it's not critical for this work.
    if row["status"] == "Withdrawn":
        return (
            '<status="Unavailable" note="This item is withdrawn" isRequestable=false>'
        )

    if row["status"] == "On search":
        return '<status="Unavailable" note="On search" isRequestable=false>'

    # 3) Handle the combination of opacmsg and status fields from the table
    # given to us by Victoria.
    if row["location"] == "ClosedStores":
        if (
            row["status"] == "Available"
            and row["opacmsg"] == "Online request"
            and row["bib_statuses"] in {"", "Open", "OpenWithAdvisory"}
        ):
            return '<status="Open/OpenWithAdvisory" note="Online request" isRequestable=true>'

        if (
            row["status"] == "Available"
            and row["opacmsg"] == "Manual request"
            and row["bib_statuses"] in {"", "Open"}
        ):
            return '<status="Open" note="Manual request" isRequestable=false>'

        if (
            row["status"] == "Restricted"
            and row["opacmsg"] == "Online request"
            and row["bib_statuses"] in {"", "Restricted"}
        ):
            return '<status="Restricted" note="Online request" isRequestable=true>'

        if (
            row["status"] == "Permission required"
            and row["opacmsg"] == "By appointment"
            and row["bib_statuses"] in {"", "ByAppointment"}
        ):
            return '<status="ByAppointment" isRequestable=false>'

        if (
            row["status"] == "Permission required"
            and row["opacmsg"] == "Donor permission"
            and row["bib_statuses"] in {"", "PermissionRequired"}
        ):
            return '<status="PermissionRequired" isRequestable=false>'

        if (
            row["status"] == "Closed"
            and row["opacmsg"] == "Unavailable"
            and row["bib_statuses"] in {"", "Closed"}
        ):
            return '<status="Closed" isRequestable=false>'

    if (
        row["status"] == "Unavailable"
        and row["opacmsg"] == "@ digitisation"
        and row["bib_statuses"] in {"", "Unavailable"}
    ):
        return '<status="TemporarilyUnavailable" note="This item is at digitisation" isRequestable=false>'

    # 4) Items on open shelves aren't requestable.
    if (
        row["location"] == "OpenShelves"
        and row["status"] == "Available"
        and row["opacmsg"] == "Open shelves"
    ):
        return '<status="Open" isRequestable=false>'

    # 5) If the status is 'as above', there's not much we can do.
    if row["status"] == "As above":
        return '<note="Please request top item" isRequestable=false>'

    return


def pretty_row(d):
    parts = []
    for k, v in d.items():
        if k in {"example_bib", "example_item", "count"}:
            continue

        if v:
            parts.append(f"{k}={v!r}")
    return "<" + " ".join(parts) + ">"


if __name__ == "__main__":
    handled_cases = 0
    handled_items = 0

    unhandled_cases = 0
    unhandled_items = 0

    with open("combinations.csv") as infile, open("unhandled.csv", "w") as outfile:
        reader = csv.DictReader(infile)

        writer = csv.DictWriter(outfile, fieldnames=reader.fieldnames)
        writer.writeheader()

        for row in reader:
            rule = apply_transformation_rule(row)
            if rule is not None:
                handled_cases += 1
                handled_items += int(row["count"])
                print(termcolor.colored(pretty_row(row), "green"))
                print(termcolor.colored(f" => {rule}\n", "green"))
            else:
                print(termcolor.colored(pretty_row(row), "red"))
                writer.writerow(row)
                unhandled_cases += 1
                unhandled_items += int(row["count"])

    print("")
    print(
        "%s case%s handled (%s items), %s case%s unhandled (%s items)"
        % (
            handled_cases if handled_cases > 0 else "No",
            "s" if handled_cases != 1 else "",
            humanize.intcomma(handled_items),
            unhandled_cases if unhandled_cases > 0 else "no",
            "s" if handled_cases != 1 else "",
            humanize.intcomma(unhandled_items),
        )
    )
