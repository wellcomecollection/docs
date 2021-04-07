# E-Resource Authentication

Wellcome Collection like many other institutions offers its staff and patrons access to electronic journals & books offered by online databases/publishers.

The list of databases offered is [available on the Wellcome Collection site](https://wellcomecollection.org/pages/YDaP2BMAACUAT7DS).

The "Collections and Research" team handles relationships with publishers / database providers, negotiates terms of access and communicate changes in access requirements.

As part of decommissioning the Wellcome Library site we must ensure continuity of access to those resources for patrons and staff.

## E-resources in the Catalogue API

E-resources are currently available from the page linked above, but [can also be found](https://api.wellcomecollection.org/catalogue/v2/works?query=awa6c6gm&include=items) in the catalogue API.

Items will have an `online-resource` location, for example:

```json
{
  "@context": "https://api.wellcomecollection.org/catalogue/v2/context.json",
  "type": "ResultList",
  "pageSize": 10,
  "totalPages": 1,
  "totalResults": 1,
  "results": [
    {
      "id": "awa6c6gm",
      "title": "Nature",
      "alternativeTitles": [
        "Nature (Online)"
      ],
      "workType": {
        "id": "d",
        "label": "Journals",
        "type": "Format"
      },
      "items": [
        {
          "locations": [
            {
              "locationType": {
                "id": "online-resource",
                "label": "Online resource",
                "type": "LocationType"
              },
              "url": "http://resolver.ebscohost.com/Redirect/PRL?EPPackageLocationID=667.50974.646402&epcustomerid=s7451719",
              "linkText": "Connect to Nature Publishing Group",
              "accessConditions": [
                {
                  "status": {
                    "id": "licensed-resources",
                    "label": "Licensed resources",
                    "type": "AccessStatus"
                  },
                  "type": "AccessCondition"
                }
              ],
              "type": "DigitalLocation"
            }
          ],
          "type": "Item"
        }
      ],
      "availabilities": [
        {
          "id": "online",
          "label": "Online",
          "type": "Availability"
        }
      ],
      "type": "Work"
    }
  ]
}
```

The URL indexed is for the [EBSCO](https://www.ebsco.com/) Link Resolver
                           
EBSCO is a service used by "Collections and Research" to handle database/e-journal metadata.

## Current access methods

### Staff

Access for staff is via [Shibboleth](https://en.wikipedia.org/wiki/Shibboleth_Single_Sign-on_architecture), a profile of [SAML](https://en.wikipedia.org/wiki/Security_Assertion_Markup_Language).

We have an on-premises implementation hosted at [idp.wellcome.ac.uk](https://idp.wellcome.ac.uk/idp/shibboleth) and managed by [Overt](https://www.overtsoftware.com/overt-idp/). Staff users authenticate via Active Directory using their Wellcome accounts.

Staff access will be unaffected by the shut down of the Wellcome Library site. 

### Patrons

Library patrons can get access to e-resources by the following methods.

#### Kiosk access

Patrons who are on the library premises can get access from "kiosk" computers that sit on the Wellcome Collection network.

Access to e-resources is achieved by providing publishers / database providers with a fixed IP range from which resources will be accessed. 

The kiosk access method must be maintained and should be unaffected by the shut down of the Wellcome Library site.

The EBSCO link resolver URL that is referenced in Catalogue API results will provide you with a WAM Proxy link that does not require authentication.

#### Sierra WAM Proxy 

Patrons who are not on library premises can currently get access by signing in to Wellcome Library using their OPAC/Sierra login and accessing resources via the WAM Proxy.

For users who are signed in the sequence diagram for accessing e-resources would look like:

![WAM proxy sequence diagram](wam_sequence.png)

Users authenticated with Sierra have their requests proxied from an on-premises IP recognised by a publisher.

A user who is not authenticated is redirected to sign in with Sierra at https://catalogue.wellcomelibrary.org/iii/cas/login and query parameters on that page direct users back to the proxied publisher URL if sign-in is successful.  

Patrons will no longer be able to use sign-in via Sierra when they switch to using the new SSO solution as their password will not be synchronised with Sierra, we would also seek to use the new SSO solution to authenticate users to maintain consistency in UI and process.
