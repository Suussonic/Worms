import pygame

class Worm:
    def __init__(self, x, y, width, height, name="Worm"):
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
        
        # Nom du ver
        self.name = name

    def handle_input(self, controls=None):
        keys = pygame.key.get_pressed()
        
        # Si aucun contrôle personnalisé n'est fourni, utiliser les touches par défaut
        if controls is None:
            controls = {
                'left': pygame.K_LEFT,
                'right': pygame.K_RIGHT,
                'jump': pygame.K_SPACE
            }

        # Gauche / Droite
        if keys[controls['left']]:
            self.velocity.x = -self.SPEED
        elif keys[controls['right']]:
            self.velocity.x = self.SPEED
        else:
            self.velocity.x = 0

        # Saut (seulement si on est au sol)
        if keys[controls['jump']] and self.on_ground:
            self.jump()

    def jump(self):
        self.velocity.y = self.JUMP_FORCE
        self.on_ground = False

    def update(self, screen_height, terrain=None):
        self.velocity.y += self.GRAVITY

        self.rect.x += self.velocity.x
        self.rect.y += self.velocity.y
        
        # Si le ver sort de l'écran (haut ou bas), il meurt
        if self.rect.y < -10 or self.rect.y > screen_height + 10:
            self.hp = 0

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
        # Afficher le nom et les PV au-dessus du personnage
        font = pygame.font.Font(None, 22)
        
        # Afficher le nom à gauche
        name_text = font.render(self.name, True, (255, 255, 0))
        screen.blit(name_text, (self.rect.x - 5, self.rect.y - 25))
        
        # Afficher les PV à droite du nom
        hp_text = font.render(f"HP: {self.hp}", True, (255, 255, 255))
        name_width = name_text.get_width()
        screen.blit(hp_text, (self.rect.x - 5 + name_width + 5, self.rect.y - 25))
