# RFC 055: Genres as Concepts

Genres (type/technique) should be treated in the same manner as Concepts.
This includes introducing Concept pages for them that work in a similar manner to those
for Agents (where works about and by the Agent are listed separately). A Concept
page for a Genre should list works about and using that technique.

## What is it like now?

Currently, Genres behave a little like (compound) Subjects, in that a genre may be 
cracked into its constituent concepts, making a concepts list.

Genre Links on Work pages lead to a search for the whole genre in the `genres.label` field.

However, unlike Subjects, the Genre-as-a-whole does not have its own name and identifier

Genre is not one of the types extracted from Works by the Concepts Aggregator.  It is also 
not a type that is currently assigned to a Concept.

The constituent concepts that make up a Genre also behave in a similar manner
to Subjects, where they are either a Concept ($a), or a more specific sort of Concept
(e.g. Place, Period) depending on which subfield they come from.

### What is in MARC?

* Genre is extracted from marcTag:655 fields
  * there are 1,366,260 such fields
    * 1755 of them have an identifier
      * 1688 of those have an identifier in the [LCGFT](https://id.loc.gov/authorities/genreForms.html) scheme
    * 14903 of them are compounds
      * 3 of those have an identifier (all in the [DNB](https://www.dnb.de/EN/Home/home_node.html)/[GND](https://gnd.network/Webs/gnd/EN/Home/home_node.html) scheme)

## Proposal - Catalogue Pipeline

The primary Concept that is currently in a genre's concepts list
(a Concept of type Concept, derived from the $a subfield) should now
become a Concept of type Genre.

Extract lcgft ids as authoritative identifiers for them.

### Compound Genres as a whole

There are three options for dealing with compound genres as a whole in the data.

* make it work in the same manner as Subjects,
* treat it more explicitly as an extra Concept.
* leave them, they don't exist. (recommended)

#### Like a Subject

The most consistent approach is to treat Genres in the same manner as Subjects.
The Genre-as-a-whole becomes Identifiable, and an id is minted for it.

This would require little if any change to the Catalogue API and Work pages.

Currently, the Concepts pipeline and API extracts "things that look like Concepts"
from anywhere in a Work. This is anything that has one of the known Concept
types, and is identified. This currently includes Subjects, and would include
Genres with this change.

However, the relationship between a compound subject and its identifier differs
from the relationship between compound genres and their identifiers.  An identified
genre is an atomic unit that can be further embellished by extra subfields, whereas
the various subfields form part of the subject.

The consistency gained by treating a Genre like a Subject may therefore be confusing.

#### As an extra Concept

A less consistent, but possibly more future-looking approach would be to
treat the whole Genre as an extra concept in its concepts list.

The Genre-as-a-whole stays as it is, unidentified, but bearing the type Genre.

In the case of a compound Genre, a new Concept of type Genre,
representing the Genre as a whole, could be inserted as the first
concept in the concepts list.

This would be inconsistent with the way Subjects are represented, but is a better 
representation of what is happening in the Concepts pipeline and API.

Rather than Genres being another thing that looks like a Concept to be
extracted by the Concepts Pipeline, the Works pipeline would be putting it
in the concepts list.

As this would also require a more significant change to the Catalogue API and
Works pages to link to the Genre's Concept page, and would result in API data
containing inconsistent approaches for Genres vs Subjects or Contributors, it would be better 
to consider this approach as part of API v3, if desired.

#### Leave them

Compound Genres are unlike Subjects, in that rare situation (three instances) that they are identified in MARC, 
the identifier refers to the primary Concept within it, and not to the overall Genre.  Similarly, LCGFT does not contain
compounds.

e.g. from b30834107
```
655  7  |0(DE-588)4135467-9 |aAusstellungskatalog |xMiltärhistorisches Museum der Bundeswehr |y27.04.2018-30.10.2018 |zDresden. |2gnd-content
```
The id in $0 refers to the genre [Austellungskatalog](https://portal.dnb.de/opac.htm?method=simpleSearch&cqlMode=true&query=nid%3D4135467-9) 
and not to anything in the x, y, or z subfields.

As a result, the correct target for a genre link should be to the genre of the primary concept.  This is the same 
UI behaviour as contributors.

There is some conflict here between the apparent semantics of the three fields.  A Genre feels more like a subject, 
in that the compounds are "things that exist in their own right", whereas the compounding of a Contributor is about 
the relationship between an Agent and a Work.

Some compound genres seem excessively specific for this purpose, leading to fragmentation 
(e.g. Almanacs, which have many entries like `Almanacs - Pennsylvania - 1773` and `Almanacs - Massachusetts - 1702`, 
each with less than half a dozen entries), so having `Almanacs` as the concept page is probably more useful.

## Proposal - Concepts Pipeline

The concepts pipeline will start extracting Genre as one of the types of Concept.

[RFC 054](../054-authority-vs-canonical-concept-ids) covers the technique
that will be used to match Genre-as-a-Subject (where it can only be a Concept)
with Genre-as-a-Genre (where it will be a Genre).

Include LCGFT as an authoritative source.

## Proposal - website

Genre links on Work pages will link to the Concept page for their primary Concept.  
The remaining parts of the compound will still be displayed in the link text, 
but are not used to further refine that link.

## Rationale

There are two goals for the data that need to be supported by this work.

Determining Genre-ness - When rendering a Concept Page or API result for a Genre, how do we know
that it is a Genre, in order to do genre-specific things, e.g. populate a "works of this type" list.

Determining equivalence - The ability to determine that when a work is about a genre and another work is 
in that genre, that when they both refer to the same thing.

### Determining Genre-ness with the current data

With the current data, the only way to determine whether a Concept is a Genre
would be to assume that all Concepts may be Genres, and perform a text search in 
the genre.label and genre.concepts.label field in order to populate the "works in this genre" list.

This is problematic. Because Genres may be compound, searching on genre.concepts
will pick up things that are not genres.  Searching on genre alone would not
allow us to link things that should be linked.

For example: `Advertising fliers - England - London - 18th century` is a 
compound genre, where "Advertising fliers" is currently a Concept.

So, either only `Advertising fliers - England - London - 18th century` is 
treated as a Genre, meaning that `Advertising fliers` is not.  Or all
of `Advertising fliers`, `England`, `London`, `18th century` behave as genres.

Neither of these solutions are satisfactory.

We could treat only Concepts of type Concept as potential Genres, which 
would achieve the desired result.

### Determining Genre-ness with the proposed data

In the example above, `Advertising fliers` would be a Genre, so that 
can be used as the signal to look for other works using that technique.

### Determining equivalence with the current data

Currently, because both the primary Concept in a Genre's concept list, and the
primary Concept in a Subject's concept list are of type Concept, they are already
the same.

However, a compound Genre and an identical compound Subject differ on type,
so even if they were identified, they would not be the same.

### Determining equivalence with the proposed data

The primary Concept within a genre will be of type Genre.

This breaks that automatic link between the primary Concept of a Subject and 
that of a Genre.  However, this proposal includes a mechanism for determining 
sameAs relationships in this case.

When requesting works containing a given Concept, the sameAs list will be 
consulted and the resulting query to Elasticsearch will fetch works containing
both the originally requested Concept, and its equivalents.

Both compound and simple concepts will work in a consistent fashion.

## Further Considerations

The data exists, and will continue to exist, to allow for filtering on
non-genres in the genre.concepts field. For example, it will remain possible
to query for `genre.concepts=London`.

Whether this becomes a feature that gets exposed via the API is out of scope
of this RFC, but it is one that can be supported by the data format.

There are  220 different Almanacs (e.g. `Almanacs - Pennsylvania - 1765`), 
89 different Poems (e.g. `Poems - 1740`), but most top level genres are not compounds. 
