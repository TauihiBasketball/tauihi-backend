from http.server import BaseHTTPRequestHandler
import json
import httpx
from urllib.parse import urlparse, parse_qs

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Set CORS headers
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        
        try:
            # Get query parameters
            parsed_url = urlparse(self.path)
            params = parse_qs(parsed_url.query)
            league_id = params.get('leagueId', ['1'])[0]  # Default to 1
            
            # Genius Sports API configuration
            api_key = "4b1a43036f40c7762a694255636eab03"
            base_url = "https://api.wh.geniussports.com/v1/basketball"
            
            # Fetch teams from Genius Sports API
            url = f"{base_url}/leagues/{league_id}/teams"
            
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
            
            self.wfile.write(json.dumps(result).encode())
            
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
            
            self.wfile.write(json.dumps(result).encode())
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers() 