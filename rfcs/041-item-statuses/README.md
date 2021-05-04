# RFC 041: Statuses in the items API

As part of the [requesting API](../039-requesting-api-design), we need to present an item status.
We already have a model that we'll use:

```json
"status": {
  "id" : "available",
  "label" : "Available",
  "type": "ItemStatus"
}
```

but we need to decide what value it can take.

This RFC proposes a set of values that we will present through this API.



## Guiding principles

1.  **We should not assume requests are sent to a particular service.**

    Although the initial implementation will be making requests for items in Sierra, we may add support for requesting from other systems in a future update.
    We should not assume the use of Sierra, or of Sierra item statuses.

2.  **A user's list of holds is private.**

    Alice should not be able to find out what items Bob has placed on hold, and vice versa.

3.  **The status information will be publicly visible, and displayed on the works page.**

    For consistency, we should use the same terminology as will be used on the works page.
    We should assume users will see these statuses, and not expose information about the library workings.



## Existing Sierra statuses

This section describes the existing status data in Sierra items.

Sierra presents the item status in the [Item STATUS field](https://documentation.iii.com/sierrahelp/Default.htm#sril/sril_records_fixed_field_types_item.html#STATUS).
There are standard codes supplied as part of Sierra, but libraries can define additional item status values.

This is a list of item statuses in use at Wellcome, based on the reporting cluster data.
(Deleted and suppressed items have been omitted from this analysis.)

<table>
  <tr>
    <th>code</th>
    <th>name</th>
    <th>count</th>
    <th>comment</th>
  </tr>
  <tr>
    <td><code>-</code></td>
    <td>Available</td>
    <td>616,145</td>
    <td>
      The Sierra docs say this status is "items that can circulate", and that "the item retains this status even when checked out".
      We should test with this use case, and make sure the items API responds appropriately.
    </td>
  </tr>
  <tr>
    <td><code>b</code> / <code>c</code></td>
    <td>As above</td>
    <td>41,667</td>
    <td>
      Actively unhelpful.
      This causes issues in the Catalogue API and is a custom status, so we should consider working with Collections Information to remove this.
    </td>
  </tr>
  <tr>
    <td><code>h</code></td>
    <td>Closed</td>
    <td>10,262</td>
    <td></td>
  </tr>
  <tr>
    <td><code>y</code></td>
    <td>Permission required</td>
    <td>8,476</td>
    <td></td>
  </tr>
  <tr>
    <td><code>r</code></td>
    <td>Unavailable</td>
    <td>5,884</td>
    <td></td>
  </tr>
  <tr>
    <td><code>6</code></td>
    <td>Restricted</td>
    <td>5,188</td>
    <td></td>
  </tr>
  <tr>
    <td><code>m</code></td>
    <td>Missing</td>
    <td>3,689</td>
    <td></td>
  </tr>
  <tr>
    <td><code>w</code></td>
    <td>Dept material</td>
    <td>151</td>
    <td></td>
  </tr>
  <tr>
    <td><code>p</code></td>
    <td>In cataloguing</td>
    <td>47</td>
    <td></td>
  </tr>
  <tr>
    <td><code>!</code></td>
    <td>On holdshelf</td>
    <td>33</td>
    <td></td>
  </tr>
  <tr>
    <td><code>e</code></td>
    <td>On exhibition</td>
    <td>24</td>
    <td></td>
  </tr>
  <tr>
    <td><code>s</code></td>
    <td>On search</td>
    <td>16</td>
    <td></td>
  </tr>
  <tr>
    <td><code>z</code></td>
    <td>Claims returned</td>
    <td>10</td>
    <td></td>
  </tr>
  <tr>
    <td><code>x</code></td>
    <td>Withdrawn</td>
    <td>10</td>
    <td></td>
  </tr>
  <tr>
    <td><code>a</code></td>
    <td>a</td>
    <td>3</td>
    <td></td>
  </tr>
  <tr>
    <td><code>d</code></td>
    <td>On display</td>
    <td>3</td>
    <td></td>
  </tr>
  <tr>
    <td><code>r</code></td>
    <td>Restricted</td>
    <td>3</td>
    <td></td>
  </tr>
  <tr>
    <td><code>t</code></td>
    <td>In quarantine</td>
    <td>2</td>
    <td></td>
  </tr>
  <tr>
    <td><code>f</code></td>
    <td>Returned to vendor</td>
    <td>1</td>
    <td></td>
  </tr>
  <tr>
    <td><code>0</code></td>
    <td>0</td>
    <td>1</td>
    <td></td>
  </tr>
  <tr>
    <td><code>q</code></td>
    <td>Test record</td>
    <td>1</td>
    <td></td>
  </tr>
</table>



## Proposal

We will not expose the Sierra item statuses.
Instead, we will create a new set of statuses, which will be mapped as follows:

<table>
  <tr>
    <th>id</th>
    <th>label</th>
    <th>Sierra statuses</th>
    <th>comment</th>
  </tr>
  <tr>
    <td>available</td>
    <td>Available</td>
    <td><code>-</code> / Available</td>
    <td></td>
  </tr>
  <tr>
    <td>closed</td>
    <td>Closed</td>
    <td>
      <code>h</code> / Closed <br/>
    </td>
    <td>
      We distinguish between closed/restricted/unavailable in the access statuses.
      I'm assuming it's a useful distinction here, but we could collapse this into "Unavailable" if not.
    </td>
  </tr>
  <tr>
    <td>restricted</td>
    <td>Restricted</td>
    <td>
      <code>6</code> / Restricted <br/>
    </td>
    <td>
      Ditto above.
    </td>
  </tr>
  <tr>
    <td>unavailable</td>
    <td>Unavailable</td>
    <td>
      <code>r</code> / Unavailable <br/>
      <code>m</code> / Missing <br/>
      <code>x</code> / Withdrawn
    </td>
    <td>
      I assume we wouldn't want to advertise if an item was missing.
    </td>
  </tr>
  <tr>
    <td>on-exhibition</td>
    <td>On exhibition</td>
    <td>
      <code>e</code> / On exhibition
    </td>
    <td>
    </td>
  </tr>
  <tr>
    <td>on-display</td>
    <td>On display</td>
    <td>
      <code>d</code> / On display
    </td>
    <td>
    </td>
  </tr>
  <tr>
    <td>in-cataloguing</td>
    <td>In cataloguing</td>
    <td>
      <code>p</code> / In cataloguing
    </td>
    <td>
      This feels analogous to the "on order" or "on exhibition" statuses.
    </td>
  </tr>
  <tr>
    <td>on-holdshelf</td>
    <td>On holdshelf</td>
    <td>
      <code>!</code> / On holdshelf
    </td>
    <td>
      Is the "shelf" part important?
      Could this be "on-hold"?<br/><br/>
      Do we need a way to signal "on hold for the logged-in user"?
      We don't want to expose the user ID here, but knowing "it's on hold by someone" vs "it's on hold by you" might be useful.
    </td>
  </tr>
  <tr>
    <td>in-quarantine</td>
    <td>In quarantine</td>
    <td>
      <code>t</code> / In quarantine
    </td>
    <td>
      This is arguably only useful as long as COVID lasts, but it wouldn't be too tricky to add if we wanted it.
      Normally this status is "in transit", but it seems to have been renamed temporarily.
    </td>
  </tr>
  <tr>
    <td>permission-required</td>
    <td>Permission required</td>
    <td><code>y</code> / Permission required</td>
    <td></td>
  </tr>
  <tr>
    <td>unknown</td>
    <td>Unknown</td>
    <td>(all others)</td>
    <td>
      This would be a catchall for all Sierra statuses we can't map to another status.
    </td>
  </tr>
</table>

As with the Sierra locations, we will match on the text description of the status, rather than the exact codes.
This will make us a bit less coupled to the Sierra implementation.
