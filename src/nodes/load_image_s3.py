import os
import torch
import numpy as np
from PIL import Image, ImageOps, ImageSequence

from ..client_s3 import get_s3_instance
from ..logger import logger

S3_INSTANCE = get_s3_instance()


class LoadImageS3:
    @classmethod
    def INPUT_TYPES(s):

        return {"required":
                    {"image": ("STRING", {"default": "generation-type/preview/1.png"}),
                     "s3_bucket_name": ("STRING", {"default": os.getenv("S3_BUCKET_NAME")}),
                     "tag": ("STRING", {"default": "generation-type"})},
                }

    CATEGORY = "ComfyS3"
    RETURN_TYPES = ("IMAGE", "MASK")
    FUNCTION = "load_image"

    def load_image(self, image, s3_bucket_name, tag):
        s3_path = os.path.join(os.getenv("S3_INPUT_DIR"), image)

        logger.info(f"s3_path: {image}")
        logger.info(f"s3_path: {s3_path}")
        image_path = S3_INSTANCE.download_file(s3_path=image, local_path=f"input/{image}", bucket_name=s3_bucket_name)

        img = Image.open(image_path)
        output_images = []
        output_masks = []
        for i in ImageSequence.Iterator(img):
            i = ImageOps.exif_transpose(i)
            if i.mode == 'I':
                i = i.point(lambda i: i * (1 / 255))
            image = i.convert("RGB")
            image = np.array(image).astype(np.float32) / 255.0
            image = torch.from_numpy(image)[None,]
            if 'A' in i.getbands():
                mask = np.array(i.getchannel('A')).astype(np.float32) / 255.0
                mask = 1. - torch.from_numpy(mask)
            else:
                mask = torch.zeros((64, 64), dtype=torch.float32, device="cpu")
            output_images.append(image)
            output_masks.append(mask.unsqueeze(0))

        if len(output_images) > 1:
            output_image = torch.cat(output_images, dim=0)
            output_mask = torch.cat(output_masks, dim=0)
        else:
            output_image = output_images[0]
            output_mask = output_masks[0]

        return output_image, output_mask