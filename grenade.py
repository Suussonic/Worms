import pygame
import math

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
        
        # Vitesse initiale (plus faible que la roquette)
        self.velocity_x = power * 0.6 * math.cos(angle_rad)  # Vitesse réduite
        self.velocity_y = power * 0.6 * math.sin(angle_rad)
        
        # Gravité
        self.GRAVITY = 0.5
        
        # Frottements de l'air
        self.air_friction = air_friction
        self.AIR_FRICTION_COEF = 0.98  # Coefficient de friction (1.0 = pas de friction)
        
        # Actif ou non
        self.active = True
        
        # Timer d'explosion (5 secondes)
        self.explosion_time = 5000  # millisecondes
        self.creation_time = pygame.time.get_ticks()
        self.paused_time = 0  # Temps cumulé en pause
        self.pause_start = 0  # Moment où la pause a commencé
        self.is_paused = False
        
        # Nombre de rebonds effectués
        self.bounce_count = 0
        self.max_bounces = 10  # Explosion après 10 rebonds maximum
        
        # Coefficient de restitution (élasticité des rebonds)
        self.bounce_damping = 0.6  # 60% de l'énergie conservée
    
    def update(self, terrain=None):
        if not self.active:
            return
        
        # Vérifier le timer d'explosion (en tenant compte du temps de pause)
        current_time = pygame.time.get_ticks()
        elapsed_time = current_time - self.creation_time - self.paused_time
        if elapsed_time >= self.explosion_time:
            self.explode()
            return
        
        # Appliquer la gravité
        self.velocity_y += self.GRAVITY
        
        # Appliquer les frottements de l'air si activés
        if self.air_friction:
            self.velocity_x *= self.AIR_FRICTION_COEF
            self.velocity_y *= self.AIR_FRICTION_COEF
        
        # Sauvegarder l'ancienne position
        old_x = self.x
        old_y = self.y
        
        # Mise à jour de la position
        self.x += self.velocity_x
        self.y += self.velocity_y
        
        # Gérer les rebonds avec le terrain
        if terrain:
            self.handle_terrain_collision(terrain, old_x, old_y)
    
    def handle_terrain_collision(self, terrain, old_x, old_y):
        """Gère les collisions et rebonds avec le terrain"""
        # Vérifier si la grenade touche le terrain
        if terrain.is_solid(int(self.x), int(self.y)):
            # Revenir à l'ancienne position
            self.x = old_x
            self.y = old_y
            
            # Déterminer la normale de collision (approximation simple)
            # Vérifier autour pour trouver la direction du rebond
            collision_normal_x = 0
            collision_normal_y = 0
            
            # Vérifier les 4 directions principales
            check_distance = 10
            if terrain.is_solid(int(self.x), int(self.y - check_distance)):
                collision_normal_y = 1  # Sol en dessous
            if terrain.is_solid(int(self.x), int(self.y + check_distance)):
                collision_normal_y = -1  # Plafond au-dessus
            if terrain.is_solid(int(self.x - check_distance), int(self.y)):
                collision_normal_x = 1  # Mur à gauche
            if terrain.is_solid(int(self.x + check_distance), int(self.y)):
                collision_normal_x = -1  # Mur à droite
            
            # Rebond basique
            if collision_normal_y != 0:
                # Rebond vertical
                self.velocity_y = -self.velocity_y * self.bounce_damping
                self.velocity_x *= 0.8  # Friction horizontale au sol
                self.y += collision_normal_y * 2  # Décoller légèrement
            
            if collision_normal_x != 0:
                # Rebond horizontal
                self.velocity_x = -self.velocity_x * self.bounce_damping
                self.x += collision_normal_x * 2  # Décoller légèrement
            
            self.bounce_count += 1
            
            # La grenade peut exploser de 3 façons:
            # 1. Timer de 5 secondes (géré dans update())
            # 2. Trop de rebonds (10 rebonds maximum)
            # 3. Vitesse trop faible (quasi immobile)
            speed = math.sqrt(self.velocity_x**2 + self.velocity_y**2)
            if self.bounce_count >= self.max_bounces or speed < 0.5:
                self.explode()
    
    def pause(self):
        """Met le timer de la grenade en pause"""
        if not self.is_paused:
            self.is_paused = True
            self.pause_start = pygame.time.get_ticks()
    
    def resume(self):
        """Reprend le timer de la grenade"""
        if self.is_paused:
            self.is_paused = False
            self.paused_time += pygame.time.get_ticks() - self.pause_start
    
    def explode(self):
        """Marque la grenade comme inactive (explosion)"""
        self.active = False
    
    def draw(self, screen):
        if self.active:
            # Dessiner la grenade (cercle vert foncé)
            pygame.draw.circle(
                screen,
                (0, 150, 0),
                (int(self.x), int(self.y)),
                self.radius
            )
            
            # Afficher le temps restant avant explosion
            current_time = pygame.time.get_ticks()
            elapsed_time = current_time - self.creation_time - self.paused_time
            time_left = max(0, (self.explosion_time - elapsed_time) / 1000)
            font = pygame.font.Font(None, 20)
            timer_text = font.render(f"{time_left:.1f}s", True, (255, 255, 255))
            screen.blit(timer_text, (int(self.x) - 15, int(self.y) - 20))
    
    def is_out_of_bounds(self, width, height):
        """Vrai si la grenade sort de l'écran"""
        return self.x < -50 or self.x > width + 50 or self.y > height + 50
    
    def check_collision(self, rect):
        """Vérifie la collision avec un rectangle (vers)"""
        grenade_rect = pygame.Rect(
            int(self.x - self.radius),
            int(self.y - self.radius),
            self.radius * 2,
            self.radius * 2
        )
        return grenade_rect.colliderect(rect)
    
    def get_time_remaining(self):
        """Retourne le temps restant avant explosion en secondes"""
        elapsed = pygame.time.get_ticks() - self.creation_time - self.paused_time
        return max(0, (self.explosion_time - elapsed) / 1000)
