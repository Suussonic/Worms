import os
import pygame

pygame.init()

# Plein écran noir
screen = pygame.display.set_mode((1280, 720), pygame.SCALED)
pygame.display.set_caption("Worms")

# Remplit l’écran en noir une seule fois
screen.fill((0, 0, 0))
pygame.display.update()

# Boucle minimale : uniquement pour fermer avec Échap
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((170, 238, 187))
    if pygame.font:
        font = pygame.font.Font(None, 64)
        text = font.render("Worms", True, (255, 255, 255))
        background.blit(text)

pygame.quit()
