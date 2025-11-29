import requests
import json

BASE_URL = "http://localhost:5000/api"

def test_game():
    print("Testing VillageRPG API...")
    
    # Test health check
    response = requests.get(f"{BASE_URL}/health")
    print(f"Health check: {response.status_code} - {response.json()}")
    
    # Register a new player
    register_data = {
        "username": "testplayer",
        "email": "test@example.com", 
        "password": "test123"
    }
    
    response = requests.post(f"{BASE_URL}/auth/register", json=register_data)
    if response.status_code == 201:
        print("✅ Player registered successfully")
        player_data = response.json()
        player_id = player_data['id']
        print(f"Player ID: {player_id}")
    else:
        print(f"❌ Registration failed: {response.json()}")
        # Try login instead
        response = requests.post(f"{BASE_URL}/auth/login", json=register_data)
        if response.status_code == 200:
            player_data = response.json()
            player_id = player_data['id']
            print("✅ Player logged in successfully")
        else:
            print("❌ Both registration and login failed")
            return
    
    # Create a village
    village_data = {
        "player_id": player_id,
        "name": "Test Village",
        "x": 10,
        "y": 10
    }
    
    response = requests.post(f"{BASE_URL}/villages", json=village_data)
    if response.status_code == 201:
        village_data = response.json()
        village_id = village_data['id']
        print(f"✅ Village created: {village_id}")
    else:
        print(f"❌ Village creation failed: {response.json()}")
        return
    
    # Get village details
    response = requests.get(f"{BASE_URL}/villages/{village_id}")
    if response.status_code == 200:
        village = response.json()
        print(f"✅ Village loaded: {village['name']}")
        print(f"Resources: Wood={village['resources']['wood']}, Clay={village['resources']['clay']}")
    else:
        print(f"❌ Failed to get village: {response.json()}")
    
    # Get production info
    response = requests.get(f"{BASE_URL}/buildings/village/{village_id}/production")
    if response.status_code == 200:
        production = response.json()
        print("✅ Production info:")
        print(f"Total Production: Wood={production['total_production']['wood']}/hour")
        print(f"Current Resources: Wood={production['current_resources']['wood']}")
    else:
        print(f"❌ Failed to get production: {response.json()}")
    
    # Get building types
    response = requests.get(f"{BASE_URL}/buildings/types")
    if response.status_code == 200:
        buildings = response.json()
        print(f"✅ Available buildings: {len(buildings)}")
        for building in buildings[:3]:  # Show first 3
            print(f"  - {building['name']}: {building['description']}")
    else:
        print(f"❌ Failed to get building types: {response.json()}")

if __name__ == "__main__":
    test_game()