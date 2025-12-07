import math
import pygame

class TrajectoryCalculator:
    """Classe pour calculer et afficher les trajectoires de projectiles"""
    
    def __init__(self, gravity=0.5):
        self.gravity = gravity
    
    def calculate_trajectory_points(self, start_x, start_y, angle, power, max_points=100):
        """
        Calcule les points de la trajectoire d'un projectile
        
        Args:
            start_x, start_y: Position de départ
            angle: Angle de tir en degrés
            power: Puissance du tir
            max_points: Nombre maximum de points à calculer
            
        Returns:
            Liste de tuples (x, y) représentant la trajectoire
        """
        points = []
        
        # Convertir l'angle en radians et calculer les vitesses initiales
        angle_rad = math.radians(angle)
        vx = power * math.cos(angle_rad)
        vy = power * math.sin(angle_rad)
        
        # Simuler la trajectoire
        x, y = start_x, start_y
        
        for i in range(max_points):
            points.append((int(x), int(y)))
            
            # Mettre à jour la position (même physique que le projectile)
            x += vx
            y += vy
            vy += self.gravity
            
            # Arrêter si on sort de l'écran (vers le bas)
            if y > 600:  # HEIGHT
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
