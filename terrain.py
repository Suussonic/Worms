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
        
        # Créer un masque pour l'eau (tableau 2D)
        self.water_mask = np.zeros((width, height), dtype=bool)
        
        # Générer un terrain initial
        self.generate_terrain()
    
    def load_from_file(self, filepath):
        # Charge un terrain depuis un fichier texte
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
                    x = col_idx * block_size
                    y = row_idx * block_size
                    
                    if char == 'T':  # T = Terre
                        # Dessiner le bloc de terre
                        pygame.draw.rect(self.surface, (139, 90, 43), (x, y, block_size, block_size))
                        pygame.draw.rect(self.surface, (110, 70, 30), (x, y, block_size, block_size), 1)
                    elif char == 'W':  # W = Eau
                        # Dessiner le bloc d'eau
                        pygame.draw.rect(self.surface, (30, 144, 255), (x, y, block_size, block_size))
                        pygame.draw.rect(self.surface, (0, 100, 200), (x, y, block_size, block_size), 1)
            
            # Mettre à jour les masques de collision et d'eau
            self.update_mask()
        except Exception as e:
            print(f"Erreur lors du chargement du terrain : {e}")
            self.generate_terrain()
    
    def generate_terrain(self):
        # Génère un terrain avec des blocs carrés aléatoires et de l'eau en bas
        import random
        
        # Remplir le fond
        self.surface.fill((0, 0, 0))
        
        # Taille des blocs
        block_size = 20
        
        # Calculer le nombre de colonnes et lignes
        num_columns = self.width // block_size
        num_rows = self.height // block_size
        
        # Créer une couche d'eau en bas (2 blocs de hauteur)
        water_height = 2
        for col in range(num_columns):
            x = col * block_size
            for row in range(water_height):
                y = self.height - (row + 1) * block_size
                pygame.draw.rect(self.surface, (30, 144, 255), (x, y, block_size, block_size))
                pygame.draw.rect(self.surface, (0, 100, 200), (x, y, block_size, block_size), 1)
        
        # Générer le terrain avec transitions plus douces
        ground_base = self.height // 2  # Hauteur de base du terrain (milieu de l'écran)
        heights = []  # Stocker les hauteurs pour chaque colonne
        
        # Générer les hauteurs avec lissage
        current_height = ground_base // block_size
        for col in range(num_columns):
            # Variation plus petite pour terrain plus lisse
            variation = random.randint(-1, 1)  # Changement plus doux
            current_height += variation
            # Limiter entre 8 et 25 blocs de hauteur (laisser de l'espace)
            current_height = max(8, min(current_height, 25))
            heights.append(current_height)
        
        # Dessiner le terrain
        for col in range(num_columns):
            height_in_blocks = heights[col]
            x = col * block_size
            
            # Dessiner une colonne de terre jusqu'au niveau de l'eau
            for row in range(height_in_blocks):
                y = self.height - (row + water_height + 1) * block_size
                if y >= 0:  # Vérifier qu'on ne dépasse pas en haut
                    pygame.draw.rect(self.surface, (139, 90, 43), (x, y, block_size, block_size))
                    pygame.draw.rect(self.surface, (110, 70, 30), (x, y, block_size, block_size), 1)
        
        # Mettre à jour les masques
        self.update_mask()
    
    def update_mask(self):
        # Met à jour les masques de collision et d'eau basés sur la surface
        # Parcourir tous les pixels et marquer ceux qui sont solides ou de l'eau
        for x in range(self.width):
            for y in range(self.height):
                color = self.surface.get_at((x, y))
                # Terre (marron)
                if color[:3] == (139, 90, 43):
                    self.mask[x, y] = True
                    self.water_mask[x, y] = False
                # Eau (bleu)
                elif color[:3] == (30, 144, 255):
                    self.mask[x, y] = False  # L'eau n'est pas solide
                    self.water_mask[x, y] = True
                else:
                    self.mask[x, y] = False
                    self.water_mask[x, y] = False
    
    def is_solid(self, x, y):
        # Vérifie si une position contient du terrain solide
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            return False
        return self.mask[int(x), int(y)]
    
    def is_water(self, x, y):
        # Vérifie si une position contient de l'eau
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            return False
        return self.water_mask[int(x), int(y)]
    
    def create_crater(self, x, y, radius=30):
        # Crée un cratère circulaire dans le terrain
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
        # Retourne la hauteur du sol à une position x donnée
        if x < 0 or x >= self.width:
            return self.height
        
        # Chercher de haut en bas le premier pixel solide
        for y in range(self.height):
            if self.is_solid(x, y):
                return y
        return self.height
    
    def draw(self, screen):
        # Dessine le terrain sur l'écran
        screen.blit(self.surface, (0, 0))
