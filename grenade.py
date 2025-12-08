import pygame
import math
import os

class Grenade:
    def __init__(self, x, y, angle, power, owner=None, air_friction=False):
        # Position de la grenade
        self.x = x
        self.y = y
        self.radius = 6
        
        # Propriétaire ("p1", "p2", etc.)
        self.owner = owner
        
        # Angle en radians
        angle_rad = math.radians(angle)
        
        # Vitesse initiale
        self.velocity_x = power * 0.6 * math.cos(angle_rad)
        self.velocity_y = power * 0.6 * math.sin(angle_rad)
        
        # Gravité
        self.GRAVITY = 0.5
        
        # Frottements de l'air
        self.air_friction = air_friction
        self.AIR_FRICTION_COEF = 0.98
        
        # Actif ou non
        self.active = True
        
        # Timer d'explosion
        self.explosion_time = 5000
        self.creation_time = pygame.time.get_ticks()
        self.paused_time = 0
        self.pause_start = 0
        self.is_paused = False
        
        # Rebonds
        self.bounce_count = 0
        self.max_bounces = 10
        self.bounce_damping = 0.6

        # --- GESTION DU SPRITE ---
        self.image = None
        image_path = "image/grenade.png" 
        
        if os.path.exists(image_path):
            try:
                original_image = pygame.image.load(image_path).convert_alpha()
                self.image = pygame.transform.scale(original_image, (16, 16))
            except Exception as e:
                print(f"Erreur chargement image grenade: {e}")
    
    def update(self, terrain=None):
        if not self.active:
            return
        
        # Timer
        current_time = pygame.time.get_ticks()
        elapsed_time = current_time - self.creation_time - self.paused_time
        if elapsed_time >= self.explosion_time:
            self.explode()
            return
        
        # Physique
        self.velocity_y += self.GRAVITY
        
        if self.air_friction:
            self.velocity_x *= self.AIR_FRICTION_COEF
            self.velocity_y *= self.AIR_FRICTION_COEF
        
        old_x = self.x
        old_y = self.y
        
        self.x += self.velocity_x
        self.y += self.velocity_y
        
        if terrain:
            self.handle_terrain_collision(terrain, old_x, old_y)
    
    def handle_terrain_collision(self, terrain, old_x, old_y):
        """Gère les collisions et rebonds avec le terrain"""
        collision_detected = False
        
        # Points de vérification autour de la grenade
        check_points = [
            (0, 0), (self.radius, 0), (-self.radius, 0),
            (0, self.radius), (0, -self.radius),
            (self.radius * 0.7, self.radius * 0.7),
            (-self.radius * 0.7, self.radius * 0.7),
            (self.radius * 0.7, -self.radius * 0.7),
            (-self.radius * 0.7, -self.radius * 0.7),
        ]
        
        for dx, dy in check_points:
            if terrain.is_solid(int(self.x + dx), int(self.y + dy)):
                collision_detected = True
                break
        
        if collision_detected:
            self.x = old_x
            self.y = old_y
            
            collision_normal_x = 0
            collision_normal_y = 0
            
            check_dist_x = max(self.radius + 4, abs(self.velocity_x) + 4)
            check_dist_y = max(self.radius + 4, abs(self.velocity_y) + 4)
            
            if terrain.is_solid(int(self.x), int(self.y + check_dist_y)):
                collision_normal_y = -1 
            elif terrain.is_solid(int(self.x), int(self.y - check_dist_y)):
                collision_normal_y = 1
            if terrain.is_solid(int(self.x + check_dist_x), int(self.y)):
                collision_normal_x = -1
            elif terrain.is_solid(int(self.x - check_dist_x), int(self.y)):
                collision_normal_x = 1
            
            if collision_normal_y != 0:
                self.velocity_y = -self.velocity_y * self.bounce_damping
                self.velocity_x *= 0.8
                self.y += collision_normal_y * 2
            
            if collision_normal_x != 0:
                self.velocity_x = -self.velocity_x * self.bounce_damping
                self.x += collision_normal_x * 2
            
            self.bounce_count += 1
            
            # Explosion si trop de rebonds ou vitesse très faible
            speed = math.sqrt(self.velocity_x**2 + self.velocity_y**2)
            if self.bounce_count >= self.max_bounces or (speed < 0.5 and self.bounce_count > 0):
                self.explode()

    def pause(self):
        if not self.is_paused:
            self.is_paused = True
            self.pause_start = pygame.time.get_ticks()
    
    def resume(self):
        if self.is_paused:
            self.is_paused = False
            self.paused_time += pygame.time.get_ticks() - self.pause_start
    
    def explode(self):
        self.active = False
    
    def draw(self, screen):
        if self.active:
            if self.image:
                rect = self.image.get_rect(center=(int(self.x), int(self.y)))
                screen.blit(self.image, rect)
            else:
                pygame.draw.circle(screen, (0, 150, 0), (int(self.x), int(self.y)), self.radius)
            
            # Timer
            current_time = pygame.time.get_ticks()
            elapsed_time = current_time - self.creation_time - self.paused_time
            time_left = max(0, (self.explosion_time - elapsed_time) / 1000)
            font = pygame.font.Font(None, 20)
            timer_text = font.render(f"{time_left:.1f}s", True, (255, 255, 255))
            screen.blit(timer_text, (int(self.x) - 15, int(self.y) - 20))
    
    def is_out_of_bounds(self, width, height):
        return self.x < -50 or self.x > width + 50 or self.y > height + 50
    
    def check_collision(self, rect):
        grenade_rect = pygame.Rect(int(self.x - self.radius), int(self.y - self.radius), self.radius * 2, self.radius * 2)
        return grenade_rect.colliderect(rect)
    
    def get_time_remaining(self):
        # Retourne le temps restant avant explosion en secondes
        elapsed = pygame.time.get_ticks() - self.creation_time - self.paused_time
        return max(0, (self.explosion_time - elapsed) / 1000)
