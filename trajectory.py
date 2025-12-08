import math
import pygame

class TrajectoryCalculator:
    """Classe pour calculer et afficher les trajectoires de projectiles"""
    
    def __init__(self, gravity=0.5):
        self.gravity = gravity
    
    def calculate_trajectory_points(self, start_x, start_y, angle, power, max_points=100, is_grenade=False, air_friction=False):
        """
        Calcule les points de la trajectoire d'un projectile
        
        Args:
            start_x, start_y: Position de départ
            angle: Angle de tir en degrés
            power: Puissance du tir
            max_points: Nombre maximum de points à calculer
            is_grenade: Si True, réduit la vitesse initiale (grenade)
            air_friction: Si True, applique les frottements de l'air
            
        Returns:
            Liste de tuples (x, y) représentant la trajectoire
        """
        points = []
        
        # Convertir l'angle en radians et calculer les vitesses initiales
        angle_rad = math.radians(angle)
        speed_multiplier = 0.6 if is_grenade else 1.0  # Grenades plus lentes
        vx = power * speed_multiplier * math.cos(angle_rad)
        vy = power * speed_multiplier * math.sin(angle_rad)
        
        air_friction_coef = 0.98 if air_friction else 1.0
        
        # Simuler la trajectoire
        x, y = start_x, start_y
        
        for i in range(max_points):
            points.append((int(x), int(y)))
            
            # Mettre à jour la position (même physique que le projectile)
            x += vx
            y += vy
            vy += self.gravity
            
            # Appliquer les frottements si activés
            if air_friction:
                vx *= air_friction_coef
                vy *= air_friction_coef
            
            # Arrêter si on sort de l'écran (vers le bas)
            if y > 800:  # HEIGHT
                break
        
        return points
    
    def draw_trajectory(self, screen, points, color=(255, 255, 255), radius=2):
        """
        Dessine la trajectoire en pointillés
        
        Args:
            screen: Surface pygame où dessiner
            points: Liste de points (x, y)
            color: Couleur des points
            radius: Rayon des points
        """
        # Dessiner un point tous les 5 points pour effet pointillé
        for i, point in enumerate(points):
            if i % 5 == 0:  # Espacer les points
                pygame.draw.circle(screen, color, point, radius)
