import json
import requests
from typing import Tuple

from ..logger import logger


class NextryWebhookSender:
    """
    Custom ComfyUI node for sending webhook notifications with image paths.
    This is an output node that sends a POST request to a specified endpoint.
    """
    
    def __init__(self):
        self.type = 'output'
        self.timeout = 30  # Timeout for webhook request in seconds

    @classmethod
    def INPUT_TYPES(cls):
        return {
            'required': {
                'endpoint': ('STRING', {
                    'default': 'http://localhost:8000/generation/comfy_webhook',
                    'multiline': False
                }),
                'preview_image': ('STRING', {
                    'default': '',
                    'multiline': False
                }),
                'stock_image': ('STRING', {
                    'default': '',
                    'multiline': False
                }),
            }
        }

    RETURN_TYPES = ('STRING',)
    RETURN_NAMES = ('webhook_response',)
    FUNCTION = 'send_webhook'
    OUTPUT_NODE = True
    CATEGORY = 'NEXTRY_ComfyS3'

    def send_webhook(self, endpoint: str, preview_image: str, stock_image: str) -> Tuple[dict]:
        """
        Send webhook POST request with image paths.
        
        Args:
            endpoint: The URL endpoint to send the webhook to
            preview_image: Path to the preview image
            stock_image: Path to the stock image
            
        Returns:
            Tuple containing the response data and UI information
        """
        logger.info(f'Preparing webhook request to: {endpoint}')
        logger.info(f'Preview image: {preview_image}')
        logger.info(f'Stock image: {stock_image}')

        # Prepare payload
        payload = {
            'preview_image': preview_image,
            'stock_image': stock_image
        }

        try:
            # Send POST request
            response = requests.post(
                endpoint,
                json=payload,
                headers={'Content-Type': 'application/json'},
                timeout=self.timeout
            )
            
            # Check if request was successful
            response.raise_for_status()
            
            # Try to parse JSON response
            try:
                response_data = response.json()
            except json.JSONDecodeError:
                response_data = {'text': response.text}

            logger.info(f'Webhook sent successfully. Status code: {response.status_code}')
            logger.info(f'Response: {response_data}')

            result = {
                'success': True,
                'status_code': response.status_code,
                'response': response_data
            }

            return {
                'ui': {
                    'webhook_result': [result]
                },
                'result': (json.dumps(result),)
            }

        except requests.exceptions.Timeout:
            error_msg = f'Webhook request timed out after {self.timeout} seconds'
            logger.error(error_msg)
            result = {
                'success': False,
                'error': 'timeout',
                'message': error_msg
            }
            return {
                'ui': {
                    'webhook_result': [result]
                },
                'result': (json.dumps(result),)
            }

        except requests.exceptions.RequestException as e:
            error_msg = f'Webhook request failed: {str(e)}'
            logger.error(error_msg)
            result = {
                'success': False,
                'error': 'request_failed',
                'message': error_msg
            }
            return {
                'ui': {
                    'webhook_result': [result]
                },
                'result': (json.dumps(result),)
            }

        except Exception as e:
            error_msg = f'Unexpected error: {str(e)}'
            logger.error(error_msg)
            result = {
                'success': False,
                'error': 'unknown',
                'message': error_msg
            }
            return {
                'ui': {
                    'webhook_result': [result]
                },
                'result': (json.dumps(result),)
            }

