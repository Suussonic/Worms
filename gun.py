import pygame

class Projectile:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 5
        
        # Vitesse initiale vers la droite
        self.velocity_x = 10
        self.velocity_y = 0
        
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
