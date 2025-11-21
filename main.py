import os
import pygame

pygame.init()

# Plein écran noir
screen = pygame.display.set_mode((1280, 720), pygame.SCALED)
pygame.display.set_caption("Worms")
clock = pygame.time.Clock()

# Remplit l’écran en noir une seule fois
screen.fill((0, 0, 0))

# Boucle minimale : uniquement pour fermer avec Échap
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False

    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((0, 0, 0))

    if pygame.font:
        font = pygame.font.Font(None, 64)
        text = font.render("Worms", True, (255, 255, 255))
        background.blit(text, (0,0))
    
    screen.blit(background, (0, 0))
    pygame.display.update()
    clock.tick(60)  # limits FPS to 60
            

pygame.quit()
