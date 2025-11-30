import pygame

class Worm:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        
        self.velocity = pygame.math.Vector2(0, 0)
        
        self.SPEED = 5          # Vitesse horizontale
        self.JUMP_FORCE = -15   # Force du saut
        self.GRAVITY = 0.8      # Gravité
        
        self.on_ground = False

    def handle_input(self):
        keys = pygame.key.get_pressed()

        # Gauche / Droite
        if keys[pygame.K_LEFT] or keys[pygame.K_q]:
            self.velocity.x = -self.SPEED
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.velocity.x = self.SPEED
        else:
            self.velocity.x = 0

        # Saut (seulement si on est au sol)
        if (keys[pygame.K_SPACE] or keys[pygame.K_z] or keys[pygame.K_UP]) and self.on_ground:
            self.jump()

    def jump(self):
        self.velocity.y = self.JUMP_FORCE
        self.on_ground = False

    def update(self, screen_height):
        self.velocity.y += self.GRAVITY

        self.rect.x += self.velocity.x
        self.rect.y += self.velocity.y

        # Gestion collision sol (pour l'instant bord de l'écran)
        if self.rect.bottom >= screen_height:
            self.rect.bottom = screen_height
            self.velocity.y = 0
            self.on_ground = True
        else:
            self.on_ground = False

    def get_position(self):
        return (self.rect.x, self.rect.y)