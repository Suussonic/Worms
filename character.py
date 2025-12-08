import pygame
import os

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
        
        # Arme individuelle (chaque ver a sa propre arme)
        self.selected_weapon = "rocket"  # "rocket" ou "grenade"
        self.air_friction_enabled = False

        # --- GESTION DU SPRITE ---
        self.facing_right = True
        self.image = None
        image_path = "worm.png"
        
        if os.path.exists(image_path):
            try:
                original_image = pygame.image.load(image_path).convert_alpha()
                self.image = pygame.transform.scale(original_image, (width, height))
            except Exception as e:
                print(f"Erreur lors du chargement de l'image du ver : {e}")
        else:
            print(f"Image '{image_path}' non trouvée. Utilisation du rectangle par défaut.")

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
            self.facing_right = False
        elif keys[controls['right']]:
            self.velocity.x = self.SPEED
            self.facing_right = True
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

        # Sauvegarder la position avant déplacement
        old_x = self.rect.x
        old_y = self.rect.y

        self.rect.x += self.velocity.x
        self.rect.y += self.velocity.y
        
        # Si le ver sort de l'écran (haut ou bas), il meurt
        if self.rect.y < -10 or self.rect.y > screen_height + 10:
            self.hp = 0

        # Gestion collision avec le terrain
        if terrain:
            # Vérifier si le ver touche l'eau (mort instantanée)
            for y_offset in range(0, self.rect.height, 5):
                for x_offset in range(0, self.rect.width, 5):
                    check_x = self.rect.left + x_offset
                    check_y = self.rect.top + y_offset
                    if terrain.is_water(check_x, check_y):
                        self.hp = 0  # Mort instantanée dans l'eau
                        return
            
            # Vérifier les collisions latérales (gauche/droite)
            collision_lateral = False
            for y_offset in range(0, self.rect.height, 5):
                check_y = self.rect.top + y_offset
                # Vérifier côté gauche
                if terrain.is_solid(self.rect.left, check_y):
                    collision_lateral = True
                    break
                # Vérifier côté droit
                if terrain.is_solid(self.rect.right, check_y):
                    collision_lateral = True
                    break
            
            # Si collision latérale, annuler le déplacement horizontal
            if collision_lateral:
                self.rect.x = old_x
                self.velocity.x = 0
            
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
    
    def draw(self, screen):
        """Affiche le ver (sprite ou rectangle)"""
        if self.image:
            if self.facing_right:
                screen.blit(self.image, self.rect)
            else:
                screen.blit(pygame.transform.flip(self.image, True, False), self.rect)
        else:
            pygame.draw.rect(screen, (0, 255, 0), self.rect)
            
        # On appelle draw_hp pour afficher la vie au-dessus
        self.draw_hp(screen)

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
