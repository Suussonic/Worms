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
    
    def load_from_file(self, filepath):
        """Charge un terrain depuis un fichier texte"""
        import os
        
        if not os.path.exists(filepath):
            print(f"Fichier terrain introuvable : {filepath}")
            self.generate_terrain()
            return
        
        # Remplir le fond
        self.surface.fill((0, 0, 0))
        
        # Taille des blocs
        block_size = 20
        
        try:
            with open(filepath, 'r') as f:
                lines = f.readlines()
            
            for row_idx, line in enumerate(lines):
                line = line.rstrip('\n')
                for col_idx, char in enumerate(line):
                    if char == 'T':  # T = Terre
                        x = col_idx * block_size
                        y = row_idx * block_size
                        # Dessiner le bloc
                        pygame.draw.rect(self.surface, (139, 90, 43), (x, y, block_size, block_size))
                        pygame.draw.rect(self.surface, (110, 70, 30), (x, y, block_size, block_size), 1)
            
            # Mettre à jour le masque de collision
            self.update_mask()
        except Exception as e:
            print(f"Erreur lors du chargement du terrain : {e}")
            self.generate_terrain()
    
    def generate_terrain(self):
        """Génère un terrain avec des blocs carrés aléatoires"""
        import random
        
        # Remplir le fond
        self.surface.fill((0, 0, 0))
        
        # Taille des blocs
        block_size = 20
        
        # Calculer le nombre de colonnes
        num_columns = self.width // block_size
        
        # Générer la hauteur pour chaque colonne
        ground_base = self.height // 3  # Hauteur de base du terrain
        
        for col in range(num_columns):
            # Variation aléatoire pour créer des collines
            variation = random.randint(-3, 3)  # Variation en nombre de blocs
            height_in_blocks = (ground_base // block_size) + variation
            height_in_blocks = max(5, min(height_in_blocks, self.height // block_size))  # Limiter
            
            # Dessiner une colonne de blocs
            x = col * block_size
            for row in range(height_in_blocks):
                y = self.height - (row + 1) * block_size
                # Dessiner le bloc avec une bordure pour voir les carrés
                pygame.draw.rect(self.surface, (139, 90, 43), (x, y, block_size, block_size))
                pygame.draw.rect(self.surface, (110, 70, 30), (x, y, block_size, block_size), 1)  # Bordure
        
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
