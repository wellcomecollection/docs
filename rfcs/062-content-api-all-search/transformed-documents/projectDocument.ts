import { DocumentMapping } from "../mapping";

const projectDocument:DocumentMapping = {
  id: "WwQHTSAAANBfDYXU",
  uid: "lorem-ipsum",
  display: {
    type: "Project",
    id: "WwQHTSAAANBfDYXU",
    uid: "lorem-ipsum",
    title: "Lorem ipsum",
    description: "Aliquam erat volutpat", 
    format: "Film"
  },
  query: {
    type: "Project",
    title: "[title] [format]", // We want Format to be queriable, is this the right place for it?
    body: "Lorem ipsum dolor sit amet",
    description: "[promo caption] [standfirst]",
    contributors: ["John Smith", "Jane Doe"]
  },
};
