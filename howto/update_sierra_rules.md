#  HOWTO: Update Sierra Rules in the pipeline and api 

## What

When the rules for extracting Sierra data have changed in the catalogue pipeline
project, the rule changes may also need to be copied to the API, in order to 
ensure that the most up-to-date content is shown to users.

The specific situation in which you will need to do this can be determined by
looking at the check_vendored_code script in catalogue-api to see which files
it copies.

## How

1. Make your changes in [catalogue-pipeline](https://github.com/wellcomecollection/catalogue-pipeline)
2. Take that process all the way so that the changes are on main and you are satisfied they work
3. Take a branch of [catalogue-api](https://github.com/wellcomecollection/catalogue-api)
4. Run the [check_vendored_code](https://github.com/wellcomecollection/catalogue-api/blob/main/.buildkite/scripts/check_vendored_code.py) Python script
5. Satisfy yourself that it has worked, commit and push the resulting changes.
6. When CI says all is well, merge your catalogue-api branch to main and continue with the normal catalogue-api deployment process.