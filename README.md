# ComfyS3: Amazon S3 Integration for ComfyUI 
ComfyS3 seamlessly integrates with [Amazon S3](https://aws.amazon.com/en/s3/) in [ComfyUI](https://github.com/comfyanonymous/ComfyUI). This open-source project provides custom nodes for effortless loading and saving of images, videos, and checkpoint models directly from S3 buckets within the ComfyUI graph interface.

## Installation

### Using ComfyUI Manager:

- Look for ```ComfyS3```, and be sure the author is ```TemryL```. Install it.

### Manually:
- Clone this repo into `custom_nodes` folder in ComfyUI.

### Define S3 Config
Create `.env` file in ComfyS3 root folder with the following variables:

```bash 
S3_REGION="..."
S3_ACCESS_KEY="..."
S3_SECRET_KEY="..."
S3_BUCKET_NAME="..."
S3_INPUT_DIR="..."
S3_OUTPUT_DIR="..."
```

### Optional S3 Config Variables
- `S3_ENDPOINT_URL` allows the useage of a AWS Private Link or Other S3 Compatible Storage Solutions
- `S3_PUBLIC_URL` returns public URLs after upload instead of raw S3 keys

### Cloudflare R2 Config
ComfyS3 now also understands the following Cloudflare R2-style variables:

```bash
S3_REGION="auto"
S3_ACCESS_KEY_ID="..."
S3_SECRET_ACCESS_KEY="..."
S3_ENDPOINT="https://<ACCOUNT_ID>.r2.cloudflarestorage.com"
S3_PUBLIC_URL="https://<your-public-bucket>.r2.dev"

S3_BUCKET="my-bucket"
S3_INPUT_BUCKET_NAME="my-bucket"
S3_OUT_BUCKET_NAME="my-bucket"
S3_INPUT_PREFIX="user-uploads"
S3_OUT_PREFIX="generation-results"
```

The legacy `S3_ACCESS_KEY` / `S3_SECRET_KEY` / `S3_BUCKET_NAME` / `S3_INPUT_DIR` / `S3_OUTPUT_DIR` names remain supported.

## Available Features
ComfyUI nodes to:
- [x] standalone download/upload file from/to Amazon S3
- [x] load/save image from/to Amazon S3 buckets
- [x] save VHS (VideoHelperSuite) video files to Amazon S3 buckets
- [x] send webhook notifications with image paths to custom endpoints
- [x] install ComfyS3 from [ComfyUI-Manager](https://github.com/ltdrdata/ComfyUI-Manager)
- [ ] load checkpoints from Amazon S3 buckets
- [ ] load video from Amazon S3 buckets

### Webhook Sender Node
The Webhook Sender node allows you to send POST requests to custom endpoints with image paths. This is useful for:
- Notifying your backend when image generation is complete
- Triggering post-processing pipelines
- Integrating ComfyUI workflows with external systems

See [WEBHOOK_NODE_USAGE.md](./WEBHOOK_NODE_USAGE.md) for detailed usage instructions.

## Credits
- [ComfyUI](https://github.com/comfyanonymous/ComfyUI)
- [ComfyUI-VideoHelperSuite](https://github.com/Kosinkadink/ComfyUI-VideoHelperSuite)
