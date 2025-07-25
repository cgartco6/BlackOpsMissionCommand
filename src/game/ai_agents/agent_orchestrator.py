import time
import threading
import schedule
from .marketing_agent import MarketingAgent
from .upgrade_agent import UpgradeAgent
from .content_agent import ContentAgent
from .analytics_agent import AnalyticsAgent

class AIOrchestrator:
    def __init__(self, game_version):
        self.game_version = game_version
        self.agents = {
            "marketing": MarketingAgent(),
            "upgrade": UpgradeAgent(game_version),
            "content": ContentAgent(),
            "analytics": AnalyticsAgent()
        }
        self.running = False
        self.thread = None
        
    def start(self):
        """Start all AI agents in background threads"""
        if self.running:
            return
            
        self.running = True
        self.thread = threading.Thread(target=self._run_scheduler)
        self.thread.daemon = True
        self.thread.start()
        print("AI Orchestrator started")
        
    def _run_scheduler(self):
        """Schedule agent tasks at appropriate intervals"""
        # Marketing - run every 6 hours
        schedule.every(6).hours.do(self.agents["marketing"].execute_campaign)
        
        # Upgrade checks - run every 12 hours
        schedule.every(12).hours.do(self.agents["upgrade"].check_for_upgrades)
        
        # Content generation - run daily
        schedule.every().day.at("03:00").do(self.agents["content"].generate_new_content)
        
        # Analytics optimization - run every 4 hours
        schedule.every(4).hours.do(self.agents["analytics"].optimize_game)
        
        while self.running:
            schedule.run_pending()
            time.sleep(60)  # Check every minute
            
    def stop(self):
        """Stop all AI agents"""
        self.running = False
        if self.thread:
            self.thread.join(timeout=5)
        print("AI Orchestrator stopped")
        
    def get_status(self):
        """Get current status of all agents"""
        return {
            "marketing": self.agents["marketing"].get_status(),
            "upgrade": self.agents["upgrade"].get_status(),
            "content": self.agents["content"].get_status(),
            "analytics": self.agents["analytics"].get_status()
        }
