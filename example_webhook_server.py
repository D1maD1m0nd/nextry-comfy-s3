"""
Example Flask server for testing webhook notifications from ComfyUI.

This is a simple server that receives webhook POST requests
from the Nextry Webhook Sender node.

Usage:
    pip install flask
    python example_webhook_server.py

Then configure your ComfyUI webhook node to use:
    http://localhost:8000/generation/comfy_webhook
"""
from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

# Store received webhooks for inspection
webhook_history = []


@app.route('/generation/comfy_webhook', methods=['POST'])
def comfy_webhook():
    """
    Endpoint that receives webhook notifications from ComfyUI.
    
    Expected JSON payload:
    {
        "preview_image": "s3://bucket/path/to/preview.webp",
        "stock_image": "s3://bucket/path/to/stock.png"
    }
    """
    try:
        # Get JSON data from request
        data = request.json
        
        if not data:
            return jsonify({
                'status': 'error',
                'message': 'No JSON data provided'
            }), 400
        
        # Extract image paths
        preview_image = data.get('preview_image')
        stock_image = data.get('stock_image')
        
        # Validate required fields
        if not preview_image or not stock_image:
            return jsonify({
                'status': 'error',
                'message': 'Missing required fields: preview_image and stock_image'
            }), 400
        
        # Create webhook record
        webhook_record = {
            'timestamp': datetime.now().isoformat(),
            'preview_image': preview_image,
            'stock_image': stock_image,
            'ip_address': request.remote_addr
        }
        
        # Store in history
        webhook_history.append(webhook_record)
        
        # Log to console
        print('\n' + '=' * 80)
        print('🎨 New ComfyUI Webhook Received!')
        print('=' * 80)
        print(f'Timestamp: {webhook_record["timestamp"]}')
        print(f'IP Address: {webhook_record["ip_address"]}')
        print(f'Preview Image: {preview_image}')
        print(f'Stock Image: {stock_image}')
        print('=' * 80 + '\n')
        
        # Here you can add your custom logic:
        # - Download images from S3
        # - Process images
        # - Store in database
        # - Trigger other workflows
        # - Send notifications
        # etc.
        
        # Return success response
        return jsonify({
            'status': 'success',
            'message': 'Webhook received successfully',
            'data': {
                'preview_image': preview_image,
                'stock_image': stock_image,
                'received_at': webhook_record['timestamp']
            }
        }), 200
        
    except Exception as e:
        print(f'❌ Error processing webhook: {str(e)}')
        return jsonify({
            'status': 'error',
            'message': f'Server error: {str(e)}'
        }), 500


@app.route('/webhooks/history', methods=['GET'])
def get_webhook_history():
    """
    Get the history of received webhooks.
    """
    return jsonify({
        'total': len(webhook_history),
        'webhooks': webhook_history
    })


@app.route('/webhooks/clear', methods=['POST'])
def clear_webhook_history():
    """
    Clear the webhook history.
    """
    global webhook_history
    webhook_history = []
    return jsonify({
        'status': 'success',
        'message': 'Webhook history cleared'
    })


@app.route('/health', methods=['GET'])
def health_check():
    """
    Health check endpoint.
    """
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'total_webhooks_received': len(webhook_history)
    })


@app.route('/', methods=['GET'])
def index():
    """
    Root endpoint with information about the server.
    """
    return jsonify({
        'name': 'ComfyUI Webhook Test Server',
        'version': '1.0.0',
        'endpoints': {
            'webhook': 'POST /generation/comfy_webhook',
            'history': 'GET /webhooks/history',
            'clear': 'POST /webhooks/clear',
            'health': 'GET /health'
        },
        'usage': 'Configure your ComfyUI webhook node to use: http://localhost:8000/generation/comfy_webhook'
    })


if __name__ == '__main__':
    print('\n' + '=' * 80)
    print('🚀 ComfyUI Webhook Test Server')
    print('=' * 80)
    print('Server starting on http://localhost:8000')
    print('\nAvailable endpoints:')
    print('  • POST   http://localhost:8000/generation/comfy_webhook  - Receive webhooks')
    print('  • GET    http://localhost:8000/webhooks/history          - View webhook history')
    print('  • POST   http://localhost:8000/webhooks/clear            - Clear history')
    print('  • GET    http://localhost:8000/health                    - Health check')
    print('\nConfigure your ComfyUI webhook node with:')
    print('  Endpoint: http://localhost:8000/generation/comfy_webhook')
    print('=' * 80 + '\n')
    
    # Run the Flask app
    app.run(
        host='0.0.0.0',
        port=8000,
        debug=True
    )

