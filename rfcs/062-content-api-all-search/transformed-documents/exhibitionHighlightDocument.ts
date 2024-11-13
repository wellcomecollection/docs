// TODO: We'll need one document for Audio and one for BSL, even though it's the same Prismic document
// so this needs further discussion

import { DocumentMapping } from "../mapping";

const exhibitionAudioHighlightDocument: DocumentMapping = {
  id: "WwQHTSAAANBfDYXU",
  uid: "jason-and-the-adventure-of-254",
  display: {
    type: "Exhibition audio highlight tour",
    id: "WwQHTSAAANBfDYXU",
    uid: "jason-and-the-adventure-of-254",
    title: "Jason and the Adventure of 254 audio highlight tour with transcripts",
    description: "Aliquam erat volutpat", 
  },
  query: {
    type: "Exhibition audio highlight tour",
    title: "Jason and the Adventure of 254 audio highlight tour with transcripts",
    description: "[intro text]",
    body: "Lorem ipsum dolor sit amet"
  },
};


const exhibitionBSLHighlightDocumen: DocumentMapping = {
  id: "WwQHTSAAANBfDYXU",
  uid: "jason-and-the-adventure-of-254",
  display: {
    type: "Exhibition BSL highlight tour",
    id: "WwQHTSAAANBfDYXU",
    uid: "jason-and-the-adventure-of-254",
    title: "Jason and the Adventure of 254 British Sign Language tour with subtitles",
    description: "Aliquam erat volutpat", 
  },
  query: {
    type: "Exhibition BSL highlight tour",
    title: "Jason and the Adventure of 254 British Sign Language tour with subtitles",
    description: "[intro text]",
    body: "Lorem ipsum dolor sit amet"
  },
};
