import os
import json
import datetime
import socket
import configparser
import random

class Analytics:
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')
        self.geoip_enabled = self.config.getboolean('ANALYTICS', 'TRACKING_ENABLED', fallback=True)
    
    def track_player(self, player_id, action):
        """Track player actions with geolocation"""
        # Get player location
        ip = self.get_public_ip()
        location = self.get_location(ip) if self.geoip_enabled else {}
        
        # Create log entry
        entry = {
            "player_id": player_id,
            "action": action,
            "timestamp": datetime.datetime.now().isoformat(),
            "ip": ip,
            "country": location.get('country', 'Unknown'),
            "region": location.get('region', 'Unknown'),
            "city": location.get('city', 'Unknown')
        }
        
        # Save to player log
        self.save_entry(entry)
    
    def track_ad_revenue(self, amount):
        """Track ad revenue"""
        entry = {
            "type": "ad_revenue",
            "amount": amount,
            "timestamp": datetime.datetime.now().isoformat()
        }
        self.save_entry(entry, "revenue")
    
    def get_public_ip(self):
        """Get public IP address (simulated)"""
        # In a real game, this would get the player's public IP
        return ".".join(str(random.randint(0, 255)) for _ in range(4))
    
    def get_location(self, ip):
        """Get location from IP address (simulated)"""
        # In a real implementation, use geoip2 database
        countries = ["United States", "United Kingdom", "Canada", "Australia", "Germany", "Japan"]
        regions = ["California", "Texas", "London", "Ontario", "New South Wales", "Bavaria", "Tokyo"]
        cities = ["Los Angeles", "Houston", "London", "Toronto", "Sydney", "Munich", "Tokyo"]
        
        return {
            "country": random.choice(countries),
            "region": random.choice(regions),
            "city": random.choice(cities)
        }
    
    def save_entry(self, entry, log_type="player"):
        """Save analytics entry to appropriate log"""
        os.makedirs("data/analytics", exist_ok=True)
        log_file = f"data/analytics/{log_type}_log.json"
        with open(log_file, "a") as f:
            f.write(json.dumps(entry) + "\n")
