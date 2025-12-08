# Worms - Jeu de Tir Balistique Multi-joueurs

## Description du Projet

Clone du célèbre jeu **Worms** développé en Python avec Pygame. Les joueurs contrôlent des vers et doivent éliminer les équipes adverses en utilisant des projectiles balistiques. Le jeu intègre physique réaliste, terrain destructible, système multi-joueurs et plusieurs armes.

### Caractéristiques
- Mode multi-joueurs (2+ joueurs, 1+ vers par joueur)
- Trois armes : Roquette, Grenade avec rebonds, Parachute
- Terrain destructible avec eau mortelle
- Physique réaliste avec frottements d'air optionnels
- Interface complète : menus, configuration, paramètres, pause
- Système de tours avec timer (20 secondes)
- Personnalisation des touches de contrôle

---

## Contrôles du Jeu

### Menu principal
- **JOUER** : Accéder à la configuration de partie
- **PARAMETRES** : Personnaliser les touches
- **QUITTER** : Fermer le jeu

### Configuration de partie
- **Boutons +/-** : Ajuster nombre de joueurs (minimum 2)
- **Boutons +/-** : Ajuster nombre de vers par joueur (minimum 1)
- **Flèches < >** : Sélectionner un terrain (aléatoire ou prédéfini)
- **COMMENCER** : Lancer la partie

### En jeu
- **Flèches Gauche/Droite** : Déplacer le ver actif
- **Espace** : Sauter
- **Flèches Haut/Bas** : Ajuster l'angle de tir (-180° à 90°)
- **Maintenir Entrée** : Charger la puissance (0 à 20)
- **Relâcher Entrée** : Tirer le projectile
- **Clic droit ou TAB** : Ouvrir le menu de sélection d'arme
- **ESC** : Mettre en pause

### Menu d'arme
- **Roquette** : Tir direct, cratère moyen (30px), dégâts 20 HP
- **Grenade** : Rebondit, explose après 5s ou 10 rebonds, cratère 40px, dégâts jusqu'à 50 HP
- **Frottements d'air** : Activer/désactiver (coefficient 0.98)

### Menu pause
- **CONTINUER** : Reprendre la partie
- **PARAMETRES** : Modifier les touches
- **QUITTER** : Retour au menu principal

### Écran de fin
- **REJOUER** : Relancer une partie avec le même terrain

---

## Structure du Code

### Fichiers principaux

#### `main.py`
Boucle principale et logique de jeu
- Initialisation Pygame, fenêtre 1200x800, 60 FPS
- États : menu, configuration, jeu, pause, game over
- Système multi-joueurs avec rotation des tours (20s par tour)
- Gestion projectiles, collisions, dégâts
- Timer visible avec alerte rouge (< 5 secondes)
- Système de parachute partagé par joueur

#### `UI.py`
Interface utilisateur et rendu graphique
- `draw_menu()` : Menu principal avec 3 boutons
- `draw_game_setup()` : Configuration joueurs/vers/terrain
- `draw_settings()` : Personnalisation des touches
- `draw_pause_menu()` : Menu pause
- `draw_hud()` : Affichage angle, puissance, timer
- `draw_aim_line()` : Ligne de visée
- `draw_trajectory()` : Trajectoire prédite en pointillés
- `draw_weapon_menu()` : Menu de sélection d'arme
- `draw_game_over()` : Écran de victoire

### Fichiers de gameplay

#### `character.py`
Classe `Worm` - Ver de jeu
- Physique : Déplacement, saut (force -8), gravité (0.8)
- Collision terrain avec détection pixel-perfect
- Système HP : 100 max, mort dans l'eau instantanée
- Visée : Angle -180° à 90°, puissance 0-20
- Armes : Sélection roquette/grenade par ver
- Sprite : Chargement image avec flip horizontal automatique
- Nom aléatoire parmi 15 prénoms

#### `gun.py`
Classe `Projectile` - Roquette
- Vitesse initiale : vx = P×cos(θ), vy = P×sin(θ)
- Gravité : 0.5 par frame
- Frottements d'air optionnels : coefficient 0.98
- Rayon : 5 pixels
- Collision avec terrain et vers
- Cratère : 30 pixels de rayon

#### `grenade.py`
Classe `Grenade` - Grenade avec rebonds
- Vitesse : 60% de la roquette
- Timer : 5 secondes avant explosion
- Rebonds : Amortissement 60%, friction sol 80%
- Explose si : timer écoulé, 10 rebonds, vitesse < 0.5
- Pause/reprise du timer
- Affichage temps restant
- Cratère : 40 pixels, dégâts max 50 HP (formule quadratique)

### Fichiers de physique

#### `trajectory.py`
Classe `TrajectoryCalculator` - Calcul de trajectoires
- Simulation itérative frame par frame
- Support grenades : vitesse réduite à 60%
- Support frottements d'air : coefficient 0.98
- Affichage pointillés : 1 point tous les 5
- Limite : 100 points ou sortie d'écran (y > 800)
- Couleur différente selon arme (rouge/vert)

#### `terrain.py`
Classe `Terrain` - Terrain destructible
- Génération procédurale par blocs 20x20 pixels
- Hauteurs lissées : variation ±1 bloc entre colonnes
- Limite hauteur : 8 à 25 blocs (espace en haut/bas)
- Eau mortelle : 2 blocs en bas (mort instantanée)
- Chargement fichiers .txt : T=terre, W=eau, #=vide
- Masque collision : numpy array booléen (width × height)
- Masque eau séparé du masque terrain
- Cratères circulaires : formule dx²+dy² ≤ r²

---

## Formules Mathématiques

### 1. Vitesse initiale du projectile
```
vx = P × cos(θ)
vy = P × sin(θ)
```
Code (`gun.py`) :
```python
angle_rad = math.radians(angle)
self.velocity_x = power * math.cos(angle_rad)
self.velocity_y = power * math.sin(angle_rad)
```

### 2. Mouvement avec gravité
```
vy(t+1) = vy(t) + g
x(t+1) = x(t) + vx
y(t+1) = y(t) + vy
```
Gravité : g = 0.5 (projectiles) ou 0.8 (vers)

Code (`gun.py`, `character.py`) :
```python
self.velocity_y += self.GRAVITY
self.x += self.velocity_x
self.y += self.velocity_y
```

### 3. Frottements d'air
```
vx(t+1) = vx(t) × k
vy(t+1) = (vy(t) + g) × k
```
Coefficient k = 0.98

Code (`gun.py`, `grenade.py`) :
```python
self.velocity_y += self.GRAVITY
if self.air_friction:
    self.velocity_x *= self.AIR_FRICTION_COEF
    self.velocity_y *= self.AIR_FRICTION_COEF
```

### 4. Rebonds des grenades
```
vy_après = -vy_avant × d
vx_après = vx_avant × f
```
Amortissement d = 0.6, friction sol f = 0.8

Code (`grenade.py`) :
```python
self.velocity_y = -self.velocity_y * self.bounce_damping
self.velocity_x *= 0.8
```

### 5. Collision circulaire (cratères)
```
Si dx² + dy² ≤ R² alors détruire pixel
```
Code (`terrain.py`) :
```python
for dx in range(-radius, radius + 1):
    for dy in range(-radius, radius + 1):
        if dx*dx + dy*dy <= radius*radius:
            self.mask[px, py] = False
```

### 6. Dégâts d'explosion
```
ratio = distance / rayon_max
damage = damage_max × (1 - ratio)²
```
Minimum 5 HP, maximum 50 HP

Code (`main.py`) :
```python
distance_ratio = distance / explosion_radius
damage = int(max_damage * (1 - distance_ratio) ** 2)
damage = max(5, damage)
```

---

## Fonctionnalités Implémentées

### Système de jeu
- Menu principal : Jouer, Paramètres, Quitter
- Configuration partie : joueurs (2+), vers/joueur (1+), terrains
- Sélection terrain : aléatoire ou fichiers .txt prédéfinis
- Menu pause (ESC) avec accès paramètres
- Écran victoire avec bouton rejouer
- Rotation automatique des tours (20s par tour)
- Timer visible avec alerte rouge (< 5s)
- Affichage noms des vers (15 prénoms aléatoires)

### Armes et combat
- Roquette : Impact direct, cratère 30px, 20 HP de dégâts
- Grenade : Rebonds amortis, explosion après 5s ou 10 rebonds, cratère 40px, jusqu'à 50 HP
- Menu sélection arme : Clic droit ou TAB
- Frottements d'air : Option activable/désactivable (coef 0.98)
- Prédiction trajectoire : Pointillés colorés selon arme

### Physique et terrain
- Trajectoire balistique réaliste
- Terrain destructible avec cratères circulaires
- Génération procédurale avec hauteurs lissées
- Eau mortelle (mort instantanée)
- Collision pixel-perfect (masques numpy)
- Rebonds grenades avec amortissement
- Gravité différenciée : 0.5 (projectiles), 0.8 (vers)

### Interface utilisateur
- HUD complet : Angle, puissance, timer, HP
- Ligne de visée orientable
- Sprites vers avec flip horizontal
- Personnalisation touches complète
- Visualisation terrain avant partie
- Affichage temps restant grenades
- Distinction visuelle par couleur (armes, alertes)

---

## Installation

### Prérequis
```bash
pip install pygame numpy
```

### Lancer le jeu
```bash
python main.py
```

### Format fichiers terrain
Dossier `terrains/` - Fichiers .txt 60×40 caractères :
- `T` : Terre (bloc solide marron, 20×20px)
- `W` : Eau (bloc bleu mortel, 20×20px)
- `#` : Vide (transparent)

---

## Convention de Code

Tous les commentaires utilisent le format `#` :
```python
# Commentaire simple pour expliquer le code
def fonction():
    # Description de ce que fait la fonction
    x = 5  # Commentaire inline
```

Pas de docstrings `"""` dans le code pour plus de cohérence.

---

## ▶️ Lancer le Jeu

```bash
python main.py
```