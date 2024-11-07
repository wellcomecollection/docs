// Proposal for /all API response.
// TODO: Add Collections results in here

const apiResponse = {
  type: "ResultList",
  results: {
    content: [
      {
        type: "Page",
        //... whatever is in "display" in pageDocument.
      },
      {
        type: "Visual story",
        //... whatever is in "display" in visualStoryDocument.
      },
    ],
    works: {
      type: "Works",
      formats: [
        {
          id: "a222zvge", // for link
          label: "Lorem ipsum",
          results: 12345,
        },
        {
          id: "a223k4ra", // for link
          label: "Dolor sit",
          results: 122,
        },
      ],
    },
    images: {
      type: "Images",
      results: [
        {
          imageSrc: "http://...",
          alt: "Lorem ipsum",
          workId: "yxcd6m5x", // for link
          size: {}, // ?
        },
        {
          imageSrc: "http://...",
          alt: "Lorem ipsum",
          workId: "b5kqccbb", // for link
          size: {}, // ?
        },
      ],
    },
  },
  pageSize: 10,
  totalPages: 49,
  totalResults: 482,
  nextPage: "https://api.wellcomecollection.org/content/v0/all?page=2",
};
