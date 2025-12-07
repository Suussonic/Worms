import pygame

class Enemy:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = (255, 0, 0)  # Rouge
        
        self.velocity = pygame.math.Vector2(0, 0)
        self.GRAVITY = 0.8  # Même gravité que le joueur
        self.on_ground = False
    
    def update(self, screen_height):
        self.velocity.y += self.GRAVITY
        
        self.rect.x += self.velocity.x
        self.rect.y += self.velocity.y
        
        # Gestion collision sol
        if self.rect.bottom >= screen_height:
            self.rect.bottom = screen_height
            self.velocity.y = 0
            self.on_ground = True
        else:
            self.on_ground = False
    
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
