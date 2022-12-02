# Transforming Data

We use transformation functions to parse the data we get from the Prismic API, to best present that data in the frontend. 
We try to ensure we are only ever passing the data a page needs to the frontend, so you will see throughout `content/webapp` the convention of 
`Article` and `ArticleBasic`. 

If you check out the `services/prismic` folders within `content/webapp` you will see we have split the fetching and transforming and represented
that in the folder structure. If we take a look at [articles as an example](https://github.com/wellcomecollection/wellcomecollection.org/blob/main/content/webapp/services/prismic/transformers/articles.ts), you can see how we parse/mutate the incoming data from Prismic
and display the json in the format we want for the frontpage, in this case `weco.org/articles`.

