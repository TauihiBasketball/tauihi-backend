from http.server import BaseHTTPRequestHandler
import json
import os
import httpx
from typing import Dict, Any

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
            from urllib.parse import urlparse, parse_qs
            parsed_url = urlparse(self.path)
            params = parse_qs(parsed_url.query)
            league_id = params.get('leagueId', [1])[0]  # Default to 1
            
            # Call Genius Sports API
            api_key = os.environ.get('GENIUS_SPORTS_API_KEY')
            base_url = os.environ.get('GENIUS_SPORTS_BASE_URL')
            
            url = f"{base_url}/teams?leagueId={league_id}"
            headers = {
                "x-api-key": api_key,
                "Content-Type": "application/json",
                "Accept": "application/json"
            }
            
            with httpx.Client() as client:
                response = client.get(url, headers=headers)
                response.raise_for_status()
                
                data = response.json()
                
                # Transform to our format
                result = {
                    "success": True,
                    "data": data.get("data", []),
                    "error": None,
                    "timestamp": "2024-01-01T00:00:00Z",
                    "cached": False
                }
                
                self.wfile.write(json.dumps(result).encode())
                
        except Exception as e:
            error_response = {
                "success": False,
                "data": None,
                "error": str(e),
                "timestamp": "2024-01-01T00:00:00Z",
                "cached": False
            }
            self.wfile.write(json.dumps(error_response).encode())
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers() 