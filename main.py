import os
import pygame
import math
from character import Worm
from gun import Projectile
from grenade import Grenade
from trajectory import TrajectoryCalculator
from terrain import Terrain
from UI import UI

pygame.init()

WIDTH, HEIGHT = 1200, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# États du jeu
in_menu = True
in_game_setup = False
in_settings = False
is_paused = False
waiting_for_key = False
key_to_change = None

# Configuration de partie
num_players = 2
worms_per_player = 1
selected_terrain = 0  # Index du terrain sélectionné

# Scanner le dossier terrains pour obtenir la liste des fichiers .txt
def get_terrain_files():
    terrain_list = ["random"]  # Toujours avoir l'option aléatoire en premier
    terrain_dir = "terrains"
    if os.path.exists(terrain_dir):
        for filename in sorted(os.listdir(terrain_dir)):
            if filename.endswith('.txt'):
                terrain_list.append(os.path.join(terrain_dir, filename))
    return terrain_list

terrain_files = get_terrain_files()

# Contrôles par défaut
controls = {
    'left': pygame.K_LEFT,
    'right': pygame.K_RIGHT,
    'jump': pygame.K_SPACE,
    'aim_up': pygame.K_UP,
    'aim_down': pygame.K_DOWN,
    'shoot': pygame.K_RETURN,
    'weapon_menu': pygame.K_TAB  # Touche pour ouvrir le menu d'arme (alternative au clic droit)
}

# Variables de jeu
game_over = False
winner = None

# Gestion des joueurs et vers
players_worms = {}  # Dictionnaire: {"p1": [worm1, worm2, ...], "p2": [...], ...}
current_player_index = 0  # Index du joueur actuel
current_worm_index = {}  # Index du ver actuel pour chaque joueur
player_names = []  # Liste des noms de joueurs ("p1", "p2", ...)

# Gestion du tir
charging_power = 0
is_charging = False

# Menu d'arme
weapon_menu_open = False

# Liste des projectiles
projectiles = []

# Dernier joueur qui a tiré
last_shooter = None

# Timer de tour
turn_time_limit = 20  # Secondes par tour
turn_start_time = 0  # Temps de début du tour
time_remaining = turn_time_limit


def init_game():
    """Réinitialise la partie"""
    global terrain, players_worms, projectiles, player_names
    global charging_power, is_charging, game_over, winner
    global current_player_index, current_worm_index, last_shooter
    global turn_start_time, time_remaining, weapon_menu_open

    terrain = Terrain(WIDTH, HEIGHT)
    
    # Charger le terrain sélectionné
    if selected_terrain == 0 or terrain_files[selected_terrain] == "random":
        terrain.generate_terrain()
    else:
        terrain.load_from_file(terrain_files[selected_terrain])
    
    # Liste des prénoms disponibles
    import random
    available_names = [
        "Mathieu", "Yanis", "Satya", "Raphaël", "Phileas",
        "Abdel Aziz", "Emma", "Ana", "Tanguy", "Abdoullah",
        "Thomas", "Titouan", "Robin", "Paul", "Yohan"
    ]
    
    # Mélanger les noms
    random.shuffle(available_names)
    name_index = 0
    
    # Créer les joueurs et leurs vers
    players_worms = {}
    player_names = [f"p{i+1}" for i in range(num_players)]
    current_worm_index = {}
    
    for i, player_name in enumerate(player_names):
        players_worms[player_name] = []
        current_worm_index[player_name] = 0
        
        # Créer les vers pour ce joueur
        for j in range(worms_per_player):
            # Position X aléatoire avec une marge de 50 pixels des bords
            x_pos = random.randint(50, WIDTH - 50)
            y_pos = 100
            
            # Attribuer un nom aléatoire
            worm_name = available_names[name_index % len(available_names)]
            name_index += 1
            
            worm = Worm(x_pos, y_pos, 20, 40, name=worm_name)
            players_worms[player_name].append(worm)
    
    projectiles = []
    charging_power = 0
    is_charging = False
    game_over = False
    winner = None
    current_player_index = 0
    last_shooter = None
    turn_start_time = pygame.time.get_ticks()
    time_remaining = turn_time_limit
    weapon_menu_open = False

    print(f"Tour du joueur {player_names[0]}")


def get_current_player():
    """Retourne le nom du joueur actuel"""
    return player_names[current_player_index]

def get_current_worm():
    """Retourne le ver actif du joueur actuel"""
    player = get_current_player()
    worm_idx = current_worm_index[player]
    worms_list = players_worms[player]
    
    # Si le ver actuel est mort, trouver le prochain ver vivant
    if not worms_list[worm_idx].is_alive():
        for i in range(len(worms_list)):
            test_idx = (worm_idx + i) % len(worms_list)
            if worms_list[test_idx].is_alive():
                current_worm_index[player] = test_idx
                return worms_list[test_idx]
        # Aucun ver vivant pour ce joueur
        return None
    
    return worms_list[worm_idx]

def get_all_alive_worms():
    """Retourne tous les vers vivants"""
    alive_worms = []
    for player_worms in players_worms.values():
        alive_worms.extend([w for w in player_worms if w.is_alive()])
    return alive_worms

def next_turn():
    """Passe au tour suivant avec rotation du ver"""
    global current_player_index, current_worm_index, turn_start_time, time_remaining
    
    # Passer au joueur suivant
    current_player_index = (current_player_index + 1) % len(player_names)
    
    # Faire tourner le ver du joueur actuel
    player = get_current_player()
    current_worm_index[player] = (current_worm_index[player] + 1) % len(players_worms[player])
    
    # Réinitialiser le timer
    turn_start_time = pygame.time.get_ticks()
    time_remaining = turn_time_limit
    
    print(f"Tour du joueur {player} - Ver {current_worm_index[player] + 1}")

trajectory_calc = TrajectoryCalculator(gravity=0.5)

# Lancer une première fois
init_game()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # ---------------------------
        #  MENU PRINCIPAL
        # ---------------------------
        if in_menu and event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            play_button = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2 - 70, 300, 60)
            settings_button = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2 + 10, 300, 60)
            quit_button = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2 + 90, 300, 60)
            
            if play_button.collidepoint(mouse_pos):
                in_menu = False
                in_game_setup = True
            elif settings_button.collidepoint(mouse_pos):
                in_settings = True
                in_menu = False
            elif quit_button.collidepoint(mouse_pos):
                running = False
        
        # ---------------------------
        #  ÉCRAN DE CONFIGURATION
        # ---------------------------
        if in_game_setup and event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            
            # Calculer les positions des boutons
            minus_players = pygame.Rect(WIDTH // 2 - 100, 220, 50, 50)
            plus_players = pygame.Rect(WIDTH // 2 + 50, 220, 50, 50)
            minus_worms = pygame.Rect(WIDTH // 2 - 100, 370, 50, 50)
            plus_worms = pygame.Rect(WIDTH // 2 + 50, 370, 50, 50)
            prev_terrain = pygame.Rect(WIDTH // 2 - 200, 520, 50, 50)
            next_terrain = pygame.Rect(WIDTH // 2 + 150, 520, 50, 50)
            start_button = pygame.Rect(WIDTH // 2 - 120, HEIGHT - 100, 240, 60)
            
            if minus_players.collidepoint(mouse_pos) and num_players > 2:
                num_players -= 1
            elif plus_players.collidepoint(mouse_pos):
                num_players += 1
            elif minus_worms.collidepoint(mouse_pos) and worms_per_player > 1:
                worms_per_player -= 1
            elif plus_worms.collidepoint(mouse_pos):
                worms_per_player += 1
            elif prev_terrain.collidepoint(mouse_pos):
                selected_terrain = (selected_terrain - 1) % len(terrain_files)
            elif next_terrain.collidepoint(mouse_pos):
                selected_terrain = (selected_terrain + 1) % len(terrain_files)
            elif start_button.collidepoint(mouse_pos):
                in_game_setup = False
                init_game()
        
        # ---------------------------
        #  ÉCRAN SETTINGS
        # ---------------------------
        if in_settings and not waiting_for_key:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                
                # Calculer les positions des boutons (même logique que dans draw_settings)
                y_offset = 180
                control_keys = ['left', 'right', 'jump', 'aim_up', 'aim_down', 'shoot']
                
                for key in control_keys:
                    button_rect = pygame.Rect(WIDTH - 250, y_offset - 5, 150, 40)
                    if button_rect.collidepoint(mouse_pos):
                        waiting_for_key = True
                        key_to_change = key
                        break
                    y_offset += 60
                
                # Bouton retour
                back_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT - 80, 200, 50)
                if back_button.collidepoint(mouse_pos):
                    in_settings = False
                    if not is_paused:
                        in_menu = True
        
        # Attente d'une nouvelle touche
        if waiting_for_key and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                waiting_for_key = False
                key_to_change = None
            else:
                controls[key_to_change] = event.key
                waiting_for_key = False
                key_to_change = None
        
        # ---------------------------
        #  MENU PAUSE
        # ---------------------------
        # Appuyer sur Échap pendant le jeu pour mettre en pause
        if not in_menu and not in_game_setup and not in_settings and not game_over and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                is_paused = not is_paused
                # Mettre en pause ou reprendre les grenades
                for projectile in projectiles:
                    if isinstance(projectile, Grenade):
                        if is_paused:
                            projectile.pause()
                        else:
                            projectile.resume()
        
        # Clics dans le menu pause
        if is_paused and not in_settings and event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            continue_button = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2 - 70, 300, 60)
            settings_button = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2 + 10, 300, 60)
            quit_button = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2 + 90, 300, 60)
            
            if continue_button.collidepoint(mouse_pos):
                is_paused = False
                # Reprendre les grenades
                for projectile in projectiles:
                    if isinstance(projectile, Grenade):
                        projectile.resume()
            elif settings_button.collidepoint(mouse_pos):
                in_settings = True
            elif quit_button.collidepoint(mouse_pos):
                is_paused = False
                game_over = False
                in_menu = True

        # Clic sur le bouton REJOUER
        if game_over and event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            button_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 50, 200, 50)
            if button_rect.collidepoint(mouse_pos):
                init_game()
        
        # ---------------------------
        #  MENU SELECTION D'ARME
        # ---------------------------
        # Clic droit ou touche configurable pour ouvrir/fermer le menu d'arme
        if not game_over and not in_menu and not in_game_setup and not in_settings and not is_paused:
            # Clic droit
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                if len(projectiles) == 0:  # Seulement si pas de projectile en vol
                    weapon_menu_open = not weapon_menu_open
            
            # Touche configurable
            if event.type == pygame.KEYDOWN and event.key == controls['weapon_menu']:
                if len(projectiles) == 0:
                    weapon_menu_open = not weapon_menu_open
            
            # Clics dans le menu d'arme
            if weapon_menu_open and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Clic gauche
                mouse_pos = pygame.mouse.get_pos()
                current_worm = get_current_worm()
                
                if current_worm and current_worm.is_alive():
                    menu_x = current_worm.rect.centerx - 100
                    menu_y = current_worm.rect.top - 120
                    
                    # Boutons du menu (3 options)
                    rocket_button = pygame.Rect(menu_x, menu_y, 200, 30)
                    grenade_button = pygame.Rect(menu_x, menu_y + 35, 200, 30)
                    friction_button = pygame.Rect(menu_x, menu_y + 70, 200, 30)
                    
                    if rocket_button.collidepoint(mouse_pos):
                        current_worm.selected_weapon = "rocket"
                        weapon_menu_open = False
                    elif grenade_button.collidepoint(mouse_pos):
                        current_worm.selected_weapon = "grenade"
                        weapon_menu_open = False
                    elif friction_button.collidepoint(mouse_pos):
                        current_worm.air_friction_enabled = not current_worm.air_friction_enabled

        # ---------------------------
        #  GESTION DES TOUCHES
        # ---------------------------
        if not game_over and not in_menu and not in_game_setup and not in_settings and event.type == pygame.KEYDOWN:

            # Début de la charge du tir (touche configurable)
            if event.key == controls['shoot']:
                # On peut charger seulement si aucun projectile en vol
                if len(projectiles) == 0:
                    is_charging = True
                    charging_power = 0

        # Relâchement des touches
        if not game_over and not in_menu and not in_game_setup and not in_settings and event.type == pygame.KEYUP:
            # Tir quand on relâche la touche de tir
            if event.key == controls['shoot'] and is_charging and len(projectiles) == 0:
                current_worm = get_current_worm()
                current_player = get_current_player()
                
                # Créer le projectile en fonction de l'arme du ver
                if current_worm.selected_weapon == "rocket":
                    projectile = Projectile(
                        current_worm.rect.centerx,
                        current_worm.rect.centery,
                        current_worm.aim_angle,
                        charging_power,
                        owner=current_player,
                        air_friction=current_worm.air_friction_enabled
                    )
                else:  # grenade
                    projectile = Grenade(
                        current_worm.rect.centerx,
                        current_worm.rect.centery,
                        current_worm.aim_angle,
                        charging_power,
                        owner=current_player,
                        air_friction=current_worm.air_friction_enabled
                    )
                
                last_shooter = current_player
                projectiles.append(projectile)
                is_charging = False
                charging_power = 0
                weapon_menu_open = False  # Fermer le menu après le tir

    # ---------------------------
    #  MISE À JOUR DU JEU
    # ---------------------------
    if not game_over and not in_menu and not in_game_setup and not in_settings and not is_paused:
        
        # Mise à jour du timer
        current_time = pygame.time.get_ticks()
        elapsed_time = (current_time - turn_start_time) / 1000  # Convertir en secondes
        time_remaining = max(0, turn_time_limit - elapsed_time)
        
        # Si le temps est écoulé et aucun projectile en vol, passer au tour suivant
        if time_remaining <= 0 and len(projectiles) == 0:
            next_turn()

        # Charge de la puissance pendant que la touche est maintenue
        if is_charging:
            charging_power = min(charging_power + 0.2, 20)
        
        # Changement d'angle continu (touches maintenues)
        if len(projectiles) == 0:
            current_worm = get_current_worm()
            if current_worm and current_worm.is_alive():
                keys = pygame.key.get_pressed()
                
                # Flèche du bas -> angle monte (inversé)
                if keys[controls['aim_down']]:
                    current_worm.aim_angle = min(current_worm.aim_angle + 1, 90)
                
                # Flèche du haut -> angle descend (inversé)
                if keys[controls['aim_up']]:
                    current_worm.aim_angle = max(current_worm.aim_angle - 1, -180)

        # Déplacement du ver actif
        if len(projectiles) == 0:
            current_worm = get_current_worm()
            if current_worm and current_worm.is_alive():
                current_worm.handle_input(controls)

        # Mise à jour de tous les vers (gravité, collisions, etc.)
        for player_worms_list in players_worms.values():
            for worm in player_worms_list:
                worm.update(HEIGHT, terrain)
        
        # Vérifier si le ver actif est mort (tombé dans le vide) et passer au tour suivant
        current_worm = get_current_worm()
        if current_worm is None or not current_worm.is_alive():
            if len(projectiles) == 0:  # Seulement si aucun projectile en vol
                next_turn()

        # Vérifier si une équipe est éliminée
        alive_by_player = {}
        for player, worms_list in players_worms.items():
            alive_by_player[player] = sum(1 for w in worms_list if w.is_alive())
        
        # Compter combien d'équipes ont encore des vers vivants
        teams_alive = sum(1 for count in alive_by_player.values() if count > 0)
        
        if teams_alive <= 1:
            game_over = True
            # Trouver le gagnant
            for player, count in alive_by_player.items():
                if count > 0:
                    winner = player
                    break
            else:
                winner = "draw"

    # ---------------------------
    #  MISE À JOUR DES PROJECTILES
    # ---------------------------
    for projectile in projectiles[:]:
        # Les grenades gèrent leurs propres collisions avec le terrain
        if isinstance(projectile, Grenade):
            projectile.update(terrain)
            
            # Si la grenade a explosé (plus active)
            if not projectile.active:
                terrain.create_crater(projectile.x, projectile.y, radius=40)
                
                # Dégâts aux vers proches de l'explosion
                explosion_radius = 80  # Rayon d'effet augmenté
                max_damage = 50  # Dégâts maximum au centre
                for player, worms_list in players_worms.items():
                    for worm in worms_list:
                        if worm.is_alive():
                            # Calculer la distance entre le ver et l'explosion
                            distance = math.sqrt((worm.rect.centerx - projectile.x)**2 + 
                                               (worm.rect.centery - projectile.y)**2)
                            if distance < explosion_radius:
                                # Dégâts avec formule quadratique (plus de dégâts près du centre)
                                distance_ratio = distance / explosion_radius
                                damage = int(max_damage * (1 - distance_ratio) ** 2)
                                damage = max(5, damage)  # Minimum 5 HP de dégâts
                                worm.take_damage(damage)
                                print(f"Ver {worm.name} touché par explosion ! -{damage} HP (distance: {int(distance)}px)")
                
                projectiles.remove(projectile)
                continue
        else:
            # Projectile normal (roquette)
            projectile.update()
            
            # Collision avec le terrain
            if terrain.is_solid(projectile.x, projectile.y):
                terrain.create_crater(projectile.x, projectile.y, radius=30)
                projectiles.remove(projectile)
                continue

        # Collision avec les vers ennemis
        hit = False
        for player, worms_list in players_worms.items():
            if player != projectile.owner:  # Ne pas toucher ses propres vers
                for worm in worms_list:
                    if worm.is_alive() and projectile.check_collision(worm.rect):
                        damage = 30 if isinstance(projectile, Grenade) else 20
                        worm.take_damage(damage)
                        terrain.create_crater(projectile.x, projectile.y, radius=30)
                        projectiles.remove(projectile)
                        print(f"Ver {worm.name} touché !")
                        hit = True
                        break
            if hit:
                break
        if hit:
            continue

        # Projectile hors écran
        if projectile.is_out_of_bounds(WIDTH, HEIGHT):
            projectiles.remove(projectile)

    # ---------------------------
    #  CHANGEMENT DE TOUR
    # ---------------------------
    if not game_over and len(projectiles) == 0 and last_shooter is not None:
        next_turn()
        last_shooter = None

    # ---------------------------
    #  AFFICHAGE
    # ---------------------------
    
    if in_menu:
        # Afficher le menu principal
        UI.draw_menu(screen, WIDTH, HEIGHT)
    
    elif in_game_setup:
        # Afficher l'écran de configuration de partie
        UI.draw_game_setup(screen, WIDTH, HEIGHT, num_players, worms_per_player)
        
        # Dessiner le visualizer du terrain
        visualizer_rect = pygame.Rect(WIDTH // 2 - 140, 520, 280, 140)
        
        # Créer une miniature du terrain sélectionné
        miniature = pygame.Surface((280, 140))
        miniature.fill((135, 206, 235))  # Fond ciel bleu
        
        if selected_terrain == 0 or terrain_files[selected_terrain] == "random":
            # Afficher "ALÉATOIRE"
            font = pygame.font.Font(None, 36)
            text = font.render("ALÉATOIRE", True, (255, 255, 255))
            text_rect = text.get_rect(center=(140, 70))
            miniature.blit(text, text_rect)
        else:
            # Charger et afficher le terrain
            import os
            if os.path.exists(terrain_files[selected_terrain]):
                with open(terrain_files[selected_terrain], 'r') as f:
                    lines = f.readlines()
                
                block_size = 3.5  # Taille plus petite pour afficher 40 lignes dans 140px de hauteur
                for row_idx, line in enumerate(lines[:40]):  # Afficher toutes les 40 lignes
                    line = line.rstrip('\n')
                    for col_idx, char in enumerate(line[:60]):  # 60 colonnes max
                        x = col_idx * block_size
                        y = row_idx * block_size
                        if char == 'T':  # Terre
                            pygame.draw.rect(miniature, (139, 90, 43), (int(x), int(y), int(block_size), int(block_size)))
                        elif char == 'W':  # Eau
                            pygame.draw.rect(miniature, (30, 144, 255), (int(x), int(y), int(block_size), int(block_size)))
        
        screen.blit(miniature, visualizer_rect)
    
    elif in_settings:
        # Afficher l'écran de paramètres
        if waiting_for_key:
            # Dessiner d'abord les settings
            UI.draw_settings(screen, WIDTH, HEIGHT, controls)
            # Puis la fenêtre de prompt par-dessus
            control_labels = {
                'left': 'Déplacer à gauche',
                'right': 'Déplacer à droite',
                'jump': 'Sauter',
                'aim_up': 'Angle vers le haut',
                'aim_down': 'Angle vers le bas',
                'shoot': 'Tirer',
                'weapon_menu': 'Menu d\'arme'
            }
            UI.draw_key_prompt(screen, WIDTH, HEIGHT, control_labels[key_to_change])
        else:
            UI.draw_settings(screen, WIDTH, HEIGHT, controls)
    
    else:
        # Affichage du jeu
        screen.fill((135, 206, 235))  # ciel bleu

        # Terrain
        terrain.draw(screen)

        # Afficher tous les vers de tous les joueurs
        for player, worms_list in players_worms.items():
            for worm in worms_list:
                if worm.is_alive():
                    UI.draw_player(screen, worm)
        
        # Ligne de visée + HUD du ver actif
        current_worm = get_current_worm()
        if current_worm and current_worm.is_alive():
            UI.draw_aim_line(screen, current_worm)
            UI.draw_hud(screen, current_worm, charging_power, time_remaining)

            # Trajectoire prévisionnelle si on charge un tir
            if is_charging:
                UI.draw_trajectory(screen, trajectory_calc, current_worm, charging_power)
            
            # Menu de sélection d'arme
            if weapon_menu_open:
                UI.draw_weapon_menu(screen, current_worm, current_worm.selected_weapon, current_worm.air_friction_enabled)

        # Dessiner les projectiles
        for projectile in projectiles:
            projectile.draw(screen)

        # Ecran de fin
        if game_over:
            UI.draw_game_over(screen, WIDTH, HEIGHT, winner)
        
        # Menu pause par-dessus le jeu
        if is_paused and not in_settings:
            UI.draw_pause_menu(screen, WIDTH, HEIGHT)
        
        # Écran de settings depuis la pause
        if is_paused and in_settings:
            if waiting_for_key:
                UI.draw_settings(screen, WIDTH, HEIGHT, controls)
                control_labels = {
                    'left': 'Déplacer à gauche',
                    'right': 'Déplacer à droite',
                    'jump': 'Sauter',
                    'aim_up': 'Angle vers le haut',
                    'aim_down': 'Angle vers le bas',
                    'shoot': 'Tirer',
                    'weapon_menu': 'Menu d\'arme'
                }
                UI.draw_key_prompt(screen, WIDTH, HEIGHT, control_labels[key_to_change])
            else:
                UI.draw_settings(screen, WIDTH, HEIGHT, controls)

    pygame.display.update()
    clock.tick(60)

pygame.quit()
