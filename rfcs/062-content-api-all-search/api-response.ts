// Proposal for /all API response.

const apiResponse = {
  type: "ResultList",
  results: [
      {
        type: "Page",
        //... whatever is in "display" in pageDocument.
      },
      {
        type: "Visual story",
        //... whatever is in "display" in visualStoryDocument.
      },
  ],
  pageSize: 10,
  totalPages: 49,
  totalResults: 482,
  nextPage: "https://api.wellcomecollection.org/content/v0/all?page=2",
};
