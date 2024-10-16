from .nodes.load_image_s3 import LoadImageS3
from .nodes.save_image_s3 import SaveImageS3


NODE_CLASS_MAPPINGS = {
    "LoadImageS3": LoadImageS3,
    "SaveImageS3": SaveImageS3,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "LoadImageS3": "Nextry Load Image from S3",
    "SaveImageS3": "Nextry Save Image to S3",
}