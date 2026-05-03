import os
import posixpath
from urllib.parse import quote

import boto3
from .logger import logger
from botocore.config import Config
from botocore.exceptions import NoCredentialsError

from dotenv import load_dotenv
load_dotenv()


def get_env_value(*names, default=None):
    for name in names:
        value = os.getenv(name)
        if value is None:
            continue

        value = value.strip()
        if value:
            return value

    return default


def normalize_s3_key(value):
    if value is None:
        return ""

    normalized = value.replace("\\", "/").strip()
    if normalized in {"", ".", "/"}:
        return ""

    return normalized.lstrip("/")


def normalize_s3_prefix(value):
    return normalize_s3_key(value).strip("/")


def join_s3_key(*parts):
    normalized_parts = []
    for part in parts:
        normalized = normalize_s3_key(part).strip("/")
        if normalized:
            normalized_parts.append(normalized)

    if not normalized_parts:
        return ""

    return posixpath.join(*normalized_parts)


class S3:
    def __init__(
        self,
        region,
        access_key,
        secret_key,
        bucket_name,
        endpoint_url,
        input_bucket_name=None,
        output_bucket_name=None,
        input_dir=None,
        output_dir=None,
        public_url=None,
    ):
        self.region = region or "auto"
        self.access_key = access_key
        self.secret_key = secret_key
        self.bucket_name = bucket_name
        self.input_bucket_name = input_bucket_name or bucket_name
        self.output_bucket_name = output_bucket_name or bucket_name
        self.endpoint_url = endpoint_url
        self.input_dir = normalize_s3_prefix(input_dir)
        self.output_dir = normalize_s3_prefix(output_dir)
        self.public_url = public_url.rstrip("/") if public_url else None
        self.s3_client = self.get_client()

        if self.output_dir and not self.does_folder_exist(self.output_dir, self.output_bucket_name):
            self.create_folder(self.output_dir, self.output_bucket_name)

    def get_client(self):
        if not all([self.region, self.access_key, self.secret_key, self.bucket_name]):
            err = "Missing required S3 environment variables."
            logger.error(err)
    
        try:
            s3 = boto3.resource(
                service_name='s3',
                region_name=self.region,
                aws_access_key_id=self.access_key,
                aws_secret_access_key=self.secret_key,
                endpoint_url=self.endpoint_url,
                config=Config(s3={"addressing_style": "path"})
            )
            return s3
        except Exception as e:
            err = f"Failed to create S3 client: {e}"
            logger.error(err)

    def get_files(self, prefix, bucket_name=None):
        normalized_prefix = normalize_s3_prefix(prefix)
        list_prefix = f"{normalized_prefix}/" if normalized_prefix else ""
        target_bucket_name = bucket_name or self.output_bucket_name or self.bucket_name

        if self.does_folder_exist(normalized_prefix, target_bucket_name):
            try:
                bucket = self.s3_client.Bucket(target_bucket_name)
                files = [obj.key for obj in bucket.objects.filter(Prefix=list_prefix)]

                if list_prefix:
                    files = [
                        f[len(list_prefix):].lstrip("/")
                        for f in files
                        if f.startswith(list_prefix)
                    ]

                files = [f for f in files if f]
                return files
            except Exception as e:
                err = f"Failed to get files from S3: {e}"
                logger.error(err)
        else:
            return []
    
    def does_folder_exist(self, folder_name, bucket_name=None):
        normalized_folder_name = normalize_s3_prefix(folder_name)
        if not normalized_folder_name:
            return True

        prefix = f"{normalized_folder_name}/"

        try:
            bucket = self.s3_client.Bucket(bucket_name or self.output_bucket_name or self.bucket_name)
            response = bucket.objects.filter(Prefix=prefix)
            return any(obj.key == prefix or obj.key.startswith(prefix) for obj in response)
        except Exception as e:
            err = f"Failed to check if folder exists in S3: {e}"
            logger.error(err)
    
    def create_folder(self, folder_name, bucket_name=None):
        normalized_folder_name = normalize_s3_prefix(folder_name)
        if not normalized_folder_name:
            return

        try:
            bucket = self.s3_client.Bucket(bucket_name or self.output_bucket_name or self.bucket_name)
            bucket.put_object(Key=f"{normalized_folder_name}/")
        except Exception as e:
            err = f"Failed to create folder in S3: {e}"
            logger.error(err)

    def resolve_input_key(self, s3_path):
        normalized_s3_path = normalize_s3_key(s3_path)
        if not self.input_dir:
            return normalized_s3_path

        if normalized_s3_path == self.input_dir or normalized_s3_path.startswith(f"{self.input_dir}/"):
            return normalized_s3_path

        return join_s3_key(self.input_dir, normalized_s3_path)

    def build_public_url(self, s3_path):
        if not self.public_url:
            return None

        normalized_s3_path = normalize_s3_key(s3_path)
        encoded_path = "/".join(quote(part) for part in normalized_s3_path.split("/"))
        return f"{self.public_url}/{encoded_path}"
    
    def download_file(self, s3_path, local_path, bucket_name=None):
        local_dir = os.path.dirname(local_path)
        if not os.path.exists(local_dir):
            os.makedirs(local_dir)

        normalized_s3_path = self.resolve_input_key(s3_path)

        try:
            target_bucket_name = bucket_name or self.input_bucket_name or self.bucket_name
            bucket = self.s3_client.Bucket(target_bucket_name)
            logger.info(f"Downloading file from S3: {normalized_s3_path} to {local_path} in bucket {target_bucket_name}")
            bucket.download_file(normalized_s3_path, local_path)
            return local_path
        except NoCredentialsError:
            err = "Credentials not available or not valid."
            logger.error(err)
        except Exception as e:
            err = f"Failed to download file from S3: {e}"
            logger.error(err)

    def upload_file(self, local_path, s3_path, bucket_name=None):
        normalized_s3_path = normalize_s3_key(s3_path)

        try:
            target_bucket_name = bucket_name or self.output_bucket_name or self.bucket_name
            bucket = self.s3_client.Bucket(target_bucket_name)
            bucket.upload_file(local_path, normalized_s3_path)

            return normalized_s3_path
        except NoCredentialsError:
            err = "Credentials not available or not valid."
            logger.error(err)
        except Exception as e:
            err = f"Failed to upload file to S3: {e}"
            logger.error(err)
    
    def get_save_path(self, filename_prefix, image_width=0, image_height=0):
        def map_filename(filename):
            prefix_len = len(posixpath.basename(filename_prefix))
            prefix = filename[:prefix_len + 1]
            try:
                digits = int(filename[prefix_len + 1:].split('_')[0])
            except:
                digits = 0
            return (digits, prefix)

        def compute_vars(input, image_width, image_height):
            input = input.replace("%width%", str(image_width))
            input = input.replace("%height%", str(image_height))
            return input

        filename_prefix = compute_vars(filename_prefix, image_width, image_height).replace("\\", "/")
        subfolder = posixpath.dirname(filename_prefix)
        filename = posixpath.basename(filename_prefix)
        
        full_output_folder_s3 = join_s3_key(self.output_dir, subfolder)
        
        # Check if the output folder exists, create it if it doesn't
        if full_output_folder_s3 and not self.does_folder_exist(full_output_folder_s3, self.output_bucket_name):
            self.create_folder(full_output_folder_s3, self.output_bucket_name)

        try:
            # Continue with the counter calculation
            files = self.get_files(full_output_folder_s3, self.output_bucket_name)
            counter = max(
                filter(
                    lambda a: a[1][:-1] == filename and a[1][-1] == "_",
                    map(map_filename, files)
                )
            )[0] + 1
        except (ValueError, KeyError):
            counter = 1
        
        return full_output_folder_s3, filename, counter, subfolder, filename_prefix


def get_s3_instance():
    try:
        s3_instance = S3(
            region=get_env_value("S3_REGION", default="auto"),
            access_key=get_env_value("S3_ACCESS_KEY", "S3_ACCESS_KEY_ID", "AWS_ACCESS_KEY_ID"),
            secret_key=get_env_value("S3_SECRET_KEY", "S3_SECRET_ACCESS_KEY", "AWS_SECRET_ACCESS_KEY"),
            bucket_name=get_env_value("S3_BUCKET_NAME", "S3_BUCKET", "S3_OUT_BUCKET_NAME", "S3_INPUT_BUCKET_NAME"),
            endpoint_url=get_env_value("S3_ENDPOINT_URL", "S3_ENDPOINT"),
            input_bucket_name=get_env_value("S3_INPUT_BUCKET_NAME", "S3_BUCKET_NAME", "S3_BUCKET", "S3_OUT_BUCKET_NAME"),
            output_bucket_name=get_env_value("S3_OUT_BUCKET_NAME", "S3_BUCKET_NAME", "S3_BUCKET", "S3_INPUT_BUCKET_NAME"),
            input_dir=get_env_value("S3_INPUT_DIR", "S3_INPUT_PREFIX"),
            output_dir=get_env_value("S3_OUTPUT_DIR", "S3_OUT_PREFIX", "S3_OUT_DIR", "S3_ASSETS_PREFIX"),
            public_url=get_env_value("S3_PUBLIC_URL")
        )
        return s3_instance
    except Exception as e:
        err = f"Failed to create S3 instance: {e} Please check your environment variables."
        logger.error(err)
