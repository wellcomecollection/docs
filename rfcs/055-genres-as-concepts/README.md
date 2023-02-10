# RFC 055: Genres as Concepts

Genres (type/technique) should be treated in the same manner as Concepts.
This includes introducing Concept pages for them that work in a similar manner to those
for Agents (where works about and by the Agent are listed separately). A Concept
page for a Genre should list works about and using that technique.

## What is it like now?

Currently, Genres behave a little like (compound) Subjects, in that it is 
cracked into its constituent concepts, making a concepts list.

However, unlike Subjects, the Genre-as-a-whole does not have its own name and identifier

Genre is also not one of the types extracted from Works by the Concepts Aggregator.

The constituent concepts that make up a Genre also behave in a similar manner
to Subjects, where they are either a Concept ($a), or a more specific sort of Concept
(e.g. Place, Period) depending on which subfield they come from.

## Proposal - Catalogue Pipeline

The Genre-as-a-whole stays as it is, unidentified, but bearing the type Genre.

The primary Concept that is currently in its concepts list 
(a Concept of type Concept, derived from the $a subfield) should now 
become a Concept of type Genre.

In the case of a compound Genre, a new Concept representing the Genre as a whole should be inserted as the first
concept in the concepts list.

This will be inconsistent with the way Subjects are represented, but is a better 
representation of what is happening in the Concepts API.


## Proposal - Concepts Pipeline

The concepts pipeline will start extracting Genre as one of the types of Concept.

[RFC 054](../054-authority-vs-canonical-concept-ids) covers the technique
that will be used to match Genre-as-a-Subject (where it can only be a Concept)
with Genre-as-a-Genre (where it will be a Genre).

## Rationale

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
so are not the same.

### Determining equivalence with the proposed data

Both the compound concept and primary Concept within it will be of type Genre.

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
of this RFC, but it is one that can be supported by the data format.  However,
the actual data behind it may not be appropriate to support it.  There are 
220 different Almanacs (e.g. `Almanacs - Pennsylvania - 1765`), 89 different Poems
(e.g. `Poems - 1740`), but most top level genres are not compounds. 
