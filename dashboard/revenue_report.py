import pygame
import random
from config import *

class RevenueReport:
    def __init__(self):
        self.font = pygame.font.Font("assets/fonts/default.ttf", 20)
        self.title_font = pygame.font.Font("assets/fonts/default.ttf", 28)
        self.data = {
            "daily_revenue": 0,
            "total_revenue": 0,
            "arpu": 0,
            "conversion": 0,
            "top_product": "Elite Pack"
        }
        self.transactions = []
        
    def update_data(self, new_data):
        """Update revenue data"""
        self.data.update(new_data)
        
        # Generate fake transactions
        if random.random() < 0.3:
            products = ["Starter Pack", "Weapon Skin", "Elite Pack", "Currency Pack"]
            self.transactions.append({
                "player": f"Player{random.randint(1000, 9999)}",
                "product": random.choice(products),
                "amount": random.uniform(1.99, 99.99)
            })
            if len(self.transactions) > 8:
                self.transactions.pop(0)
        
    def render(self, screen):
        """Render revenue dashboard"""
        # Draw title
        title = self.title_font.render("Revenue Report", True, TEXT_COLOR)
        screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 20))
        
        # Draw metrics
        self._draw_metric(screen, "Daily Revenue", f"${self.data['daily_revenue']:,.2f}", 100, 80)
        self._draw_metric(screen, "Total Revenue", f"${self.data['total_revenue']:,.2f}", 100, 140)
        self._draw_metric(screen, "ARPU", f"${self.data['arpu']:,.2f}", 100, 200)
        self._draw_metric(screen, "Conversion Rate", f"{self.data['conversion']}%", 100, 260)
        self._draw_metric(screen, "Top Product", self.data["top_product"], 100, 320)
        
        # Draw revenue breakdown
        self._draw_revenue_breakdown(screen, SCREEN_WIDTH//2 - 250, 380, 500, 200)
        
        # Draw recent transactions
        self._draw_transactions(screen, 100, 600, SCREEN_WIDTH - 200, 150)
    
    def _draw_metric(self, screen, label, value, x, y):
        """Render a single metric"""
        label_text = self.font.render(label, True, TEXT_COLOR)
        value_text = self.font.render(str(value), True, (255, 200, 100))
        
        screen.blit(label_text, (x, y))
        screen.blit(value_text, (x + 250, y))
    
    def _draw_revenue_breakdown(self, screen, x, y, width, height):
        """Render revenue breakdown chart"""
        # Draw chart background
        pygame.draw.rect(screen, (30, 35, 45), (x, y, width, height), 0)
        pygame.draw.rect(screen, (60, 70, 90), (x, y, width, height), 2)
        
        # Draw title
        chart_title = self.font.render("Revenue by Product Category", True, TEXT_COLOR)
        screen.blit(chart_title, (x + width//2 - chart_title.get_width()//2, y + 10))
        
        # Draw bars
        categories = {
            "Starter Packs": 35,
            "Weapon Skins": 25,
            "Elite Packs": 20,
            "Currency": 15,
            "Other": 5
        }
        
        bar_width = 80
        spacing = (width - (len(categories) * bar_width)) // (len(categories) + 1)
        colors = [(0, 150, 200), (0, 200, 150), (200, 150, 0), (200, 0, 100), (150, 0, 200)]
        
        for i, (category, percent) in enumerate(categories.items()):
            bar_x = x + spacing + i * (bar_width + spacing)
            bar_height = (percent / 100) * (height - 60)
            
            # Draw bar
            pygame.draw.rect(screen, colors[i], 
                           (bar_x, y + height - bar_height - 20, bar_width, bar_height), 0)
            
            # Draw label
            cat_text = self.font.render(category, True, TEXT_COLOR)
            screen.blit(cat_text, (bar_x + bar_width//2 - cat_text.get_width()//2, y + height - 15))
            
            # Draw value
            val_text = self.font.render(f"{percent}%", True, TEXT_COLOR)
            screen.blit(val_text, (bar_x + bar_width//2 - val_text.get_width()//2, y + height - bar_height - 40))
    
    def _draw_transactions(self, screen, x, y, width, height):
        """Render recent transactions"""
        # Draw section background
        pygame.draw.rect(screen, (30, 35, 45), (x, y, width, height), 0)
        pygame.draw.rect(screen, (60, 70, 90), (x, y, width, height), 2)
        
        # Draw title
        title = self.font.render("Recent Transactions", True, TEXT_COLOR)
        screen.blit(title, (x + 20, y + 10))
        
        # Draw headers
        pygame.draw.line(screen, (80, 90, 110), (x, y + 40), (x + width, y + 40), 2)
        headers = ["Player", "Product", "Amount"]
        header_x = [x + 20, x + width//3, x + 2*width//3]
        
        for i, header in enumerate(headers):
            header_text = self.font.render(header, True, (200, 200, 255))
            screen.blit(header_text, (header_x[i], y + 15))
        
        # Draw transactions
        for i, transaction in enumerate(self.transactions):
            row_y = y + 50 + i * 25
            
            player_text = self.font.render(transaction["player"], True, TEXT_COLOR)
            product_text = self.font.render(transaction["product"], True, TEXT_COLOR)
            amount_text = self.font.render(f"${transaction['amount']:.2f}", True, (200, 255, 150))
            
            screen.blit(player_text, (header_x[0], row_y))
            screen.blit(product_text, (header_x[1], row_y))
            screen.blit(amount_text, (header_x[2], row_y))
            
            if i < len(self.transactions) - 1:
                pygame.draw.line(screen, (50, 55, 65), (x, row_y + 20), (x + width, row_y + 20), 1)
