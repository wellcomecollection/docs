# Deployment example

This is an example TF stack demonstrating the principles described in this RFC.

## Usage

### Setup

You will need to create the stack and populate the ECR repositories.

```
# Create the stack
terraform apply

# Populates ECR repos with images
./deploy.sh
```

You should receive a list of the images in ECR:

```
{
    "imageIds": [
        {
            "imageDigest": "sha256:4fe8827f51a5e11bb83afa8227cbccb402df840d32c6b633b7ad079bc8144100",
            "imageTag": "prod"
        },
        {
            "imageDigest": "sha256:afe605d272837ce1732f390966166c2afff5391208ddd57de10942748694049d",
            "imageTag": "hash_2"
        },
        {
            "imageDigest": "sha256:4fe8827f51a5e11bb83afa8227cbccb402df840d32c6b633b7ad079bc8144100",
            "imageTag": "hash_1"
        }
    ]
}
```

You can see there are 2 images (notice the matching digests) under 3 tags. By default `hash_1` is tagged `prod`.

### Check the state

You can then run `check.sh` to view the current state of deployments.

This lists the image digests in use by the services current tasks, along with the digest currently tagged "prod".

```
$ ./check.sh
prod ENV_DIGEST: sha256:4fe8827f51a5e11bb83afa8227cbccb402df840d32c6b633b7ad079bc8144100

All TASK_DIGESTS will match the ENV_DIGEST when the deployment is complete.

TASK_DIGEST: sha256:4fe8827f51a5e11bb83afa8227cbccb402df840d32c6b633b7ad079bc8144100 (match)
```

### Deploy

You can choose to deploy `hash_2` as follows:

```
# Populates ECR repos with images
./deploy.sh hash_2
```

This will update the image tags so that `hash_2` is tagged `prod` and a redeployment is forced.

Again you can check the status of the deployment by running `check.sh`.

If you check while the transition is occuring you may see both tasks available with the new image_id task replacing the old.

```
$ ./check.sh
prod ENV_DIGEST: sha256:afe605d272837ce1732f390966166c2afff5391208ddd57de10942748694049d

All TASK_DIGESTS will match the ENV_DIGEST when the deployment is complete.

TASK_DIGEST: sha256:afe605d272837ce1732f390966166c2afff5391208ddd57de10942748694049d (match)
TASK_DIGEST: sha256:4fe8827f51a5e11bb83afa8227cbccb402df840d32c6b633b7ad079bc8144100 (no_match)
```

