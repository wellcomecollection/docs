// TODO: We'll need one document for Audio and one for BSL, even though it's the same Prismic document
// so this needs further discussion

const exhibitionHighlightDocument = {
  id: "WwQHTSAAANBfDYXU",
  uid: "lorem-ipsum",
  display: {
    type: "Exhibition highlight tour",
    id: "WwQHTSAAANBfDYXU",
    uid: "lorem-ipsum",
    title: "[name of exhibition] audio highlight tour with transcripts",
    introText: "Aliquam erat volutpat", // Can this be called standfirst or caption to match others?
  },
  query: {
    // TODO determine which fields should exist across all content types, what name they should have
    // and which Prismic fields they could contain.
    //
    // type: "Exhibition highlight tour"
    // id: "", // ?
    // title: "[name of exhibition] audio highlight tour with transcripts",
    // introText: "Aliquam erat volutpat", // Can this be called standfirst or caption to match others?
    // body: "Lorem ipsum dolor sit amet"
  },
};
