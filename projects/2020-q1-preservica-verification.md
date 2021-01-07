# Preservica verification

## Problem

Preservica contains 41,990,996 files, many of which would be expensive or impossible to replace. Before we decommission Preservica, we want to check that every file:

* Has been successfully copied to the new storage service, or;
* Is a file we are happy to delete

This document describes how we completed this verification.

## Concepts

Within Preservica, files are organised into _deliverable units \(DUs\)_. A DU is analogous to a directory in a traditional filesystem hierarchy: DUs can be nested, and each file belongs to exactly one DU.

Each DU has an associated catalogue reference: for example, `b11633682` or `SATIH/43`. This tells us which bag in the storage service the files in this DU should be associated with. We also know when each DU was created.

We can get the following metadata about each file from the Preservica SQL database:

* The UUID that identifies the file within Preservica
* The size of the file in bytes
* The original filename of the file
* The SHA-1 checksum of the file
* The deliverable unit that this file belongs to

## The verification process: a how-to

* **Look for files that were copied byte-for-byte to the storage service.**

  The Preservica metadata lets us work out where a file would have been copied to in the storage service, if it was copied -- space, external identifier, and filename within the bag.

  If that bag exists, and it contains a file with matching filename, file size, and SHA-1 checksum, this file has been copied successfully.

* **Ignore files that we know we don't want to keep.**

  Preservica contains files that we know we don't want to keep, including:

  * Born-digital material that has been de-accessioned or was only ingested for test purposes \(working from a spreadsheet `PreservicaAppraisal.xls`\)
  * Born-digital files that are deleted by Archivematica upon ingest, such as `.DS_Store` or `thumbs.db`
  * Digitised material that we don't want to keep, e.g. images Sierra b numbers that have since been deleted
  * Digitised files that are artefacts of old processed, and should never have been copied to Preservica \(e.g. `analyse.xml`\)

  We ignored all of these files.

* **Ignore files that we know we can get from the Internet Archive.**

  In some cases, there were digitised files that hadn't been copied successfully. If we know those files originally came from the Internet Archive, we made note of the b-number on a spreadsheet, and then ignored those files.

* **Ignore files that had been replaced by newer versions.**

  Some b numbers have multiple versions -- for example, if a book was digitised and then one of the images was replaced. This would create two deliverable units.

  If the same catalogue reference has multiple DUs, ignore all files associated with all but the newest version of that DU.

* **Replace files that were corrupted during the migration process.**

  The matching process found some JP2 files that were corrupted when they were copied to the storage service. If you tried to open the JP2, you'd get an error. \(I haven't investigated, but I suspect this was a bagger bug -- the file in the storage service matches the bag manifest, but it got a bad manifest.\)

  If you find such a file, ingest a new version of the bag with the correct file, then verify the newly-uploaded file is correct.

* **Upload everything else to S3 for further inspection.**

  If there was anything that:

  * Hadn't been copied correctly
  * Wasn't in a DU we were sure we could delete
  * Wasn't something we could reharvest from Internet Archive

  then we uploaded a copy to S3 or the V drive for safekeeping, where it can be inspected and stored properly at a later date.

