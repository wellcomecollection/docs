import { DocumentMapping } from "../mapping";

// TODO display analysis
const eventDocument: DocumentMapping = {
  id: "WwQHTSAAANBfDYXU",
  uid: "lorem-ipsum",
  display: {
    type: "Event",
    id: "WwQHTSAAANBfDYXU",
    uid: "lorem-ipsum",
    title: "Lorem ipsum",
    description: "Aliquam erat volutpat", // (promo.caption || standfirst) ?
  },
  query: {
    type: "Event",
    title: "Lorem ipsum",
    description: "[promo caption] [standfirst]",
    body: "Lorem ipsum dolor sit amet"
  },
};
