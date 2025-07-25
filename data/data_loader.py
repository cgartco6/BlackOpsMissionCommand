from player_data import PlayerData
from config import PLAYER_DATA_FILE
import json

def load_player_data():
    """Load player data from the storage system"""
    data = PlayerData()
    data.load_data()
    return data

def export_player_data(format='json'):
    """Export player data in specified format"""
    data = PlayerData()
    data.load_data()
    
    if format == 'json':
        with open(PLAYER_DATA_FILE, 'r') as f:
            return json.load(f)
    elif format == 'csv':
        # Simple CSV conversion
        if not data.players:
            return ""
            
        headers = list(data.players[0].keys())
        csv = ",".join(headers) + "\n"
        
        for player in data.players:
            csv += ",".join(str(player[h]) for h in headers) + "\n"
            
        return csv
    else:
        return data.players

def get_player_analytics():
    """Get aggregated player analytics"""
    data = PlayerData()
    data.load_data()
    
    return {
        "activity": data.get_activity_data(),
        "financial": data.get_financial_data(),
        "geo_distribution": data.get_country_distribution(),
        "platform_distribution": data.get_platform_distribution(),
        "level_distribution": data.get_level_distribution()
    }

if __name__ == "__main__":
    # Test data export
    print("Exporting sample data...")
    json_data = export_player_data('json')
    print(f"JSON data contains {len(json_data)} records")
    
    csv_data = export_player_data('csv')
    print(f"CSV data contains {len(csv_data.splitlines())} lines")
    
    analytics = get_player_analytics()
    print("\nPlayer Analytics:")
    print(json.dumps(analytics, indent=2))
