const bookDocument = {
  id: "WwQHTSAAANBfDYXU",
  uid: "lorem-ipsum",
  display: {
    type: "Book",
    id: "WwQHTSAAANBfDYXU",
    uid: "lorem-ipsum",
    title: "Lorem ipsum",
    description: "Aliquam erat volutpat", // (promo.caption || standfirst) ?
  },
  query: {
    // TODO determine which fields should exist across all content types, what name they should have
    // and which Prismic fields they could contain.
    //
    // type: "Book"
    // id: "WwQHTSAAANBfDYXU", // do we want to allow search by ID?
    // title: "Lorem ipsum",
    // subtitle: "Dolor sit amet",
    // description: "Aliquam erat volutpat",
    // standfirst: "" // Allow both promo.caption AND standfirst to live IN description?
    // body: "Lorem ipsum dolor sit amet",
    // contributors: []
  },
};
