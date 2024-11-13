import { DocumentMapping } from "../mapping";

// TODO display analysis
const storyDocument: DocumentMapping = {
  id: "WwQHTSAAANBfDYXU",
  uid: "lorem-ipsum",
  display: {
    type: "Story",
    id: "WwQHTSAAANBfDYXU",
    uid: "lorem-ipsum",
    title: "Lorem ipsum",
    description: "Aliquam erat volutpat", // (promo.caption || standfirst) ?
  },
  query: {
    type: "Story",
    title: "Lorem ipsum",
    description: "[promo caption] [standfirst]",
    body: "Lorem ipsum dolor sit amet"
  },
};
