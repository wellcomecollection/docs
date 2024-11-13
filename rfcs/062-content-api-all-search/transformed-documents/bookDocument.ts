import { DocumentMapping } from "../mapping";

const bookDocument: DocumentMapping = {
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
    type: "Book",
    title: "[title] [subtitle]",
    description: "[promo caption] [standfirst]",
    body: "Lorem ipsum dolor sit amet",
    contributors: ["John Smith", "Jane Doe"]
  },
};
