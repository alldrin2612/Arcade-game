import pygame
import random
import math
import os

class SpaceShooter:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()

        # Display settings
        self.screen_width = 800
        self.screen_height = 600
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Space Shooter")
        
        # Colors
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.RED = (255, 0, 0)
        self.GREEN = (0, 255, 0)
        
        # Game states
        self.running = True
        self.game_over = False
        self.score = 0
        self.lives = 3
        self.wave = 1
        
        # Clock and timing
        self.clock = pygame.time.Clock()
        self.FPS = 60
        
        # Load assets
        self.load_assets()
        
        # Initialize game objects
        self.init_game_objects()

    def load_assets(self):
        # Create simple shapes for entities if no images available
        self.player_ship = pygame.Surface((40, 40), pygame.SRCALPHA)
        pygame.draw.polygon(self.player_ship, self.WHITE, [(20, 0), (0, 40), (40, 40)])
        
        self.enemy_ship = pygame.Surface((30, 30), pygame.SRCALPHA)
        pygame.draw.polygon(self.enemy_ship, self.RED, [(15, 0), (30, 30), (0, 30)])
        
        self.bullet = pygame.Surface((4, 12), pygame.SRCALPHA)
        pygame.draw.rect(self.bullet, self.GREEN, (0, 0, 4, 12))
        
        # Font
        self.font = pygame.font.Font(None, 36)

    def init_game_objects(self):
        # Player attributes
        self.player_pos = [self.screen_width // 2, self.screen_height - 60]
        self.player_speed = 6
        self.player_velocity = [0, 0]
        self.player_acceleration = 0.5
        self.player_friction = 0.92
        
        # Enemy attributes
        self.enemies = []
        self.spawn_wave()
        
        # Bullet attributes
        self.bullets = []
        self.bullet_speed = 10
        self.last_shot_time = 0
        self.shot_delay = 250  # Milliseconds between shots

    def spawn_wave(self):
        self.enemies.clear()
        enemy_rows = 3
        enemies_per_row = 6
        
        for row in range(enemy_rows):
            for col in range(enemies_per_row):
                x = col * (self.screen_width // enemies_per_row) + 50
                y = row * 60 + 50
                enemy = {
                    'pos': [x, y],
                    'velocity': [2, 0],
                    'health': 1
                }
                self.enemies.append(enemy)

    def handle_input(self):
        keys = pygame.key.get_pressed()
        
        # Horizontal movement with acceleration
        if keys[pygame.K_LEFT]:
            self.player_velocity[0] -= self.player_acceleration
        if keys[pygame.K_RIGHT]:
            self.player_velocity[0] += self.player_acceleration
            
        # Apply friction and velocity
        self.player_velocity[0] *= self.player_friction
        self.player_pos[0] += self.player_velocity[0]
        
        # Keep player in bounds
        self.player_pos[0] = max(0, min(self.player_pos[0], self.screen_width - 40))
        
        # Shooting
        current_time = pygame.time.get_ticks()
        if keys[pygame.K_SPACE] and current_time - self.last_shot_time > self.shot_delay:
            self.shoot()
            self.last_shot_time = current_time

    def shoot(self):
        bullet_pos = [self.player_pos[0] + 18, self.player_pos[1] - 10]
        self.bullets.append(bullet_pos)

    def update_enemies(self):
        for enemy in self.enemies:
            # Update enemy position
            enemy['pos'][0] += enemy['velocity'][0]
            
            # Check for wall collision
            if enemy['pos'][0] <= 0 or enemy['pos'][0] >= self.screen_width - 30:
                enemy['velocity'][0] *= -1
                enemy['pos'][1] += 20  # Move down when hitting wall
                
            # Check if enemies reached player
            if enemy['pos'][1] + 30 >= self.player_pos[1]:
                self.game_over = True

    def update_bullets(self):
        for bullet in self.bullets[:]:
            bullet[1] -= self.bullet_speed
            if bullet[1] < -10:
                self.bullets.remove(bullet)

    def check_collisions(self):
        for bullet in self.bullets[:]:
            for enemy in self.enemies[:]:
                if (bullet[0] > enemy['pos'][0] and 
                    bullet[0] < enemy['pos'][0] + 30 and
                    bullet[1] > enemy['pos'][1] and 
                    bullet[1] < enemy['pos'][1] + 30):
                    
                    if bullet in self.bullets:
                        self.bullets.remove(bullet)
                    self.enemies.remove(enemy)
                    self.score += 100
                    
                    # Check for wave completion
                    if not self.enemies:
                        self.wave += 1
                        self.spawn_wave()
                    break

    def draw(self):
        self.screen.fill(self.BLACK)
        
        # Draw player
        self.screen.blit(self.player_ship, self.player_pos)
        
        # Draw enemies
        for enemy in self.enemies:
            self.screen.blit(self.enemy_ship, enemy['pos'])
        
        # Draw bullets
        for bullet in self.bullets:
            self.screen.blit(self.bullet, bullet)
        
        # Draw HUD
        score_text = self.font.render(f'Score: {self.score}', True, self.WHITE)
        wave_text = self.font.render(f'Wave: {self.wave}', True, self.WHITE)
        lives_text = self.font.render(f'Lives: {self.lives}', True, self.WHITE)
        
        self.screen.blit(score_text, (10, 10))
        self.screen.blit(wave_text, (10, 40))
        self.screen.blit(lives_text, (10, 70))
        
        if self.game_over:
            game_over_text = self.font.render('GAME OVER - Press R to Restart', True, self.RED)
            text_rect = game_over_text.get_rect(center=(self.screen_width/2, self.screen_height/2))
            self.screen.blit(game_over_text, text_rect)
        
        pygame.display.flip()

    def run(self):
        while self.running:
            self.clock.tick(self.FPS)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r and self.game_over:
                        self.game_over = False
                        self.score = 0
                        self.wave = 1
                        self.lives = 3
                        self.init_game_objects()
            
            if not self.game_over:
                self.handle_input()
                self.update_enemies()
                self.update_bullets()
                self.check_collisions()
            
            self.draw()
        
        pygame.quit()

if __name__ == "__main__":
    game = SpaceShooter()
    game.run()