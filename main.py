import os
import pygame
import math
from character import Worm
from gun import Projectile
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

# Contrôles par défaut
controls = {
    'left': pygame.K_LEFT,
    'right': pygame.K_RIGHT,
    'jump': pygame.K_SPACE,
    'aim_up': pygame.K_UP,
    'aim_down': pygame.K_DOWN,
    'shoot': pygame.K_RETURN
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

# Liste des projectiles
projectiles = []

# Dernier joueur qui a tiré
last_shooter = None


def init_game():
    """Réinitialise la partie"""
    global terrain, players_worms, projectiles, player_names
    global charging_power, is_charging, game_over, winner
    global current_player_index, current_worm_index, last_shooter

    terrain = Terrain(WIDTH, HEIGHT)
    
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
    global current_player_index, current_worm_index
    
    # Passer au joueur suivant
    current_player_index = (current_player_index + 1) % len(player_names)
    
    # Faire tourner le ver du joueur actuel
    player = get_current_player()
    current_worm_index[player] = (current_worm_index[player] + 1) % len(players_worms[player])
    
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
            start_button = pygame.Rect(WIDTH // 2 - 120, HEIGHT - 100, 240, 60)
            
            if minus_players.collidepoint(mouse_pos) and num_players > 2:
                num_players -= 1
            elif plus_players.collidepoint(mouse_pos):
                num_players += 1
            elif minus_worms.collidepoint(mouse_pos) and worms_per_player > 1:
                worms_per_player -= 1
            elif plus_worms.collidepoint(mouse_pos):
                worms_per_player += 1
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
        
        # Clics dans le menu pause
        if is_paused and not in_settings and event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            continue_button = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2 - 70, 300, 60)
            settings_button = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2 + 10, 300, 60)
            quit_button = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2 + 90, 300, 60)
            
            if continue_button.collidepoint(mouse_pos):
                is_paused = False
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
                
                projectile = Projectile(
                    current_worm.rect.centerx,
                    current_worm.rect.centery,
                    current_worm.aim_angle,
                    charging_power,
                    owner=current_player
                )
                last_shooter = current_player

                projectiles.append(projectile)
                is_charging = False
                charging_power = 0

    # ---------------------------
    #  MISE À JOUR DU JEU
    # ---------------------------
    if not game_over and not in_menu and not in_game_setup and not in_settings and not is_paused:

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
                        worm.take_damage(20)
                        terrain.create_crater(projectile.x, projectile.y, radius=30)
                        projectiles.remove(projectile)
                        print(f"Ver du joueur {player} touché !")
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
                'shoot': 'Tirer'
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
            UI.draw_hud(screen, current_worm, charging_power)

            # Trajectoire prévisionnelle si on charge un tir
            if is_charging:
                UI.draw_trajectory(screen, trajectory_calc, current_worm, charging_power)

        # Dessiner les projectiles
        UI.draw_projectiles(screen, projectiles)

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
                    'shoot': 'Tirer'
                }
                UI.draw_key_prompt(screen, WIDTH, HEIGHT, control_labels[key_to_change])
            else:
                UI.draw_settings(screen, WIDTH, HEIGHT, controls)

    pygame.display.update()
    clock.tick(60)

pygame.quit()
