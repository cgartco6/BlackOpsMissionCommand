import json
import os
import datetime
import random
import configparser
from .ads_manager import AdManager

class EconomySystem:
    def __init__(self, player_id):
        self.player_id = player_id
        self.data_file = f"data/player_data/{player_id}.json"
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')
        self.data = self.load_data()
        self.today = datetime.date.today().isoformat()
        self.ad_manager = AdManager()
        self.ad_set_completed = False
        
    def load_data(self):
        if not os.path.exists(self.data_file):
            return {
                "tokens": 3,  # 3 free games per day
                "last_played": None,
                "total_ads_watched": 0,
                "ads_watched_today": 0,
                "subscription_level": 0,
                "purchases": [],
                "total_spent": 0.0,
                "last_ad_set_time": None,
                "ad_sets_completed": 0
            }
        with open(self.data_file, 'r') as f:
            return json.load(f)
    
    def save_data(self):
        with open(self.data_file, 'w') as f:
            json.dump(self.data, f)
    
    def reset_daily_tokens(self):
        if self.data.get('last_played') != self.today:
            self.data['tokens'] = 3
            self.data['ads_watched_today'] = 0
            self.data['last_played'] = self.today
            self.save_data()
    
    def can_play(self):
        self.reset_daily_tokens()
        return self.data['tokens'] > 0
    
    def use_token(self):
        if self.data['tokens'] > 0:
            self.data['tokens'] -= 1
            self.save_data()
            return True
        return False
    
    def can_watch_ad_set(self):
        """Check if player can watch a new set of ads"""
        # Players can always watch ads if they're not subscribers
        if self.data.get('subscription_level', 0) > 0:
            return False
            
        # Check time between ad sets
        last_set_time = self.data.get('last_ad_set_time')
        min_interval = int(self.config.get('ADS', 'MIN_TIME_BETWEEN_SETS', fallback="60"))
        
        if not last_set_time:
            return True
            
        try:
            last_set = datetime.datetime.fromisoformat(last_set_time)
            return (datetime.datetime.now() - last_set).total_seconds() > min_interval
        except:
            return True
    
    def watch_ad_set(self):
        """Player watches a set of 3 ads to earn 3 tokens"""
        if not self.can_watch_ad_set():
            return False
        
        # Simulate watching 3 high-value ads
        total_revenue = 0
        for i in range(3):
            # Generate high-value ad impression ($100-$2200 eCPM)
            ad_revenue = self.ad_manager.show_ad()
            total_revenue += ad_revenue
            
            # Track ad metrics
            self.data['total_ads_watched'] = self.data.get('total_ads_watched', 0) + 1
            self.data['ads_watched_today'] = self.data.get('ads_watched_today', 0) + 1
            
            # Record revenue
            self.record_revenue("ad", ad_revenue, ad_index=i+1)
        
        # Award tokens
        self.data['tokens'] = self.data.get('tokens', 0) + 3
        self.data['ad_sets_completed'] = self.data.get('ad_sets_completed', 0) + 1
        self.data['last_ad_set_time'] = datetime.datetime.now().isoformat()
        self.save_data()
        
        return True
    
    def record_revenue(self, source, amount, ad_index=None):
        """Log revenue to transaction file"""
        transaction = {
            "player_id": self.player_id,
            "source": source,
            "amount": amount,
            "timestamp": datetime.datetime.now().isoformat(),
            "ad_index": ad_index
        }
        
        # Append to transaction log
        os.makedirs("data/transaction_logs", exist_ok=True)
        with open("data/transaction_logs/revenue.csv", "a") as f:
            f.write(f"{transaction['timestamp']},{transaction['player_id']},{transaction['source']},{transaction['amount']},{transaction.get('ad_index','')}\n")
        
        # Send to PayPal
        self.send_to_paypal(amount, source)
    
    def send_to_paypal(self, amount, source):
        """Simulate PayPal integration"""
        paypal_email = self.config.get('MONETIZATION', 'PAYPAL_EMAIL', fallback='your.paypal@email.com')
        # In real implementation, use PayPal API
        print(f"Revenue ${amount:.2f} from {source} sent to {paypal_email}")
