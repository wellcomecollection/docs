import { DocumentMapping } from "../mapping";

// Events being slightly complicated, this is to be further developed 
// https://github.com/wellcomecollection/wellcomecollection.org/issues/11402
const eventDocument: DocumentMapping = {
  id: "WwQHTSAAANBfDYXU",
  uid: "lorem-ipsum",
  display: {
    type: "Event",
    id: "WwQHTSAAANBfDYXU",
    uid: "lorem-ipsum",
    title: "Lorem ipsum",
    format: "Comic",
    description: "Aliquam erat volutpat",
    date: "22 December 2022",
  },
  query: {
    type: "Event",
    title: "[title] [format]",
    description: "[promo caption] [standfirst]",
    body: "Lorem ipsum dolor sit amet"
  },
};
