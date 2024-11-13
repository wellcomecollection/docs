import { DocumentMapping } from "../mapping";

const seasonDocument: DocumentMapping = {
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
    type: "Season",
    title: "Lorem ipsum",
    body: "Lorem ipsum dolor sit amet",
    description: "[promo caption] [standfirst]",
  },
};
