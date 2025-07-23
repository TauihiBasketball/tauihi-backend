import json
from datetime import datetime

def handler(event, context):
    """Netlify function handler"""
    
    # Set CORS headers
    headers = {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type'
    }
    
    # Handle OPTIONS request for CORS
    if event['httpMethod'] == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': headers,
            'body': ''
        }
    
    # Simple test response
    result = {
        "success": True,
        "message": "Tauihi Backend is working on Netlify!",
        "timestamp": datetime.now().isoformat(),
        "endpoints": [
            "/api/teams?leagueId=1",
            "/api/games?competitionId=1", 
            "/api/standings?competitionId=1"
        ]
    }
    
    return {
        'statusCode': 200,
        'headers': headers,
        'body': json.dumps(result)
    } 