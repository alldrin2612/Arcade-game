import pygame
import os
from game import SpaceShooter

class Menu:
    def __init__(self):
        pygame.init()
        
        # Initial window setup
        self.WINDOW_WIDTH = 800
        self.WINDOW_HEIGHT = 600
        self.screen = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        pygame.display.set_caption("Space Invaders - Ship Selection")
        
        # Colors
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.GRAY = (128, 128, 128)
        self.HIGHLIGHT = (0, 255, 0, 128)  # Semi-transparent green
        
        # Load ship images
        self.ships = []
        self.ship_rects = []
        self.selected_ship = 0
        
        ship_files = ["ship 1.png", "ship 2.png", "spaceship 1.png", "spaceship 2.png"]
        for ship_file in ship_files:
            path = os.path.join("BG", ship_file)
            ship = pygame.image.load(path)
            ship = pygame.transform.scale(ship, (100, 100))  # Resize ships to uniform size
            self.ships.append(ship)
        
        # Create ship selection rectangles
        spacing = self.WINDOW_WIDTH // 5
        y_position = self.WINDOW_HEIGHT // 2 - 50
        for i in range(4):
            x_position = spacing * (i + 1) - 50
            self.ship_rects.append(pygame.Rect(x_position, y_position, 100, 100))
        
        # Start button
        button_width = 200
        button_height = 50
        self.start_button = pygame.Rect(
            self.WINDOW_WIDTH // 2 - button_width // 2,
            self.WINDOW_HEIGHT - 100,
            button_width,
            button_height
        )
        
        self.fullscreen = False
        
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
                
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_f, pygame.K_f):
                    self.toggle_fullscreen()
                    
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                # Check ship selection
                for i, rect in enumerate(self.ship_rects):
                    if rect.collidepoint(mouse_pos):
                        self.selected_ship = i
                
                # Check start button
                if self.start_button.collidepoint(mouse_pos):
                    # Start the game with selected ship
                    self.start_game()
                    
        return True
    
    def toggle_fullscreen(self):
        self.fullscreen = not self.fullscreen
        if self.fullscreen:
            # Get the current display info
            display_info = pygame.display.Info()
            self.WINDOW_WIDTH = display_info.current_w
            self.WINDOW_HEIGHT = display_info.current_h
            self.screen = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT), pygame.FULLSCREEN)
        else:
            self.WINDOW_WIDTH = 800
            self.WINDOW_HEIGHT = 600
            self.screen = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
    
    def draw(self):
        # Clear screen
        self.screen.fill(self.BLACK)
        
        # Draw game title
        title_font = pygame.font.Font(None, 72)  # Bigger font for game title
        game_title = title_font.render("Space Shooter", True, self.WHITE)
        game_title_rect = game_title.get_rect(center=(self.WINDOW_WIDTH // 2, 50))
        self.screen.blit(game_title, game_title_rect)
        
        # Draw ship selection text (moved down)
        selection_font = pygame.font.Font(None, 48)
        selection_text = selection_font.render("Select Your Ship", True, self.WHITE)
        selection_rect = selection_text.get_rect(center=(self.WINDOW_WIDTH // 2, 150))
        self.screen.blit(selection_text, selection_rect)
        
        # Draw ships and highlight selected
        for i, (ship, rect) in enumerate(zip(self.ships, self.ship_rects)):
            # Draw highlight for selected ship
            if i == self.selected_ship:
                highlight_surface = pygame.Surface((rect.width + 10, rect.height + 10), pygame.SRCALPHA)
                pygame.draw.rect(highlight_surface, self.HIGHLIGHT, highlight_surface.get_rect())
                self.screen.blit(highlight_surface, (rect.x - 5, rect.y - 5))
            
            self.screen.blit(ship, rect)
        
        # Draw start button
        pygame.draw.rect(self.screen, self.WHITE, self.start_button, 2)
        font = pygame.font.Font(None, 36)
        start_text = font.render("START", True, self.WHITE)
        text_rect = start_text.get_rect(center=self.start_button.center)
        self.screen.blit(start_text, text_rect)
        
        # Update display
        pygame.display.flip()
    
    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.draw()
        
        pygame.quit()
    
    def start_game(self):
        # Initialize and run the game with the selected ship and screen properties
        game = SpaceShooter(
            selected_ship=self.selected_ship,
            is_fullscreen=self.fullscreen,
            screen_width=self.WINDOW_WIDTH,
            screen_height=self.WINDOW_HEIGHT
        )
        game.run()
        
        # After the game ends, reset the display mode
        if self.fullscreen:
            self.screen = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT), pygame.FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))

if __name__ == "__main__":
    menu = Menu()
    menu.run()
