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
        self.BLUE = (0, 0, 255)
        
        # Game states
        self.running = True
        self.game_over = False
        self.score = 0
        self.lives = 3
        self.wave = 1
        
        # Clock and timing
        self.clock = pygame.time.Clock()
        self.FPS = 60
        
        # Wave patterns
        self.wave_patterns = [
            self.create_grid_formation,
            self.create_v_formation,
            self.create_circle_formation,
            self.create_diamond_formation,
            self.create_zigzag_formation
        ]
        
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

    def create_enemy(self, x, y, pattern_type):
        movement_patterns = {
            'linear': {'velocity': [2, 0], 'pattern_func': self.move_linear},
            'sine': {'velocity': [2, 0], 'pattern_func': self.move_sine},
            'circular': {'velocity': [2, 0], 'pattern_func': self.move_circular},
            'zigzag': {'velocity': [2, 0], 'pattern_func': self.move_zigzag}
        }
        
        pattern = random.choice(list(movement_patterns.keys()))
        
        return {
            'pos': [x, y],
            'velocity': movement_patterns[pattern]['velocity'].copy(),
            'health': 1,
            'pattern': pattern,
            'pattern_func': movement_patterns[pattern]['pattern_func'],
            'initial_pos': [x, y],
            'time': random.random() * math.pi * 2  # Random start phase
        }

    def create_grid_formation(self):
        enemies = []
        rows = 3
        cols = 6
        spacing_x = 80
        spacing_y = 60
        
        for row in range(rows):
            for col in range(cols):
                x = col * spacing_x + 100
                y = row * spacing_y + 50
                enemies.append(self.create_enemy(x, y, 'grid'))
        return enemies

    def create_v_formation(self):
        enemies = []
        num_enemies = 9
        spacing = 40
        
        for i in range(num_enemies):
            if i < num_enemies // 2:
                x = self.screen_width // 2 - (i + 1) * spacing
                y = 50 + i * spacing
            else:
                x = self.screen_width // 2 + (i - num_enemies // 2) * spacing
                y = 50 + (num_enemies - i - 1) * spacing
            enemies.append(self.create_enemy(x, y, 'v'))
        return enemies

    def create_circle_formation(self):
        enemies = []
        num_enemies = 12
        radius = 100
        center_x = self.screen_width // 2
        center_y = 150
        
        for i in range(num_enemies):
            angle = (2 * math.pi * i) / num_enemies
            x = center_x + radius * math.cos(angle)
            y = center_y + radius * math.sin(angle)
            enemies.append(self.create_enemy(x, y, 'circle'))
        return enemies

    def create_diamond_formation(self):
        enemies = []
        size = 5
        spacing = 40
        
        for i in range(size * 2 - 1):
            width = size - abs(size - 1 - i)
            for j in range(width):
                x = self.screen_width // 2 + (j - width // 2) * spacing
                y = 50 + i * spacing // 2
                enemies.append(self.create_enemy(x, y, 'diamond'))
        return enemies

    def create_zigzag_formation(self):
        enemies = []
        num_rows = 3
        enemies_per_row = 8
        spacing_x = 80
        spacing_y = 60
        
        for row in range(num_rows):
            offset = spacing_x // 2 if row % 2 else 0
            for col in range(enemies_per_row):
                x = col * spacing_x + offset + 50
                y = row * spacing_y + 50
                enemies.append(self.create_enemy(x, y, 'zigzag'))
        return enemies

    def move_linear(self, enemy):
        enemy['pos'][0] += enemy['velocity'][0]
        if enemy['pos'][0] <= 0 or enemy['pos'][0] >= self.screen_width - 30:
            enemy['velocity'][0] *= -1
            enemy['pos'][1] += 20

    def move_sine(self, enemy):
        enemy['time'] += 0.05
        enemy['pos'][0] += enemy['velocity'][0]
        enemy['pos'][1] = enemy['initial_pos'][1] + math.sin(enemy['time']) * 30
        
        if enemy['pos'][0] <= 0 or enemy['pos'][0] >= self.screen_width - 30:
            enemy['velocity'][0] *= -1
            enemy['pos'][1] += 10

    def move_circular(self, enemy):
        enemy['time'] += 0.03
        radius = 30
        enemy['pos'][0] = enemy['initial_pos'][0] + math.cos(enemy['time']) * radius
        enemy['pos'][1] = enemy['initial_pos'][1] + math.sin(enemy['time']) * radius

    def move_zigzag(self, enemy):
        enemy['time'] += 0.1
        enemy['pos'][0] += enemy['velocity'][0]
        if enemy['pos'][0] <= 0 or enemy['pos'][0] >= self.screen_width - 30:
            enemy['velocity'][0] *= -1
            enemy['pos'][1] += 30

    def spawn_wave(self):
        self.enemies.clear()
        
        # Choose a random formation based on wave number
        if self.wave <= len(self.wave_patterns):
            # Use sequential patterns for first few waves
            pattern_func = self.wave_patterns[self.wave - 1]
        else:
            # Use random patterns for later waves
            pattern_func = random.choice(self.wave_patterns)
        
        # Create enemies using the selected pattern
        self.enemies = pattern_func()
        
        # Increase difficulty with each wave
        speed_multiplier = 1 + (self.wave - 1) * 0.1
        for enemy in self.enemies:
            enemy['velocity'][0] *= speed_multiplier

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
            enemy['pattern_func'](enemy)
            
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