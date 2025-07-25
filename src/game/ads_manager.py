import random
import time

class AdManager:
    def __init__(self):
        self.ad_networks = {
            "premium_ads": {
                "min_cpm": 100,
                "max_cpm": 2200,
                "ad_types": ["rewarded"]
            }
        }
    
    def get_ad_value(self, player_value_score):
        """
        Calculate ad value based on player's engagement level
        Higher scores = higher value ads
        """
        min_cpm = 100
        max_cpm = 2200
        
        # Player score from 0-1 based on engagement metrics
        value_multiplier = min(1.0, max(0.1, player_value_score))
        
        # Exponential scaling - top 10% get max value
        if value_multiplier > 0.9:
            return max_cpm
        elif value_multiplier > 0.7:
            return min_cpm + (max_cpm - min_cpm) * (value_multiplier - 0.7) * 5
        else:
            return min_cpm + (max_cpm - min_cpm) * value_multiplier * 0.7
    
    def show_ad(self, player_value_score=0.5):
        """Show a premium ad with high CPM value"""
        network = "premium_ads"
        cpm = self.get_ad_value(player_value_score)
        revenue = cpm / 1000  # CPM to per-impression value
        
        # Simulate ad display
        print(f"Showing premium ad (CPM: ${cpm:.2f})")
        time.sleep(0.5)  # Simulate shorter ad duration for gameplay
        
        return revenue
