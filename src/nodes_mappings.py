from .nodes.load_image_s3 import NextryLoadImageS3
from .nodes.save_image_s3 import NextrySaveImageS3


NODE_CLASS_MAPPINGS = {
    "NextryLoadImageS3": NextryLoadImageS3,
    "NextrySaveImageS3": NextrySaveImageS3,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "NextryLoadImageS3": "Nextry Load Image from S3",
    "NextrySaveImageS3": "Nextry Save Image to S3",
}