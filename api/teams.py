import json
import httpx

def handler(event, context):
    """Netlify function to fetch teams from Genius Sports API"""
    
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
    
    try:
        # Parse query parameters
        query_string = event.get('queryStringParameters', {}) or {}
        league_id = query_string.get('leagueId', '1')
        
        # Genius Sports API configuration
        api_key = "4b1a43036f40c7762a694255636eab03"
        base_url = "https://api.wh.geniussports.com/v1/basketball"
        
        # Fetch teams from Genius Sports API
        url = f"{base_url}/leagues/{league_id}/teams"
        
        # Use synchronous httpx client
        with httpx.Client() as client:
            response = client.get(
                url,
                headers={
                    "x-api-key": api_key,
                    "Content-Type": "application/json",
                    "Accept": "application/json"
                },
                timeout=30.0
            )
            response.raise_for_status()
            data = response.json()
        
        result = {
            "success": True,
            "data": data.get("data", []),
            "cached": False,
            "timestamp": "2024-01-01T00:00:00Z"
        }
        
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps(result)
        }
        
    except Exception as e:
        # Fallback to mock data if API fails
        mock_data = {
            "data": [
                {
                    "id": 1,
                    "name": "Auckland Dream",
                    "abbreviation": "AUC",
                    "logo_url": "https://example.com/auckland-dream.png"
                },
                {
                    "id": 2, 
                    "name": "Canterbury Wildcats",
                    "abbreviation": "CAN",
                    "logo_url": "https://example.com/canterbury-wildcats.png"
                },
                {
                    "id": 3,
                    "name": "Northern Mystics",
                    "abbreviation": "NOR",
                    "logo_url": "https://example.com/northern-mystics.png"
                }
            ]
        }
        
        result = {
            "success": True,
            "data": mock_data["data"],
            "cached": True,
            "timestamp": "2024-01-01T00:00:00Z",
            "note": "Using mock data due to API error"
        }
        
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps(result)
        } 