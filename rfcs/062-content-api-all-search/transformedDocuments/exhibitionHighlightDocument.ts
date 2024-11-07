// TODO: We'll need one document for Audio and one for BSL, even though it's the same Prismic document
// so this needs further discussion

const exhibitionAudioHighlightDocument = {
  id: "WwQHTSAAANBfDYXU",
  uid: "jason-and-the-adventure-of-254",
  display: {
    type: "Exhibition audio highlight tour",
    id: "WwQHTSAAANBfDYXU",
    uid: "jason-and-the-adventure-of-254",
    title: "Jason and the Adventure of 254 audio highlight tour with transcripts",
    description: "Aliquam erat volutpat", // Prismic field is intro_text
  },
  query: {
    // TODO determine which fields should exist across all content types, what name they should have
    // and which Prismic fields they could contain.
    //
    // type: "Exhibition audio highlight tour"
    // id: "WwQHTSAAANBfDYXU", // do we want to allow search by ID?
    // title: "Jason and the Adventure of 254 audio highlight tour with transcripts",
    // description: "Aliquam erat volutpat",
    // body: "Lorem ipsum dolor sit amet"
  },
};


const exhibitionBSLHighlightDocument = {
  id: "WwQHTSAAANBfDYXU",
  uid: "jason-and-the-adventure-of-254",
  display: {
    type: "Exhibition BSL highlight tour",
    id: "WwQHTSAAANBfDYXU",
    uid: "jason-and-the-adventure-of-254",
    title: "Jason and the Adventure of 254 British Sign Language tour with subtitles",
    description: "Aliquam erat volutpat", // Prismic field is intro_text
  },
  query: {
    // TODO determine which fields should exist across all content types, what name they should have
    // and which Prismic fields they could contain.
    //
    // type: "Exhibition BSL highlight tour"
    // id: "WwQHTSAAANBfDYXU", // do we want to allow search by ID?
    // title: "Jason and the Adventure of 254 British Sign Language tour with subtitles",
    // description: "Aliquam erat volutpat",
    // body: "Lorem ipsum dolor sit amet"
  },
};
