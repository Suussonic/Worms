import pygame
import numpy as np
import os
import random

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
        
        # --- GESTION DES SPRITES ---
        self.block_size = 20
        self.ground_img = None
        self.water_img = None
        
        # Chargement des textures
        try:
            if os.path.exists("image/ground.png"):
                img = pygame.image.load("image/ground.png").convert()
                self.ground_img = pygame.transform.scale(img, (self.block_size, self.block_size))
            
            if os.path.exists("image/water.png"):
                img = pygame.image.load("image/water.png").convert()
                self.water_img = pygame.transform.scale(img, (self.block_size, self.block_size))
        except Exception as e:
            print(f"Erreur chargement textures terrain: {e}")

        # Générer un terrain initial
        self.generate_terrain()
    
    def draw_block(self, x, y, type_block):
        """Dessine un bloc et met à jour le masque correspondant"""
        # Dessin
        if type_block == 'T': # Terre
            if self.ground_img:
                self.surface.blit(self.ground_img, (x, y))
            else:
                # Fallback couleur
                pygame.draw.rect(self.surface, (139, 90, 43), (x, y, self.block_size, self.block_size))
                pygame.draw.rect(self.surface, (110, 70, 30), (x, y, self.block_size, self.block_size), 1)
            
            # Mise à jour masque collision
            self.mask[int(x):int(x)+self.block_size, int(y):int(y)+self.block_size] = True
            
        elif type_block == 'W': # Eau
            if self.water_img:
                self.surface.blit(self.water_img, (x, y))
            else:
                # Fallback couleur
                pygame.draw.rect(self.surface, (30, 144, 255), (x, y, self.block_size, self.block_size))
                pygame.draw.rect(self.surface, (0, 100, 200), (x, y, self.block_size, self.block_size), 1)
            
            # Mise à jour masque eau
            self.water_mask[int(x):int(x)+self.block_size, int(y):int(y)+self.block_size] = True

    def load_from_file(self, filepath):
        """Charge un terrain depuis un fichier texte"""
        if not os.path.exists(filepath):
            print(f"Fichier terrain introuvable : {filepath}")
            self.generate_terrain()
            return
        
        # Réinitialiser
        self.surface.fill((0, 0, 0))
        self.mask.fill(False)
        self.water_mask.fill(False)
        
        try:
            with open(filepath, 'r') as f:
                lines = f.readlines()
            
            for row_idx, line in enumerate(lines):
                line = line.rstrip('\n')
                for col_idx, char in enumerate(line):
                    x = col_idx * self.block_size
                    y = row_idx * self.block_size
                    
                    if char == 'T':
                        self.draw_block(x, y, 'T')
                    elif char == 'W':
                        self.draw_block(x, y, 'W')
                        
        except Exception as e:
            print(f"Erreur lors du chargement du terrain : {e}")
            self.generate_terrain()
    
    def generate_terrain(self):
        """Génère un terrain avec des blocs carrés aléatoires et de l'eau en bas"""
        # Réinitialiser
        self.surface.fill((0, 0, 0))
        self.mask.fill(False)
        self.water_mask.fill(False)
        
        # Calculer le nombre de colonnes et lignes
        num_columns = self.width // self.block_size
        
        # Créer une couche d'eau en bas (2 blocs de hauteur)
        water_height = 2
        for col in range(num_columns):
            x = col * self.block_size
            for row in range(water_height):
                y = self.height - (row + 1) * self.block_size
                self.draw_block(x, y, 'W')
        
        # Générer le terrain avec transitions plus douces
        ground_base = self.height // 2
        
        # Générer les hauteurs avec lissage
        current_height = ground_base // self.block_size
        
        for col in range(num_columns):
            # Variation plus petite pour terrain plus lisse
            variation = random.randint(-1, 1)
            current_height += variation
            # Limiter entre 8 et 25 blocs de hauteur
            current_height = max(8, min(current_height, 25))
            
            x = col * self.block_size
            
            # Dessiner une colonne de terre jusqu'au niveau de l'eau
            for row in range(current_height):
                y = self.height - (row + water_height + 1) * self.block_size
                if y >= 0:
                    self.draw_block(x, y, 'T')
    
    def is_solid(self, x, y):
        """Vérifie si une position contient du terrain solide"""
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            return False
        return self.mask[int(x), int(y)]
    
    def is_water(self, x, y):
        """Vérifie si une position contient de l'eau"""
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            return False
        return self.water_mask[int(x), int(y)]
    
    def create_crater(self, x, y, radius=30):
        """Crée un cratère circulaire dans le terrain"""
        # Dessiner un cercle noir (transparent) pour créer le cratère
        pygame.draw.circle(self.surface, (0, 0, 0), (int(x), int(y)), radius)
        
        # Mettre à jour le masque dans la zone du cratère
        min_x = max(0, int(x - radius))
        max_x = min(self.width, int(x + radius + 1))
        min_y = max(0, int(y - radius))
        max_y = min(self.height, int(y + radius + 1))
        
        for px in range(min_x, max_x):
            for py in range(min_y, max_y):
                if (px - x)**2 + (py - y)**2 <= radius**2:
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
