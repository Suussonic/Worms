import os
import pygame
import math
from character import Worm
from gun import Projectile
from trajectory import TrajectoryCalculator
from enemy import Enemy
from terrain import Terrain
from UI import UI

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Variables de jeu
game_over = False
winner = None

def init_game():
    """Initialise ou réinitialise le jeu"""
    global terrain, mon_ver, ennemi, projectiles, charging_power, is_charging, game_over, winner
    
    terrain = Terrain(WIDTH, HEIGHT)
    mon_ver = Worm(100, 100, 20, 40)
    ennemi = Enemy(WIDTH - 60, 100, 20, 40)
    projectiles = []
    charging_power = 0
    is_charging = False
    game_over = False
    winner = None

trajectory_calc = TrajectoryCalculator(gravity=0.5)

# Initialiser le jeu
init_game()

# Plein écran noir
# screen = pygame.display.set_mode((1280, 720), pygame.SCALED)
# pygame.display.set_caption("Worms")
# clock = pygame.time.Clock()

# Remplit l’écran en noir une seule fois
# screen.fill((0, 0, 0))

# Boucle minimale : uniquement pour fermer avec Échap
running = True
while running:
    for event in pygame.event.get():
        #if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
        #    running = False
        if event.type == pygame.QUIT:
            running = False
        
        # Gestion du bouton rejouer
        if game_over and event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            button_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 50, 200, 50)
            if button_rect.collidepoint(mouse_pos):
                init_game()
        
        # Contrôle de l'angle de tir (seulement si le jeu n'est pas terminé)
        if not game_over and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                mon_ver.aim_angle = min(mon_ver.aim_angle + 5, 90)  # Max 90°
            elif event.key == pygame.K_DOWN:
                mon_ver.aim_angle = max(mon_ver.aim_angle - 5, -180)  # Min -90°
            elif event.key == pygame.K_RETURN:
                # Commencer à charger la puissance
                is_charging = True
                charging_power = 0
        
        # Tirer quand on relâche Entrée (seulement si le jeu n'est pas terminé)
        if not game_over and event.type == pygame.KEYUP and event.key == pygame.K_RETURN:
            if is_charging:
                # Tirer avec la puissance chargée
                projectile = Projectile(mon_ver.rect.centerx, mon_ver.rect.centery, 
                                       mon_ver.aim_angle, charging_power)
                projectiles.append(projectile)
                is_charging = False
                charging_power = 0

    # Ne mettre à jour que si le jeu n'est pas terminé
    if not game_over:
        # Augmenter la puissance si on est en train de charger
        if is_charging:
            charging_power = min(charging_power + 0.2, 20)  # Max 20
        
        mon_ver.handle_input()
        mon_ver.update(HEIGHT, terrain)
        ennemi.update(HEIGHT, terrain)
        
        # Vérifier si quelqu'un a gagné
        if not ennemi.is_alive():
            game_over = True
            winner = 'player'
        elif not mon_ver.is_alive():
            game_over = True
            winner = 'enemy'
        
        # Vérifier si quelqu'un a gagné
        if not ennemi.is_alive():
            game_over = True
            winner = 'player'
        elif not mon_ver.is_alive():
            game_over = True
            winner = 'enemy'
    
    # Mettre à jour tous les projectiles
    for projectile in projectiles[:]:
        if not projectile.active:
            projectiles.remove(projectile)
            continue
            
        projectile.update()
        
        # Vérifier collision avec le terrain
        if terrain.is_solid(projectile.x, projectile.y):
            terrain.create_crater(projectile.x, projectile.y, radius=30)
            projectile.active = False
            projectiles.remove(projectile)
            print(f"Impact terrain à ({int(projectile.x)}, {int(projectile.y)})")
            continue
        
        # Vérifier collision avec l'ennemi uniquement
        # (Le joueur ne peut pas se toucher lui-même)
        if ennemi.is_alive() and projectile.check_collision(ennemi.rect):
            ennemi.take_damage(20)  # 20 dégâts
            projectile.active = False
            projectiles.remove(projectile)
            print(f"Ennemi touché! HP restants: {ennemi.hp}")  # Debug
            continue
        
        if projectile.is_out_of_bounds(WIDTH, HEIGHT):
            projectiles.remove(projectile)

    screen.fill((135, 206, 235))  # Bleu ciel comme fond
    
    # Dessiner le terrain en premier
    terrain.draw(screen)
    
    # Dessiner le joueur
    UI.draw_player(screen, mon_ver)
    
    # Dessiner l'ennemi
    UI.draw_enemy(screen, ennemi)
    
    # Dessiner la ligne de visée
    UI.draw_aim_line(screen, mon_ver)
    
    # Afficher le HUD (angle et puissance)
    UI.draw_hud(screen, mon_ver, charging_power)
    
    # Afficher la trajectoire prédite si on charge
    if is_charging:
        UI.draw_trajectory(screen, trajectory_calc, mon_ver, charging_power)
    
    # Dessiner tous les projectiles
    UI.draw_projectiles(screen, projectiles)
    
    # Afficher l'écran de victoire si le jeu est terminé
    if game_over:
        UI.draw_game_over(screen, WIDTH, HEIGHT, winner)
    
    #Create background
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((0, 0, 0))

    #Show text
    #if pygame.font:
    #    font = pygame.font.Font(None, 64)
    #    text = font.render("Worms", True, (255, 255, 255))
    #    background.blit(text, (0,0))
    
    #screen.blit(background, (0, 0))
    pygame.display.update()

    clock.tick(60)  # limits FPS to 60
            

pygame.quit()
