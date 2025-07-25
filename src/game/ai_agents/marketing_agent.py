import random
import requests
import time
import os
import json
import subprocess
from datetime import datetime
from configparser import ConfigParser
import moviepy.editor as mpe
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import sys
import platform

# Constants
ACCENT = (0, 150, 200)
WHITE = (240, 240, 240)
SCREEN_WIDTH, SCREEN_HEIGHT = 1000, 700

class MarketingAgent:
    def __init__(self):
        self.config = ConfigParser()
        self.config.read('config.ini')
        self.last_run = None
        self.status = "idle"
        self.campaigns = []
        self.player_targets = {
            1: 1000,   # Month 1 target
            2: 5000,   # Month 2 target
            3: 20000,  # Month 3 target
            6: 100000  # Month 6 target
        }
        
        # Ensure marketing directories exist
        os.makedirs("data/marketing/videos", exist_ok=True)
        os.makedirs("data/marketing/images", exist_ok=True)
        os.makedirs("data/marketing/audio", exist_ok=True)
        os.makedirs("data/marketing/campaigns", exist_ok=True)
        
        # Set launch date if not exists
        if not self.config.has_option('LAUNCH', 'DATE'):
            self.config.set('LAUNCH', 'DATE', datetime.now().isoformat())
            with open('config.ini', 'w') as configfile:
                self.config.write(configfile)
    
    def execute_campaign(self, intensity=None):
        """Execute a multimedia marketing campaign"""
        self.status = "running"
        self.last_run = datetime.now()
        
        try:
            # Check player growth progress
            current_players = self.get_current_players()
            launch_date = datetime.fromisoformat(self.config.get('LAUNCH', 'DATE'))
            month = (datetime.now() - launch_date).days // 30 + 1
            target = self.player_targets.get(month, 100000)
            
            # Adjust campaign intensity based on progress if not provided
            if intensity is None:
                intensity = self.calculate_intensity(current_players, target)
            
            # Generate multimedia content
            content = self.generate_multimedia_content(intensity)
            
            # Post to all social platforms
            platforms = self.get_active_platforms()
            for platform in platforms:
                self.post_to_platform(platform, content, intensity)
                
            # Track campaign performance
            new_players = self.track_campaign(content, intensity)
            
            # Adjust strategy if behind target
            if new_players < (target - current_players) / max(1, (30 - datetime.now().day)):
                self.boost_campaign(intensity)
            
            self.status = "success"
            return True
        except Exception as e:
            print(f"Marketing error: {e}")
            self.status = f"error: {str(e)}"
            return False
            
    def calculate_intensity(self, current_players, target):
        """Determine campaign intensity based on player growth progress"""
        if target == 0:
            return "medium"
        progress = current_players / target
        if progress < 0.5:
            return "high"  # Behind target
        elif progress < 0.8:
            return "medium"
        return "low"
    
    def generate_multimedia_content(self, intensity):
        """Generate video, image, audio, and text content using free AI tools"""
        # Generate campaign theme
        theme = random.choice([
            "New Elite Mission", "Character Showcase", "Gameplay Highlight",
            "Player Achievement", "Limited-Time Event"
        ])
        
        # Generate script using free AI API
        script = self.generate_script(theme)
        
        # Create multimedia assets
        content = {
            "theme": theme,
            "script": script,
            "hashtags": "#BlackOpsGame #TacticalGaming #FreeToPlay #MobileGame",
            "video_file": self.create_video(script, intensity),
            "image_files": self.create_images(script, 3, intensity),
            "audio_clip": self.create_audio(script)
        }
        
        return content
    
    def generate_script(self, theme):
        """Generate marketing script using free AI API"""
        # Simulate using free AI services
        scripts = {
            "New Elite Mission": (
                "🚀 NEW MISSION UNLOCKED!\n"
                "Lead your elite team in Operation: Midnight Strike\n"
                "Infiltrate the high-security facility and neutralize the threat\n"
                "Available now in Black Ops: Mission Command!"
            ),
            "Character Showcase": (
                "MEET THE ELITE TEAM!\n"
                "Chris Stone: Team Leader with Mjolnir Strike ability\n"
                "Luke Steel: Tactical Specialist with Shield Wall defense\n"
                "Liam Frost: Sniper with Precision Shot\n"
                "Build your squad today!"
            ),
            "Gameplay Highlight": (
                "INTENSE TACTICAL COMBAT!\n"
                "Turn-based strategy meets explosive action\n"
                "Command your team, use special abilities, and complete missions\n"
                "Download now and join the fight!"
            )
        }
        return scripts.get(theme, "Experience elite tactical combat in Black Ops: Mission Command! Download now!")
    
    def create_video(self, script, intensity):
        """Create short video content using free tools"""
        # Determine video length based on intensity
        duration = 15 if intensity == "high" else 9
        
        # Generate gameplay footage (simulated)
        clips = []
        for _ in range(3):
            # Create dynamic gameplay visual
            clip = self.generate_gameplay_clip(duration/3)
            clips.append(clip)
        
        # Combine clips
        final_clip = mpe.concatenate_videoclips(clips)
        
        # Add text overlay
        txt_clip = mpe.TextClip(script, fontsize=28, color='white', 
                               font='Arial-Bold', size=(final_clip.w * 0.9, None))
        txt_clip = txt_clip.set_position(('center', 'top')).set_duration(duration)
        
        # Add audio
        audio = self.create_audio(script)
        final_clip = final_clip.set_audio(audio)
        
        # Add text to video
        video = mpe.CompositeVideoClip([final_clip, txt_clip])
        
        # Save video
        filename = f"data/marketing/videos/{int(time.time())}.mp4"
        video.write_videofile(filename, fps=24, codec='libx264', audio_codec='aac')
        
        return filename
    
    def generate_gameplay_clip(self, duration):
        """Generate simulated gameplay footage"""
        # Create dynamic gameplay animation
        width, height = 720, 1280
        frames = []
        
        for i in range(int(duration * 24)):
            # Create animated frame
            img = Image.new('RGB', (width, height), color=(15, 25, 45))
            draw = ImageDraw.Draw(img)
            
            # Draw animated elements
            draw.rectangle([100, 200 + i%100, 600, 400], fill=(30, 60, 100))
            draw.rectangle([200, 300 + i%80, 500, 500], fill=(50, 100, 200))
            draw.rectangle([300, 400 + i%60, 400, 600], fill=(200, 50, 50))
            
            # Convert to array and add to frames
            frames.append(np.array(img))
        
        return mpe.ImageSequenceClip(frames, fps=24)
    
    def create_images(self, script, count, intensity):
        """Generate social media images"""
        images = []
        for i in range(count):
            # Create image with different aspect ratios
            if i == 0:
                size = (1080, 1080)  # Instagram square
            elif i == 1:
                size = (1080, 1920)  # Instagram story
            else:
                size = (1200, 630)   # Facebook/Twitter
            
            img = Image.new('RGB', size, color=(15, 25, 45))
            draw = ImageDraw.Draw(img)
            
            # Draw game elements
            draw.rectangle([50, 50, size[0]-50, size[1]-50], outline=ACCENT, width=5)
            
            # Add text
            try:
                font = ImageFont.truetype("arialbd.ttf", 36)
                draw.text((size[0]//2, size[1]//2), script, 
                         fill=WHITE, font=font, anchor="mm")
            except:
                # Fallback if font not found
                draw.text((size[0]//2, size[1]//2), script, 
                         fill=WHITE, anchor="mm")
            
            # Save image
            filename = f"data/marketing/images/{int(time.time())}_{i}.png"
            img.save(filename)
            images.append(filename)
        
        return images
    
    def create_audio(self, script):
        """Generate voiceover audio using free TTS"""
        # Simulate using free TTS service
        filename = f"data/marketing/audio/{int(time.time())}.mp3"
        
        # In real implementation, would use:
        # from gtts import gTTS
        # tts = gTTS(script)
        # tts.save(filename)
        
        # For simulation, create silent audio
        with open(filename, 'wb') as f:
            f.write(b'')  # Empty file for now
        
        return mpe.AudioFileClip(filename)
    
    def get_active_platforms(self):
        """Get all social platforms to target"""
        return self.config.get('AI_AGENTS', 'MARKETING_PLATFORMS', 
                              fallback="tiktok,instagram,facebook,twitter,youtube_shorts,snapchat").split(',')
    
    def post_to_platform(self, platform, content, intensity):
        """Post content to specified platform with intensity-based scheduling"""
        # Determine posting frequency
        frequency = {"high": 4, "medium": 2, "low": 1}[intensity]
        
        for i in range(frequency):
            # Post different content variations
            if platform in ["tiktok", "youtube_shorts"]:
                # Use video content
                media = content["video_file"]
                caption = f"{content['script']}\n\n{content['hashtags']}"
            elif platform == "instagram":
                # Use square image for feed, story for stories
                media = content["image_files"][0] if i % 2 == 0 else content["image_files"][1]
                caption = f"{content['script']}\n{content['hashtags']}"
            else:
                # Use standard image
                media = content["image_files"][2]
                caption = f"{content['script']}\n{content['hashtags']}"
            
            # Simulate posting
            print(f"Posted to {platform.upper()}: {caption[:50]}...")
            
            # Track in campaign log
            self.campaigns.append({
                "platform": platform,
                "content": media,
                "intensity": intensity,
                "timestamp": datetime.now().isoformat()
            })
            
            # Space out posts
            time.sleep(random.uniform(0.5, 2))
    
    def track_campaign(self, content, intensity):
        """Track campaign performance and estimate installs"""
        # Simulate campaign results
        engagement_rate = {"high": 0.12, "medium": 0.08, "low": 0.05}[intensity]
        install_rate = engagement_rate * 0.15  # 15% conversion
        
        # Estimate reach based on intensity
        reach = {"high": 50000, "medium": 25000, "low": 10000}[intensity]
        
        # Calculate installs
        installs = int(reach * install_rate)
        
        print(f"Campaign generated: {reach} reach, {installs} installs")
        
        # Save campaign data
        with open("data/marketing/campaigns/campaigns.json", "a") as f:
            f.write(json.dumps({
                "theme": content["theme"],
                "intensity": intensity,
                "reach": reach,
                "installs": installs,
                "platforms": self.get_active_platforms(),
                "timestamp": datetime.now().isoformat()
            }) + "\n")
        
        # Update player count
        self.update_player_count(installs)
        return installs
    
    def update_player_count(self, new_players):
        """Update player count in config"""
        current = self.get_current_players()
        self.config.set('PLAYERS', 'COUNT', str(current + new_players))
        
        with open('config.ini', 'w') as configfile:
            self.config.write(configfile)
    
    def get_current_players(self):
        """Get current player count"""
        try:
            return int(self.config.get('PLAYERS', 'COUNT', fallback="0"))
        except:
            return 0
    
    def boost_campaign(self, current_intensity):
        """Increase campaign intensity if behind targets"""
        if current_intensity != "high":
            print("Boosting campaign intensity to HIGH")
            self.execute_campaign(intensity="high")
            
    def get_status(self):
        return {
            "status": self.status,
            "last_run": self.last_run.isoformat() if self.last_run else None,
            "campaign_count": len(self.campaigns),
            "current_players": self.get_current_players()
        }
