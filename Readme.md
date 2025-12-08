# Worms - Jeu de Tir Balistique

## 📖 Description du Projet

Ce projet est un clone simplifié du célèbre jeu **Worms**, développé en Python avec Pygame. Le joueur contrôle un personnage (ver vert) qui doit éliminer un ennemi (ver rouge) en utilisant des projectiles balistiques. Le jeu intègre des calculs de trajectoire réalistes basés sur la physique, un terrain destructible, et un système de combat tactique.

### Objectifs pédagogiques
- Simuler des trajectoires balistiques avec et sans frottements de l'air
- Implémenter un terrain destructible avec détection de collision
- Gérer la physique du jeu (gravité, vélocité, forces)
- Créer une interface utilisateur interactive

---

## 🎮 Contrôles du Jeu

### Menu principal
- **Clic sur "JOUER"** : Démarrer une nouvelle partie

### Pendant le jeu
- **← / →** ou **Q / D** : Déplacer le personnage
- **Espace** : Sauter
- **↑ / ↓** : Ajuster l'angle de tir (de -90° à 90°)
- **Maintenir Entrée** : Charger la puissance du tir (0 à 20)
- **Relâcher Entrée** : Tirer le projectile

### Écran de fin
- **Clic sur "REJOUER"** : Recommencer une nouvelle partie avec un nouveau terrain

---

## 📁 Structure des Fichiers

### Fichiers principaux

#### `main.py`
**Rôle** : Boucle principale du jeu et gestion des événements
- Initialisation de Pygame et de la fenêtre
- Gestion des états du jeu (menu, en cours, game over)
- Boucle d'événements et mise à jour des entités
- Détection des collisions projectile-terrain et projectile-ennemi

#### `UI.py`
**Rôle** : Interface utilisateur et affichage graphique
- `draw_menu()` : Écran de démarrage avec bouton "JOUER"
- `draw_hud()` : Affichage de l'angle et de la puissance
- `draw_aim_line()` : Ligne de visée jaune
- `draw_trajectory()` : Trajectoire prédite en pointillés
- `draw_game_over()` : Écran de victoire/défaite avec bouton "REJOUER"

### Fichiers de gameplay

#### `character.py`
**Rôle** : Classe `Worm` représentant le joueur
```python
class Worm:
    def __init__(self, x, y, width, height):
        self.velocity = pygame.math.Vector2(0, 0)
        self.GRAVITY = 0.8
        self.JUMP_FORCE = -15
        self.hp = 100
        self.aim_angle = 0
```
- Gestion du déplacement horizontal et du saut
- Application de la gravité et collision avec le terrain
- Système de points de vie et de visée

#### `enemy.py`
**Rôle** : Classe `Enemy` représentant l'adversaire
- Même système physique que le joueur (gravité, collision)
- Affichage des HP au-dessus du personnage
- Méthodes `take_damage()` et `is_alive()`

#### `gun.py`
**Rôle** : Classe `Projectile` pour les munitions
```python
class Projectile:
    def __init__(self, x, y, angle, power):
        angle_rad = math.radians(angle)
        self.velocity_x = power * math.cos(angle_rad)
        self.velocity_y = power * math.sin(angle_rad)
        self.GRAVITY = 0.5
```
- Calcul des composantes de vitesse à partir de l'angle et de la puissance
- Application de la gravité à chaque frame
- Détection de collision avec rectangles

### Fichiers de physique

#### `trajectory.py`
**Rôle** : Calcul et affichage des trajectoires prédites
```python
def calculate_trajectory_points(self, start_x, start_y, angle, power):
    angle_rad = math.radians(angle)
    vx = power * math.cos(angle_rad)
    vy = power * math.sin(angle_rad)
    
    for i in range(max_points):
        x += vx
        y += vy
        vy += self.gravity  # Accélération gravitationnelle
```
- Simulation frame par frame de la trajectoire
- Affichage en pointillés pour prévisualiser le tir

#### `terrain.py`
**Rôle** : Génération et gestion du terrain destructible
```python
class Terrain:
    def __init__(self, width, height):
        self.mask = np.zeros((width, height), dtype=bool)  # Masque de collision
        self.generate_terrain()  # Génération procédurale
    
    def create_crater(self, x, y, radius=30):
        # Créer un cercle de destruction
        for dx in range(-radius, radius + 1):
            for dy in range(-radius, radius + 1):
                if dx*dx + dy*dy <= radius*radius:
                    self.mask[px, py] = False
```
- Génération aléatoire de collines avec polygones
- Masque booléen pour la détection de collision pixel-perfect
- Destruction circulaire du terrain lors des impacts

---

## 🔬 Équations Mathématiques Importantes

### 1. Décomposition de la vitesse initiale

Lorsqu'un projectile est tiré avec un angle θ et une puissance P :

```
vx = P × cos(θ)
vy = P × sin(θ)
```

**Application dans le code** (`gun.py`) :
```python
angle_rad = math.radians(angle)
self.velocity_x = power * math.cos(angle_rad)
self.velocity_y = power * math.sin(angle_rad)
```

### 2. Mouvement balistique avec gravité

À chaque frame (dt), la position et la vitesse sont mises à jour :

```
vy(t+dt) = vy(t) + g × dt
x(t+dt) = x(t) + vx × dt
y(t+dt) = y(t) + vy × dt
```

Où g = 0.5 ou 0.8 selon l'objet (constante de gravité)

**Application dans le code** (`gun.py`, `character.py`) :
```python
def update(self):
    self.velocity_y += self.GRAVITY  # Accélération
    self.x += self.velocity_x         # Déplacement horizontal
    self.y += self.velocity_y         # Déplacement vertical
```

### 3. Équation de la trajectoire parabolique

Pour un projectile sans frottements, la trajectoire suit :

```
y = y₀ + x×tan(θ) - (g×x²)/(2×v₀²×cos²(θ))
```

Cette équation n'est pas directement codée, mais **simulée itérativement** dans `trajectory.py` pour prédire la trajectoire avant le tir.

### 4. Détection de collision circulaire (cratères)

Pour créer un cratère circulaire de rayon R :

```
distance² = dx² + dy²
Si distance² ≤ R², alors détruire le pixel
```

**Application dans le code** (`terrain.py`) :
```python
for dx in range(-radius, radius + 1):
    for dy in range(-radius, radius + 1):
        if dx*dx + dy*dy <= radius*radius:
            self.mask[px, py] = False  # Détruire le pixel
```

### 5. Collision rectangle-rectangle (AABB)

Détection entre le projectile et les personnages :

```python
def check_collision(self, target_rect):
    projectile_rect = pygame.Rect(self.x - self.radius, 
                                   self.y - self.radius,
                                   self.radius * 2, 
                                   self.radius * 2)
    return projectile_rect.colliderect(target_rect)
```

Utilise l'algorithme **AABB (Axis-Aligned Bounding Box)** de Pygame.

---

## 🚀 Fonctionnalités Implémentées

- ✅ Menu de démarrage
- ✅ Système de trajectoire balistique réaliste
- ✅ Prédiction de trajectoire en pointillés
- ✅ Terrain destructible avec cratères
- ✅ Collision personnage-terrain pixel-perfect
- ✅ Système de points de vie (100 HP)
- ✅ Gravité et physique du saut
- ✅ Écran de victoire/défaite
- ✅ Bouton rejouer avec nouveau terrain

---

## 🎯 Améliorations Possibles

D'après le cahier des charges initial (`ToDO.md`), voici les fonctionnalités avancées à implémenter :

### Projectiles avancés
- **Roquette** : Vitesse élevée, impact unique, destruction importante
- **Grenade** : Vitesse faible, rebonds multiples, explosion après 5s
- **Frottements de l'air** : Force proportionnelle à v²

### Effets environnementaux
- **Vent** : Force horizontale affectant les projectiles
- **Parachute** : Ralentissement de la chute
- **Grappin** : Déplacement vertical du personnage

### Physique avancée
- **Frottements aqueux** : Si projectile dans l'eau
- **Poussée d'Archimède** : Flottabilité
- **Gravité variable** : Champ gravitationnel non uniforme

---

## 📦 Dépendances

```
pygame==2.6.1
numpy (pour le masque de terrain)
```

Installation :
```bash
pip install pygame numpy
```

---

## ▶️ Lancer le Jeu

```bash
python main.py
```