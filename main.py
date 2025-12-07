import os
import pygame
import math
from character import Worm
from gun import Projectile

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

mon_ver = Worm(100, 100, 20, 40)  # x, y, width, height
projectiles = []  # Liste pour stocker tous les projectiles

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
        
        # Contrôle de l'angle de tir
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                mon_ver.aim_angle = min(mon_ver.aim_angle + 5, 90)  # Max 90°
            elif event.key == pygame.K_DOWN:
                mon_ver.aim_angle = max(mon_ver.aim_angle - 5, -180)  # Min -90°
        
        # Tirer un projectile avec la touche Entrée
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            # Le projectile part du centre du personnage avec l'angle et la puissance
            projectile = Projectile(mon_ver.rect.centerx, mon_ver.rect.centery, 
                                   mon_ver.aim_angle, mon_ver.aim_power)
            projectiles.append(projectile)

    mon_ver.handle_input()
    mon_ver.update(HEIGHT)
    
    # Mettre à jour tous les projectiles
    for projectile in projectiles[:]:
        projectile.update()
        if projectile.is_out_of_bounds(WIDTH, HEIGHT):
            projectiles.remove(projectile)

    screen.fill((50, 50, 50))
    
    pygame.draw.rect(screen, (0, 255, 0), mon_ver.rect)
    
    # Dessiner la ligne de visée
    aim_length = 50
    angle_rad = math.radians(mon_ver.aim_angle)
    end_x = mon_ver.rect.centerx + aim_length * math.cos(angle_rad)
    end_y = mon_ver.rect.centery + aim_length * math.sin(angle_rad)
    pygame.draw.line(screen, (255, 255, 0), 
                    (mon_ver.rect.centerx, mon_ver.rect.centery), 
                    (end_x, end_y), 3)
    
    # Afficher l'angle à l'écran
    font = pygame.font.Font(None, 36)
    angle_text = font.render(f"Angle: {mon_ver.aim_angle}°", True, (255, 255, 255))
    screen.blit(angle_text, (10, 10))
    
    # Dessiner tous les projectiles
    for projectile in projectiles:
        projectile.draw(screen) 
    
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
