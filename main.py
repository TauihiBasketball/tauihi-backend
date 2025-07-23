from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import httpx
import json
from datetime import datetime
from typing import Optional

app = FastAPI(title="Tauihi Basketball API", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Tauihi Basketball API", "status": "running"}

@app.get("/api/test")
async def test():
    return {
        "success": True,
        "message": "Tauihi Backend is working!",
        "timestamp": datetime.now().isoformat(),
        "endpoints": [
            "/api/teams?leagueId=1",
            "/api/games?competitionId=1",
            "/api/standings?competitionId=1"
        ]
    }

@app.get("/api/teams")
async def get_teams(leagueId: Optional[str] = "1"):
    try:
        # Genius Sports API configuration
        api_key = "4b1a43036f40c7762a694255636eab03"
        base_url = "https://api.wh.geniussports.com/v1/basketball"
        
        # Fetch teams from Genius Sports API
        url = f"{base_url}/leagues/{leagueId}/teams"
        
        async with httpx.AsyncClient() as client:
            response = await client.get(
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
        
        return {
            "success": True,
            "data": data.get("data", []),
            "cached": False,
            "timestamp": datetime.now().isoformat()
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
        
        return {
            "success": True,
            "data": mock_data["data"],
            "cached": True,
            "timestamp": datetime.now().isoformat(),
            "note": "Using mock data due to API error"
        }

@app.get("/api/games")
async def get_games(competitionId: Optional[str] = "1"):
    # Mock games data for now
    mock_games = {
        "data": [
            {
                "id": 1,
                "home_team": "Auckland Dream",
                "away_team": "Canterbury Wildcats",
                "date": "2024-02-15T19:30:00Z",
                "venue": "Auckland Arena",
                "status": "upcoming"
            },
            {
                "id": 2,
                "home_team": "Northern Mystics",
                "away_team": "Auckland Dream",
                "date": "2024-02-20T20:00:00Z",
                "venue": "North Shore Events Centre",
                "status": "upcoming"
            }
        ]
    }
    
    return {
        "success": True,
        "data": mock_games["data"],
        "cached": True,
        "timestamp": datetime.now().isoformat()
    }

@app.get("/api/standings")
async def get_standings(competitionId: Optional[str] = "1"):
    # Mock standings data
    mock_standings = {
        "data": [
            {
                "rank": 1,
                "team": "Auckland Dream",
                "wins": 5,
                "losses": 1,
                "percent": 0.833
            },
            {
                "rank": 2,
                "team": "Canterbury Wildcats",
                "wins": 4,
                "losses": 2,
                "percent": 0.667
            },
            {
                "rank": 3,
                "team": "Northern Mystics",
                "wins": 2,
                "losses": 4,
                "percent": 0.333
            }
        ]
    }
    
    return {
        "success": True,
        "data": mock_standings["data"],
        "cached": True,
        "timestamp": datetime.now().isoformat()
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 