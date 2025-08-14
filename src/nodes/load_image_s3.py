import os
import torch
import numpy as np
from PIL import Image, ImageOps, ImageSequence

from ..client_s3 import get_s3_instance
from ..logger import logger

S3_INSTANCE = get_s3_instance()


class NextryLoadImageS3:
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
        # image = "generation-type/preview/1.png" (ключ в бакете)
        s3_path = os.path.join(os.getenv("S3_INPUT_DIR"), image)

        logger.info(f"s3_key: {image}")
        logger.info(f"s3_path (with input dir): {s3_path}")

        # Скачиваем по правильному пути в локальный файл
        local_path = f"input/{image}"
        os.makedirs(os.path.dirname(local_path), exist_ok=True)
        image_path = S3_INSTANCE.download_file(
            s3_path=image,  # ключ в бакете
            local_path=local_path,
            bucket_name=s3_bucket_name
        )

        pil_img = Image.open(image_path)

        # Если не анимированная картинка — просто один кадр
        if not getattr(pil_img, "is_animated", False):
            frame = ImageOps.exif_transpose(pil_img.convert("RGBA"))
            W, H = frame.size
            rgb = frame.convert("RGB")
            arr = (np.asarray(rgb).astype(np.float32) / 255.0)
            img_t = torch.from_numpy(arr).unsqueeze(0)  # [1,H,W,3]

            if "A" in frame.getbands():
                alpha = (np.asarray(frame.getchannel("A")).astype(np.float32) / 255.0)
                mask = 1.0 - torch.from_numpy(alpha)     # [H,W], 1=непрозрачн.
            else:
                mask = torch.zeros((H, W), dtype=torch.float32)

            return img_t, mask.unsqueeze(0)              # [1,H,W,3], [1,H,W]

        # Анимированный случай: выравниваем все кадры к размеру первого
        output_images = []
        output_masks = []

        target_W = target_H = None

        for idx, fr in enumerate(ImageSequence.Iterator(pil_img)):
            fr = ImageOps.exif_transpose(fr.convert("RGBA"))
            if idx == 0:
                target_W, target_H = fr.size
            elif fr.size != (target_W, target_H):
                fr = fr.resize((target_W, target_H), Image.LANCZOS)

            rgb = fr.convert("RGB")
            arr = (np.asarray(rgb).astype(np.float32) / 255.0)
            img_t = torch.from_numpy(arr).unsqueeze(0)  # [1,H,W,3]
            output_images.append(img_t)

            if "A" in fr.getbands():
                alpha = (np.asarray(fr.getchannel("A")).astype(np.float32) / 255.0)
                mask = 1.0 - torch.from_numpy(alpha)    # [H,W]
            else:
                mask = torch.zeros((target_H, target_W), dtype=torch.float32)
            output_masks.append(mask.unsqueeze(0))       # [1,H,W]

        output_image = torch.cat(output_images, dim=0)   # [B,H,W,3]
        output_mask  = torch.cat(output_masks,  dim=0)   # [B,H,W]
        return output_image, output_mask