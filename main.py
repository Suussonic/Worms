import os
import pygame
import math
from character import Worm
from gun import Projectile
from trajectory import TrajectoryCalculator
from terrain import Terrain
from UI import UI

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Variables de jeu
game_over = False
winner = None

# "p1" = joueur 1 (gauche), "p2" = joueur 2 (droite)
current_turn = "p1"

# Gestion du tir
charging_power = 0
is_charging = False

# Liste des projectiles
projectiles = []

# Dernier joueur qui a tiré ("p1" ou "p2")
last_shooter = None


def init_game():
    """Réinitialise la partie"""
    global terrain, mon_ver, ennemi, projectiles
    global charging_power, is_charging, game_over, winner
    global current_turn, last_shooter

    terrain = Terrain(WIDTH, HEIGHT)

    # Joueur 1 (gauche)
    mon_ver = Worm(100, 100, 20, 40)

    # Joueur 2 (droite) : aussi un Worm
    ennemi = Worm(WIDTH - 120, 100, 20, 40)

    projectiles = []
    charging_power = 0
    is_charging = False
    game_over = False
    winner = None

    current_turn = "p1"
    last_shooter = None

    print("Tour du joueur 1")


trajectory_calc = TrajectoryCalculator(gravity=0.5)

# Lancer une première fois
init_game()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Clic sur le bouton REJOUER
        if game_over and event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            button_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 50, 200, 50)
            if button_rect.collidepoint(mouse_pos):
                init_game()

        # ---------------------------
        #  GESTION DES TOUCHES
        # ---------------------------
        if not game_over and event.type == pygame.KEYDOWN:

            # Changement d'angle (flèches haut / bas)
            if event.key == pygame.K_UP:
                if current_turn == "p1":
                    mon_ver.aim_angle = min(mon_ver.aim_angle + 5, 90)
                else:
                    ennemi.aim_angle = min(ennemi.aim_angle + 5, 90)

            elif event.key == pygame.K_DOWN:
                if current_turn == "p1":
                    mon_ver.aim_angle = max(mon_ver.aim_angle - 5, -180)
                else:
                    ennemi.aim_angle = max(ennemi.aim_angle - 5, -180)

            # Début de la charge du tir (Entrée)
            elif event.key == pygame.K_RETURN:
                # On peut charger seulement si aucun projectile en vol
                if len(projectiles) == 0:
                    is_charging = True
                    charging_power = 0

        # Relâchement des touches
        if not game_over and event.type == pygame.KEYUP:
            # Tir quand on relâche Entrée
            if event.key == pygame.K_RETURN and is_charging and len(projectiles) == 0:
                if current_turn == "p1":
                    # Tir du joueur 1
                    projectile = Projectile(
                        mon_ver.rect.centerx,
                        mon_ver.rect.centery,
                        mon_ver.aim_angle,
                        charging_power,
                        owner="p1"
                    )
                    last_shooter = "p1"
                else:
                    # Tir du joueur 2
                    projectile = Projectile(
                        ennemi.rect.centerx,
                        ennemi.rect.centery,
                        ennemi.aim_angle,
                        charging_power,
                        owner="p2"
                    )
                    last_shooter = "p2"

                projectiles.append(projectile)
                is_charging = False
                charging_power = 0

    # ---------------------------
    #  MISE À JOUR DU JEU
    # ---------------------------
    if not game_over:

        # Charge de la puissance pendant que la touche est maintenue
        if is_charging:
            charging_power = min(charging_power + 0.2, 20)

        # Déplacement du joueur dont c'est le tour
        # (Q / D / flèches gauche-droite / espace gérés dans handle_input)
        if len(projectiles) == 0:
            if current_turn == "p1":
                mon_ver.handle_input()
            else:
                ennemi.handle_input()

        # Mise à jour des deux vers (gravité, collisions, etc.)
        mon_ver.update(HEIGHT, terrain)
        ennemi.update(HEIGHT, terrain)

        # Vérifier si l'un des deux est mort
        if not ennemi.is_alive():
            game_over = True
            winner = "player"
        elif not mon_ver.is_alive():
            game_over = True
            winner = "enemy"

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

        # Collision selon le joueur qui a tiré
        if projectile.owner == "p1":
            # Tir du joueur 1 → peut toucher le joueur 2
            if ennemi.is_alive() and projectile.check_collision(ennemi.rect):
                ennemi.take_damage(20)
                projectiles.remove(projectile)
                print("Joueur 2 touché !")
                continue
        elif projectile.owner == "p2":
            # Tir du joueur 2 → peut toucher le joueur 1
            if mon_ver.is_alive() and projectile.check_collision(mon_ver.rect):
                mon_ver.take_damage(20)
                projectiles.remove(projectile)
                print("Joueur 1 touché !")
                continue

        # Projectile hors écran
        if projectile.is_out_of_bounds(WIDTH, HEIGHT):
            projectiles.remove(projectile)

    # ---------------------------
    #  CHANGEMENT DE TOUR
    # ---------------------------
    if not game_over and len(projectiles) == 0 and last_shooter is not None:
        if last_shooter == "p1" and current_turn == "p1":
            current_turn = "p2"
            print("Tour du joueur 2")
        elif last_shooter == "p2" and current_turn == "p2":
            current_turn = "p1"
            print("Tour du joueur 1")
        last_shooter = None

    # ---------------------------
    #  AFFICHAGE
    # ---------------------------
    screen.fill((135, 206, 235))  # ciel bleu

    # Terrain
    terrain.draw(screen)

    # Joueur 1 (vert) et Joueur 2 (rouge via UI.draw_enemy)
    UI.draw_player(screen, mon_ver)
    UI.draw_player(screen, ennemi)

    # Ligne de visée + HUD du joueur dont c'est le tour
    if current_turn == "p1":
        UI.draw_aim_line(screen, mon_ver)
        UI.draw_hud(screen, mon_ver, charging_power)
    else:
        UI.draw_aim_line(screen, ennemi)
        UI.draw_hud(screen, ennemi, charging_power)

    # Trajectoire prévisionnelle si on charge un tir
    if is_charging:
        if current_turn == "p1":
            UI.draw_trajectory(screen, trajectory_calc, mon_ver, charging_power)
        else:
            UI.draw_trajectory(screen, trajectory_calc, ennemi, charging_power)

    # Dessiner les projectiles
    UI.draw_projectiles(screen, projectiles)

    # Ecran de fin
    if game_over:
        UI.draw_game_over(screen, WIDTH, HEIGHT, winner)

    pygame.display.update()
    clock.tick(60)

pygame.quit()
