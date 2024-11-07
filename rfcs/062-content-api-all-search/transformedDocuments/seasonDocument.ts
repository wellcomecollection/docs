const seasonDocument = {
  id: "WwQHTSAAANBfDYXU",
  uid: "lorem-ipsum",
  display: {
    type: "Season",
    id: "WwQHTSAAANBfDYXU",
    uid: "lorem-ipsum",
    title: "Lorem ipsum",
    description: "Aliquam erat volutpat", // (promo.caption || standfirst) ?
  },
  query: {
    // TODO determine which fields should exist across all content types, what name they should have
    // and which Prismic fields they could contain.
    //
    // type: "Season"
    // id: "WwQHTSAAANBfDYXU", // do we want to allow search by ID?
    // title: "Lorem ipsum",
    // body: "Lorem ipsum dolor sit amet",
    // description: "Aliquam erat volutpat",
    // standfirst: "" // Allow both promo.caption AND standfirst to live IN description?
  },
};
