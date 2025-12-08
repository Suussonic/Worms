import pygame
import math

class Projectile:
    def __init__(self, x, y, angle, power, owner=None, air_friction=False):
        # Position du projectile
        self.x = x
        self.y = y
        self.radius = 5

        # "p1" ou "p2" (joueur 1 ou joueur 2)
        self.owner = owner
        
        # Angle en radians
        angle_rad = math.radians(angle)

        # Vitesse initiale
        self.velocity_x = power * math.cos(angle_rad)
        self.velocity_y = power * math.sin(angle_rad)

        # Gravité
        self.GRAVITY = 0.5
        
        # Frottements de l'air
        self.air_friction = air_friction
        self.AIR_FRICTION_COEF = 0.98  # Coefficient de friction (1.0 = pas de friction)
        
        # Actif ou non
        self.active = True
    
    def update(self):
        if not self.active:
            return
        
        # Gravité
        self.velocity_y += self.GRAVITY
        
        # Appliquer les frottements de l'air si activés
        if self.air_friction:
            self.velocity_x *= self.AIR_FRICTION_COEF
            self.velocity_y *= self.AIR_FRICTION_COEF
        
        # Mise à jour position
        self.x += self.velocity_x
        self.y += self.velocity_y
    
    def draw(self, screen):
        if self.active:
            pygame.draw.circle(
                screen,
                (255, 0, 0),
                (int(self.x), int(self.y)),
                self.radius
            )
    
    def is_out_of_bounds(self, width, height):
        # Vrai si le projectile sort de l'écran
        return self.x < 0 or self.x > width or self.y > height
    
    def check_collision(self, target_rect):
        # Collision avec un rectangle
        projectile_rect = pygame.Rect(
            self.x - self.radius,
            self.y - self.radius,
            self.radius * 2,
            self.radius * 2
        )
        return projectile_rect.colliderect(target_rect)
