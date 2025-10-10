"""
Test script for Nextry Webhook Sender Node

This script demonstrates how to test the webhook functionality.
"""
import sys
import os

# Add the src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from nodes.webhook_sender import NextryWebhookSender


def test_webhook_sender():
    """Test the webhook sender node"""
    
    # Create an instance of the webhook sender
    webhook_node = NextryWebhookSender()
    
    # Test parameters
    test_endpoint = 'http://localhost:8000/generation/comfy_webhook'
    test_preview = 's3://test-bucket/output/preview_test123.webp'
    test_stock = 's3://test-bucket/output/stock_test123.png'
    
    print('=' * 80)
    print('Testing Nextry Webhook Sender Node')
    print('=' * 80)
    print(f'\nEndpoint: {test_endpoint}')
    print(f'Preview Image: {test_preview}')
    print(f'Stock Image: {test_stock}')
    print('\nNote: This will fail if the endpoint is not available.')
    print('You can test with a mock server like httpbin.org or setup your own endpoint.\n')
    
    # Alternative test endpoint using httpbin (for testing)
    # Uncomment to test with httpbin
    # test_endpoint = 'https://httpbin.org/post'
    
    # Send the webhook
    result = webhook_node.send_webhook(
        endpoint=test_endpoint,
        preview_image=test_preview,
        stock_image=test_stock
    )
    
    print('\n' + '=' * 80)
    print('Result:')
    print('=' * 80)
    print(result)
    print('\n')


def test_with_httpbin():
    """Test with httpbin.org (online service for testing HTTP requests)"""
    
    webhook_node = NextryWebhookSender()
    
    test_endpoint = 'https://httpbin.org/post'
    test_preview = 's3://test-bucket/output/preview_httpbin.webp'
    test_stock = 's3://test-bucket/output/stock_httpbin.png'
    
    print('=' * 80)
    print('Testing with httpbin.org')
    print('=' * 80)
    
    result = webhook_node.send_webhook(
        endpoint=test_endpoint,
        preview_image=test_preview,
        stock_image=test_stock
    )
    
    print('\n' + '=' * 80)
    print('Result from httpbin.org:')
    print('=' * 80)
    print(result)
    print('\n')


if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Test Nextry Webhook Sender Node')
    parser.add_argument(
        '--httpbin',
        action='store_true',
        help='Test with httpbin.org instead of localhost'
    )
    
    args = parser.parse_args()
    
    if args.httpbin:
        test_with_httpbin()
    else:
        test_webhook_sender()

