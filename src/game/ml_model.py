import random
import json
import os
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import numpy as np

class AdaptiveGameAI:
    def __init__(self):
        self.model_file = "data/models/player_behavior_model.pkl"
        self.model = self.load_model()
        self.player_data = []
        
    def load_model(self):
        if os.path.exists(self.model_file):
            return joblib.load(self.model_file)
        return None
    
    def collect_data(self, player_id, action, success, difficulty):
        """Collect player behavior data for ML training"""
        self.player_data.append({
            "player_id": player_id,
            "action": action,
            "success": int(success),
            "difficulty": difficulty,
            "timestamp": datetime.datetime.now().isoformat()
        })
        
        # Save periodically
        if len(self.player_data) % 10 == 0:
            self.save_data()
    
    def save_data(self):
        os.makedirs("data/player_data/ml", exist_ok=True)
        with open("data/player_data/ml_dataset.json", "a") as f:
            for entry in self.player_data:
                f.write(json.dumps(entry) + "\n")
        self.player_data = []
    
    def train_model(self):
        """Train model to predict player success based on actions"""
        # Load dataset
        try:
            with open("data/player_data/ml_dataset.json", "r") as f:
                data = [json.loads(line) for line in f]
        except FileNotFoundError:
            return  # No data yet
        
        # Prepare features and labels
        X = np.array([[d['action'], d['difficulty']] for d in data])
        y = np.array([d['success'] for d in data])
        
        # Train-test split
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        # Train model
        model = RandomForestClassifier(n_estimators=100)
        model.fit(X_train, y_train)
        
        # Save model
        os.makedirs("data/models", exist_ok=True)
        joblib.dump(model, self.model_file)
        self.model = model
    
    def adjust_difficulty(self, player_id, current_difficulty):
        """Adjust game difficulty based on player performance"""
        if not self.model:
            return current_difficulty
        
        # Predict player success probability
        proba = self.model.predict_proba([[player_id, current_difficulty]])[0][1]
        
        # Make game easier if player is struggling
        if proba < 0.3:
            return max(1, current_difficulty - 1)
        # Make game harder if player is doing well
        elif proba > 0.7:
            return min(10, current_difficulty + 1)
        return current_difficulty
    
    def generate_addictive_content(self, player_id):
        """Generate content to keep player engaged"""
        # In a real implementation, this would use player behavior data
        # to create personalized addictive content
        addictive_elements = [
            "special_event", "limited_time_offer", "new_challenge",
            "leaderboard_update", "personalized_reward"
        ]
        return random.choice(addictive_elements)
