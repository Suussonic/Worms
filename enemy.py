import pygame

class Enemy:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = (255, 0, 0)  # Rouge
        
        self.velocity = pygame.math.Vector2(0, 0)
        self.GRAVITY = 0.8  # Même gravité que le joueur
        self.on_ground = False
        
        # Points de vie
        self.hp = 100
        self.max_hp = 100
    
    def update(self, screen_height, terrain=None):
        self.velocity.y += self.GRAVITY
        
        self.rect.x += self.velocity.x
        self.rect.y += self.velocity.y
        
        # Gestion collision avec le terrain
        if terrain:
            # Vérifier les collisions avec le terrain en dessous
            self.on_ground = False
            for x_offset in range(0, self.rect.width, 5):  # Vérifier plusieurs points
                check_x = self.rect.left + x_offset
                check_y = self.rect.bottom
                
                if terrain.is_solid(check_x, check_y):
                    # Remonter jusqu'à trouver la surface
                    while terrain.is_solid(check_x, self.rect.bottom - 1) and self.rect.bottom > 0:
                        self.rect.y -= 1
                    self.velocity.y = 0
                    self.on_ground = True
                    break
        else:
            # Fallback: collision avec le bord de l'écran
            if self.rect.bottom >= screen_height:
                self.rect.bottom = screen_height
                self.velocity.y = 0
                self.on_ground = True
            else:
                self.on_ground = False
    
    def take_damage(self, damage):
        self.hp = max(0, self.hp - damage)
    
    def is_alive(self):
        return self.hp > 0
    
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        
        # Afficher les PV au-dessus
        font = pygame.font.Font(None, 24)
        hp_text = font.render(f"HP: {self.hp}", True, (255, 255, 255))
        screen.blit(hp_text, (self.rect.x - 5, self.rect.y - 25))
