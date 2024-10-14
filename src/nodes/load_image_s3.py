import os
import torch
import numpy as np
from PIL import Image, ImageOps, ImageSequence
from ..logger import logger
from ..client_s3 import get_s3_instance
S3_INSTANCE = get_s3_instance()


class LoadImageS3:
    @classmethod
    def INPUT_TYPES(s):
        input_dir = os.getenv("S3_INPUT_DIR")
        try:
            files = S3_INSTANCE.get_files(prefix=input_dir)
        except Exception as e:
            files = []
        return {"required":
                    {
                        "image": (sorted(files), {"image_upload": False}),
                         "s3_bucket_name": ("STRING", {"default": os.getenv("S3_BUCKET_NAME")}),
                     },

                }
    
    CATEGORY = "ComfyS3"
    RETURN_TYPES = ("IMAGE", )
    FUNCTION = "load_image"

    def load_image(self, image, s3_bucket_name):
        s3_path = os.path.join(os.getenv("S3_INPUT_DIR"), image)
        image_path = S3_INSTANCE.download_file(s3_path=s3_path, local_path=f"input/{image}")
        logger.info("START LOADING FROM S3")
        img = Image.open(image_path)
        output_images = []
        for i in ImageSequence.Iterator(img):
            i = ImageOps.exif_transpose(i)
            if i.mode == 'I':
                i = i.point(lambda i: i * (1 / 255))
            image = i.convert("RGB")
            image = np.array(image).astype(np.float32) / 255.0
            image = torch.from_numpy(image)[None,]

            output_images.append(image)


        if len(output_images) > 1:
            output_image = torch.cat(output_images, dim=0)

        else:
            output_image = output_images[0]

        return output_image