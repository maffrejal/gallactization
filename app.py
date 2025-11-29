from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os
import uuid
from datetime import datetime, timedelta
import bcrypt
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional

app = Flask(__name__)
CORS(app)

# Data classes
@dataclass
class Resources:
    wood: float = 0
    clay: float = 0
    iron: float = 0
    wheat: float = 0

@dataclass
class ResourceProduction:
    wood: float = 0
    clay: float = 0
    iron: float = 0
    wheat: float = 0

@dataclass 
class ResourceStorage:
    wood: float = 1000
    clay: float = 1000
    iron: float = 1000
    wheat: float = 1000

class BuildingType:
    MAIN_BUILDING = "main_building"
    WOODCUTTER = "woodcutter" 
    CLAY_PIT = "clay_pit"
    IRON_MINE = "iron_mine"
    CROPLAND = "cropland"
    WAREHOUSE = "warehouse"
    GRANARY = "granary"

@dataclass
class Building:
    id: str
    type: str
    level: int = 0

class Village:
    def __init__(self, id=None, name="New Village", player_id=None, x=0, y=0):
        self.id = id or str(uuid.uuid4())
        self.name = name
        self.player_id = player_id
        self.x = x
        self.y = y
        self.resources = Resources(750, 750, 750, 750)
        self.production = ResourceProduction()
        self.storage = ResourceStorage()
        self.buildings: List[Building] = []
        self.last_updated = datetime.utcnow()
        
        self._initialize_buildings()
        self._update_production()
    
    def _initialize_buildings(self):
        initial_buildings = [
            BuildingType.MAIN_BUILDING,
            BuildingType.WOODCUTTER,
            BuildingType.CLAY_PIT, 
            BuildingType.IRON_MINE,
            BuildingType.CROPLAND,
            BuildingType.WAREHOUSE,
            BuildingType.GRANARY
        ]
        
        for building_type in initial_buildings:
            self.buildings.append(Building(
                id=str(uuid.uuid4()),
                type=building_type,
                level=1
            ))
    
    def _update_production(self):
        self.production = ResourceProduction()
        for building in self.buildings:
            if building.type == BuildingType.WOODCUTTER:
                self.production.wood = building.level * 5
            elif building.type == BuildingType.CLAY_PIT:
                self.production.clay = building.level * 5
            elif building.type == BuildingType.IRON_MINE:
                self.production.iron = building.level * 5
            elif building.type == BuildingType.CROPLAND:
                self.production.wheat = building.level * 5
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "player_id": self.player_id,
            "x": self.x,
            "y": self.y,
            "resources": asdict(self.resources),
            "production": asdict(self.production),
            "storage": asdict(self.storage),
            "buildings": [{"id": b.id, "type": b.type, "level": b.level} for b in self.buildings],
            "last_updated": self.last_updated.isoformat()
        }

class Player:
    def __init__(self, id=None, username="", email=""):
        self.id = id or str(uuid.uuid4())
        self.username = username
        self.email = email
        self.created_at = datetime.utcnow()
        self.last_active = datetime.utcnow()
        self.password_hash = ""
        self.villages: List[Village] = []
    
    def set_password(self, password):
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))
    
    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "created_at": self.created_at.isoformat(),
            "last_active": self.last_active.isoformat(),
            "villages": [v.to_dict() for v in self.villages]
        }

# Simple storage
players_db = {}
villages_db = {}

# API Routes
@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        "status": "healthy", 
        "message": "VillageRPG API is running!",
        "timestamp": datetime.utcnow().isoformat(),
        "players_count": len(players_db),
        "villages_count": len(villages_db)
    })

@app.route('/api/auth/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
        
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        
        if not username or not email or not password:
            return jsonify({"error": "Missing required fields"}), 400
        
        if username in players_db:
            return jsonify({"error": "Username already exists"}), 400
        
        player = Player(username=username, email=email)
        player.set_password(password)
        players_db[username] = player
        
        return jsonify({
            "id": player.id,
            "username": player.username,
            "email": player.email,
            "message": "Player registered successfully"
        }), 201
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/auth/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        
        player = players_db.get(username)
        if not player or not player.check_password(password):
            return jsonify({"error": "Invalid credentials"}), 401
        
        player.last_active = datetime.utcnow()
        
        return jsonify({
            "id": player.id,
            "username": player.username,
            "email": player.email,
            "villages": [v.to_dict() for v in player.villages]
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/villages', methods=['POST'])
def create_village():
    try:
        data = request.get_json()
        player_id = data.get('player_id')
        name = data.get('name', 'My Village')
        x = data.get('x', 0)
        y = data.get('y', 0)
        
        # Find player
        player = None
        for p in players_db.values():
            if p.id == player_id:
                player = p
                break
        
        if not player:
            return jsonify({"error": "Player not found"}), 404
        
        village = Village(name=name, player_id=player_id, x=x, y=y)
        villages_db[village.id] = village
        player.villages.append(village)
        
        return jsonify(village.to_dict()), 201
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/villages/<village_id>', methods=['GET'])
def get_village(village_id):
    village = villages_db.get(village_id)
    if not village:
        return jsonify({"error": "Village not found"}), 404
    
    return jsonify(village.to_dict())

@app.route('/api/buildings/types', methods=['GET'])
def get_building_types():
    building_types = [
        {
            "type": BuildingType.MAIN_BUILDING,
            "name": "Main Building",
            "description": "The heart of your village"
        },
        {
            "type": BuildingType.WOODCUTTER,
            "name": "Woodcutter", 
            "description": "Produces wood for your village"
        },
        {
            "type": BuildingType.CLAY_PIT,
            "name": "Clay Pit",
            "description": "Produces clay for your village"
        },
        {
            "type": BuildingType.IRON_MINE,
            "name": "Iron Mine",
            "description": "Produces iron for your village" 
        },
        {
            "type": BuildingType.CROPLAND,
            "name": "Cropland",
            "description": "Produces wheat for your village"
        }
    ]
    
    return jsonify(building_types)

@app.route('/')
def home():
    return """
    <h1>🚀 VillageRPG - Flask Edition</h1>
    <p>Your game server is running successfully!</p>
    <h3>Test Endpoints:</h3>
    <ul>
        <li><a href="/api/health">/api/health</a> - Health check</li>
        <li><a href="/api/buildings/types">/api/buildings/types</a> - Building types</li>
    </ul>
    <h3>POST Endpoints (use Postman or curl):</h3>
    <ul>
        <li><code>/api/auth/register</code> - Register player</li>
        <li><code>/api/auth/login</code> - Login player</li>
        <li><code>/api/villages</code> - Create village</li>
    </ul>
    """

if __name__ == '__main__':
    print("🎮 VillageRPG Flask Server Starting...")
    print("📍 Visit: http://localhost:5000")
    print("🔧 API Health: http://localhost:5000/api/health")
    print("🐛 Debug mode: ON")
    app.run(debug=True, host='0.0.0.0', port=5000)