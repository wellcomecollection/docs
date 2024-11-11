// Proposal for /all API response.

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
      workType: [
        {
          id: "a",
          label: "Books",
          count: 931,
        },
        {
          id: "h", 
          label: "Archives and manuscripts",
          count: 398,
        },
      ]
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
