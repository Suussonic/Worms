import pygame
import numpy as np

class Terrain:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        
        # Créer une surface pour le terrain
        self.surface = pygame.Surface((width, height))
        self.surface.set_colorkey((0, 0, 0))  # Noir = transparent
        
        # Créer un masque de collision (tableau 2D)
        self.mask = np.zeros((width, height), dtype=bool)
        
        # Générer un terrain initial
        self.generate_terrain()
    
    def generate_terrain(self):
        """Génère un terrain avec des collines aléatoires"""
        import random
        
        # Remplir le fond
        self.surface.fill((0, 0, 0))
        
        # Créer des points pour les collines
        points = []
        ground_height = self.height // 3  # Hauteur de base du terrain
        
        # Générer des points pour créer des collines
        num_points = 20
        for i in range(num_points + 1):
            x = (self.width // num_points) * i
            # Variation aléatoire pour créer des collines
            variation = random.randint(-50, 50)
            y = self.height - ground_height + variation
            y = max(self.height // 2, min(self.height, y))  # Limiter la hauteur
            points.append((x, y))
        
        # Dessiner le terrain
        if len(points) > 2:
            # Créer un polygone pour le terrain
            terrain_points = points + [(self.width, self.height), (0, self.height)]
            pygame.draw.polygon(self.surface, (139, 90, 43), terrain_points)  # Couleur marron
        
        # Mettre à jour le masque de collision
        self.update_mask()
    
    def update_mask(self):
        """Met à jour le masque de collision basé sur la surface"""
        # Parcourir tous les pixels et marquer ceux qui sont solides
        for x in range(self.width):
            for y in range(self.height):
                color = self.surface.get_at((x, y))
                # Si le pixel n'est pas noir (transparent), c'est du terrain solide
                self.mask[x, y] = color[:3] != (0, 0, 0)
    
    def is_solid(self, x, y):
        """Vérifie si une position contient du terrain solide"""
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            return False
        return self.mask[int(x), int(y)]
    
    def create_crater(self, x, y, radius=30):
        """Crée un cratère circulaire dans le terrain"""
        # Dessiner un cercle noir (transparent) pour créer le cratère
        pygame.draw.circle(self.surface, (0, 0, 0), (int(x), int(y)), radius)
        
        # Mettre à jour le masque dans la zone du cratère
        for dx in range(-radius, radius + 1):
            for dy in range(-radius, radius + 1):
                if dx*dx + dy*dy <= radius*radius:
                    px, py = int(x + dx), int(y + dy)
                    if 0 <= px < self.width and 0 <= py < self.height:
                        self.mask[px, py] = False
    
    def get_ground_height(self, x):
        """Retourne la hauteur du sol à une position x donnée"""
        if x < 0 or x >= self.width:
            return self.height
        
        # Chercher de haut en bas le premier pixel solide
        for y in range(self.height):
            if self.is_solid(x, y):
                return y
        return self.height
    
    def draw(self, screen):
        """Dessine le terrain sur l'écran"""
        screen.blit(self.surface, (0, 0))
