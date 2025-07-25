import random
import json
import os
from datetime import datetime

class ContentAgent:
    def __init__(self):
        self.status = "idle"
        self.last_run = None
        self.generated_content = []
        
    def generate_new_content(self):
        """Generate new game content"""
        self.status = "generating"
        self.last_run = datetime.now()
        
        try:
            # Generate new missions
            new_missions = self.generate_missions()
            
            # Save content
            self.save_content(new_missions)
            
            self.status = "success"
            return True
        except Exception as e:
            print(f"Content generation error: {e}")
            self.status = f"error: {str(e)}"
            return False
            
    def generate_missions(self, count=2):
        """Generate new missions"""
        themes = [
            "Cyber Heist", "Desert Ambush", "Underwater Facility",
            "Space Station", "AI Core Breach"
        ]
        
        locations = [
            "Neo-Tokyo", "Sahara Desert", "Mariana Trench",
            "Low Earth Orbit", "Quantum Computing Facility"
        ]
        
        missions = []
        for i in range(count):
            name = f"Operation: {random.choice(themes)}"
            description = f"A high-stakes mission to {random.choice(['retrieve', 'destroy', 'rescue'])} in {random.choice(locations)}"
            location = random.choice(locations)
            difficulty = random.randint(3, 5)
            
            missions.append({
                "name": name,
                "description": description,
                "location": location,
                "difficulty": difficulty
            })
            
        return missions
        
    def save_content(self, missions):
        """Save generated content"""
        os.makedirs("data/generated", exist_ok=True)
        with open("data/generated/missions.json", "a") as f:
            for mission in missions:
                f.write(json.dumps(mission) + "\n")
        
        # Track generation
        self.generated_content.append({
            "missions": len(missions),
            "timestamp": datetime.now().isoformat()
        })
        
    def get_status(self):
        return {
            "status": self.status,
            "last_run": self.last_run.isoformat() if self.last_run else None,
            "total_generated": len(self.generated_content)
        }
