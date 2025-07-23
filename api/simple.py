import json
from datetime import datetime

def handler(event, context):
    """Simple test function without external dependencies"""
    
    headers = {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type'
    }
    
    if event['httpMethod'] == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': headers,
            'body': ''
        }
    
    result = {
        "success": True,
        "message": "Simple Python function working!",
        "timestamp": datetime.now().isoformat(),
        "method": event['httpMethod'],
        "path": event['path']
    }
    
    return {
        'statusCode': 200,
        'headers': headers,
        'body': json.dumps(result)
    } 