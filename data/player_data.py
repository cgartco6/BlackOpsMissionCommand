import json
import os
import random
from datetime import datetime, timedelta
from config import DATA_DIR

class PlayerData:
    def __init__(self):
        self.players = []
        self.data_file = os.path.join(DATA_DIR, "player_data.json")
        self._ensure_data_directory()
        
    def _ensure_data_directory(self):
        """Create data directory if it doesn't exist"""
        if not os.path.exists(DATA_DIR):
            os.makedirs(DATA_DIR)
        
    def generate_sample_data(self, num_players=10000):
        """Generate realistic sample player data"""
        print(f"Generating sample data for {num_players} players...")
        self.players = []
        
        # Common player names
        first_names = ["John", "Sarah", "Mike", "Alex", "Chris", "Jessica", "David", "Emily", "James", "Jennifer"]
        last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Miller", "Davis", "Garcia", "Wilson", "Martinez"]
        
        # Game-related data ranges
        levels = list(range(1, 101))
        countries = ["US", "UK", "CA", "AU", "DE", "FR", "JP", "KR", "BR", "RU", "IN", "CN"]
        platforms = ["PC", "PS5", "Xbox Series X", "Switch", "Mobile"]
        
        for player_id in range(1, num_players + 1):
            # Basic info
            first = random.choice(first_names)
            last = random.choice(last_names)
            name = f"{first} {last}"
            email = f"{first.lower()}.{last.lower()}{player_id}@example.com"
            
            # Game stats
            level = random.choices(levels, weights=[10]*10 + [8]*10 + [6]*20 + [4]*30 + [2]*30)[0]
            playtime = random.randint(10, 1000)  # hours
            sessions = random.randint(1, 500)
            avg_session = random.randint(15, 120)  # minutes
            last_login = datetime.now() - timedelta(days=random.randint(0, 30))
            
            # Combat stats
            kills = random.randint(0, 5000)
            deaths = random.randint(0, 3000)
            kd_ratio = kills / max(1, deaths)
            headshots = random.randint(0, kills)
            
            # Progression
            missions_completed = random.randint(0, 100)
            win_rate = random.uniform(0.3, 0.8)
            
            # Financial
            total_spent = random.choices([0, 5, 20, 50, 100, 200], weights=[40, 30, 15, 8, 5, 2])[0]
            
            player = {
                "player_id": player_id,
                "name": name,
                "email": email,
                "country": random.choice(countries),
                "platform": random.choice(platforms),
                "level": level,
                "playtime_hours": playtime,
                "sessions": sessions,
                "avg_session_min": avg_session,
                "last_login": last_login.isoformat(),
                "kills": kills,
                "deaths": deaths,
                "kd_ratio": round(kd_ratio, 2),
                "headshots": headshots,
                "headshot_percent": round(headshots / max(1, kills) * 100, 1),
                "missions_completed": missions_completed,
                "win_rate": round(win_rate, 2),
                "total_spent": total_spent,
                "premium": total_spent > 50,
                "churn_risk": random.choices(["Low", "Medium", "High"], weights=[70, 20, 10])[0]
            }
            self.players.append(player)
        
        self.save_data()
        print(f"Generated {len(self.players)} player records")
    
    def load_data(self):
        """Load player data from JSON file"""
        if not os.path.exists(self.data_file):
            self.generate_sample_data()
            return
        
        try:
            with open(self.data_file, 'r') as f:
                self.players = json.load(f)
            print(f"Loaded {len(self.players)} player records")
        except Exception as e:
            print(f"Error loading player data: {e}")
            self.generate_sample_data()
    
    def save_data(self):
        """Save player data to JSON file"""
        try:
            with open(self.data_file, 'w') as f:
                json.dump(self.players, f, indent=2)
            print(f"Saved {len(self.players)} player records")
        except Exception as e:
            print(f"Error saving player data: {e}")
    
    def get_all_players(self):
        """Get all player records"""
        return self.players
    
    def get_player(self, player_id):
        """Get a specific player by ID"""
        for player in self.players:
            if player['player_id'] == player_id:
                return player
        return None
    
    def update_player(self, player_id, updates):
        """Update a player record"""
        for i, player in enumerate(self.players):
            if player['player_id'] == player_id:
                self.players[i].update(updates)
                self.save_data()
                return True
        return False
    
    def get_player_count(self):
        """Get total player count"""
        return len(self.players)
    
    def get_premium_count(self):
        """Count premium players (spent > $50)"""
        return sum(1 for p in self.players if p['premium'])
    
    def get_country_distribution(self):
        """Get player distribution by country"""
        countries = {}
        for player in self.players:
            country = player['country']
            countries[country] = countries.get(country, 0) + 1
        return countries
    
    def get_platform_distribution(self):
        """Get player distribution by platform"""
        platforms = {}
        for player in self.players:
            platform = player['platform']
            platforms[platform] = platforms.get(platform, 0) + 1
        return platforms
    
    def get_level_distribution(self):
        """Get player distribution by level groups"""
        distribution = {
            "1-10": 0,
            "11-20": 0,
            "21-30": 0,
            "31-40": 0,
            "41-50": 0,
            "51+": 0
        }
        
        for player in self.players:
            level = player['level']
            if level <= 10:
                distribution["1-10"] += 1
            elif level <= 20:
                distribution["11-20"] += 1
            elif level <= 30:
                distribution["21-30"] += 1
            elif level <= 40:
                distribution["31-40"] += 1
            elif level <= 50:
                distribution["41-50"] += 1
            else:
                distribution["51+"] += 1
                
        return distribution
    
    def get_activity_data(self):
        """Get player activity metrics"""
        # Players active in last 7 days
        active_players = 0
        for player in self.players:
            last_login = datetime.fromisoformat(player['last_login'])
            if (datetime.now() - last_login).days <= 7:
                active_players += 1
        
        return {
            "total_players": len(self.players),
            "active_players": active_players,
            "avg_session": sum(p['avg_session_min'] for p in self.players) // len(self.players),
            "avg_playtime": sum(p['playtime_hours'] for p in self.players) // len(self.players),
            "premium_percent": round(self.get_premium_count() / len(self.players) * 100, 1)
        }
    
    def get_financial_data(self):
        """Get financial metrics"""
        total_revenue = sum(p['total_spent'] for p in self.players)
        premium_count = self.get_premium_count()
        
        return {
            "total_revenue": total_revenue,
            "arpu": round(total_revenue / len(self.players), 2),
            "arppu": round(total_revenue / max(1, premium_count), 2),
            "premium_count": premium_count
        }
    
    def get_top_players(self, metric='level', count=10):
        """Get top players by specified metric"""
        valid_metrics = ['level', 'kills', 'playtime_hours', 'missions_completed', 'kd_ratio']
        if metric not in valid_metrics:
            metric = 'level'
            
        return sorted(
            self.players, 
            key=lambda x: x[metric], 
            reverse=True
        )[:count]

if __name__ == "__main__":
    # Test data generation
    data = PlayerData()
    data.load_data()
    print(f"Total players: {data.get_player_count()}")
    print(f"Premium players: {data.get_premium_count()}")
    print(f"Activity data: {data.get_activity_data()}")
    print(f"Financial data: {data.get_financial_data()}")
    
    # Print top 5 players by level
    print("\nTop 5 players by level:")
    for player in data.get_top_players('level', 5):
        print(f"{player['name']} (Level {player['level']})")
