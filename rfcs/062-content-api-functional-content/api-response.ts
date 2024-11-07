// Proposal for /generic API response. TODO: find different name for it though.

const apiResponse = {
  type: "ResultList",
  results: [
    {
      type: "Page"
      //... whatever is in "display" in pageDocument.
    },
    {
      type: "Visual story"
      //... whatever is in "display" in visualStoryDocument.
    }
  ],
  pageSize: 10,
  totalPages: 49,
  totalResults: 482,
  nextPage:
    "https://api.wellcomecollection.org/content/v0/generic?page=2", // To do, find different name
};
