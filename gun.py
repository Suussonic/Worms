import pygame
import math

class Projectile:
    def __init__(self, x, y, angle, power):
        self.x = x
        self.y = y
        self.radius = 5
        
        # Convertir l'angle en radians et calculer les composantes de vitesse
        angle_rad = math.radians(angle)
        self.velocity_x = power * math.cos(angle_rad)
        self.velocity_y = power * math.sin(angle_rad)
        
        self.GRAVITY = 0.5
        self.active = True
    
    def update(self):
        if not self.active:
            return
        
        # Applique la gravité
        self.velocity_y += self.GRAVITY
        
        # Met à jour la position
        self.x += self.velocity_x
        self.y += self.velocity_y
    
    def draw(self, screen):
        if self.active:
            pygame.draw.circle(screen, (255, 0, 0), (int(self.x), int(self.y)), self.radius)
    
    def is_out_of_bounds(self, width, height):
        return self.x < 0 or self.x > width or self.y > height
    
    def check_collision(self, target_rect):
        """Vérifie la collision avec un rectangle (personnage ou ennemi)"""
        projectile_rect = pygame.Rect(self.x - self.radius, self.y - self.radius, 
                                     self.radius * 2, self.radius * 2)
        return projectile_rect.colliderect(target_rect)
