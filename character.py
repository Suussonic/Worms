import pygame

class Worm:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        
        self.velocity = pygame.math.Vector2(0, 0)
        
        self.SPEED = 2          # Vitesse horizontale
        self.JUMP_FORCE = -8   # Force du saut
        self.GRAVITY = 0.8      # Gravité
        
        self.on_ground = False
        
        # Système de tir
        self.aim_angle = 0      # Angle de tir en degrés (0 = horizontal droite)
        self.aim_power = 15     # Puissance du tir
        
        # Points de vie
        self.hp = 100
        self.max_hp = 100

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
        if keys[pygame.K_SPACE] and self.on_ground:
            self.jump()

    def jump(self):
        self.velocity.y = self.JUMP_FORCE
        self.on_ground = False

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

    def get_position(self):
        return (self.rect.x, self.rect.y)
    
    def take_damage(self, damage):
        self.hp = max(0, self.hp - damage)
    
    def is_alive(self):
        return self.hp > 0
    
    def draw_hp(self, screen):
        # Afficher les PV au-dessus du personnage
        font = pygame.font.Font(None, 24)
        hp_text = font.render(f"HP: {self.hp}", True, (255, 255, 255))
        screen.blit(hp_text, (self.rect.x - 5, self.rect.y - 25))
