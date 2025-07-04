import io
import os
import tempfile
import numpy as np
from PIL import Image
from comfy.cli_args import args

from ..client_s3 import get_s3_instance
from ..common.generator import id_generator
from ..logger import logger

WATERMARK_IMAGE_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), "watermark.png")
S3_INSTANCE = get_s3_instance()


class NextrySaveImageS3:
    
    def __init__(self):
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
        self.temp_dir = os.path.join(base_dir, "temp/")
        self.s3_output_dir = os.getenv("S3_OUTPUT_DIR")
        self.type = "output"
        self.prefix_append = ""
        self.compress_level = 4
        with open(WATERMARK_IMAGE_PATH, "rb") as f:
            self.watermark_bytes = f.read()

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "images": ("IMAGE", ),
                "filename_prefix": ("STRING", {"default": "Image"}),
                "s3_bucket_name": ("STRING", {"default": None}),
                #"add_watermark": ("BOOLEAN", {"default": True}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("s3_image_paths",)
    FUNCTION = "save_images"
    OUTPUT_NODE = True
    OUTPUT_IS_LIST = (True,)
    CATEGORY = "NEXTRY_ComfyS3"

    def apply_watermark(self, img: Image.Image, margin: int = 10) -> Image.Image:
    
        base = img.convert("RGBA")
        icon = Image.open(io.BytesIO(self.watermark_bytes)).convert("RGBA")
     
        max_w = base.width // 6
        scale = max_w / icon.width
        resample = Image.Resampling.LANCZOS
      
        icon = icon.resize((int(icon.width * scale), int(icon.height * scale)), resample)
        pos = (base.width - icon.width - margin, base.height - icon.height - margin)
        base.paste(icon, pos, icon)
        return base


    def save_images(self, images, filename_prefix="Nextry", s3_bucket_name=None):
        logger.info(f"Input params: {images}, {filename_prefix}, {s3_bucket_name}")
        filename_prefix += self.prefix_append
        full_output_folder, filename, counter, subfolder, filename_prefix = S3_INSTANCE.get_save_path(filename_prefix, images[0].shape[1], images[0].shape[0])
        results = list()
        s3_image_paths = list()
        
        for image in images:
            i = 255. * image.cpu().numpy()
            img = Image.fromarray(np.clip(i, 0, 255).astype(np.uint8))
            
            file_id = id_generator()
            file_full = f"stock_{file_id}.png"
            file_preview = f"preview_{file_id}.webp"

            try:
                image_full_temp_path = self.save_temp_image(img, suffix=".png")
                image_preview_temp_path = self.save_temp_image(img, suffix=".webp")

                # Upload the temporary file to S3
                s3_path_full = os.path.join(full_output_folder, file_full)
                s3_path_preview = os.path.join(full_output_folder, file_preview)

                file_path_s3_full = S3_INSTANCE.upload_file(image_full_temp_path, s3_path_full, s3_bucket_name)
                file_path_s3_preview = S3_INSTANCE.upload_file(image_preview_temp_path, s3_path_preview, s3_bucket_name)

                # Add the s3 path to the s3_image_paths list
                s3_image_paths.extend([file_path_s3_full, file_path_s3_preview])

                # Add the result to the results list
                results.extend([{
                    "filename": file_full,
                    "s3_path": file_path_s3_full,
                    "subfolder": subfolder,
                    "type": self.type
                    },
                    {
                        "filename": file_preview,
                        "s3_path": file_path_s3_preview,
                        "subfolder": subfolder,
                        "type": self.type
                    }])
                counter += 1

            finally:

                # Delete the temporary file
                if image_full_temp_path and os.path.exists(image_full_temp_path):
                    os.remove(image_full_temp_path)
                    logger.info(f"Removed temp file {image_full_temp_path}")

                if  image_preview_temp_path and os.path.exists(image_preview_temp_path):
                    os.remove(image_preview_temp_path)
                    logger.info(f"Removed temp file {image_preview_temp_path}")

        logger.info(f"Saved {len(results)} images to {full_output_folder}")
        logger.info({ "ui": { "images": results },  "result": s3_image_paths })
        return { "ui": { "images": results },  "result": s3_image_paths }

    def save_temp_image(self, img: Image, suffix: str = ".png") -> str:
        img = self.apply_watermark(img)
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp_file:
            temp_file_path = temp_file.name
            format_file = suffix.replace(".", "").upper()

            # Универсальная конвертация режима (лучше для совместимости)
            if img.mode not in ("RGB", "RGBA"):
                img = img.convert("RGBA" if format_file == "PNG" else "RGB")

            # Параметры сохранения
            save_kwargs = {}
            if format_file == "PNG":
                save_kwargs = {
                    "format": "PNG",
                    "compress_level": getattr(self, "compress_level", 6),  # от 0 (нет сжатия) до 9
                    "optimize": True
                }
            elif format_file == "WEBP":
                save_kwargs = {
                    "format": "WEBP",
                    "quality": getattr(self, "quality", 75),
                    "lossless": True
                }

            img.save(temp_file_path, **save_kwargs)

            return temp_file_path
        
    




