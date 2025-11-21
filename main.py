import pygame

pygame.init()

# Plein écran noir
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("Fullscreen Black Screen")

# Remplit l’écran en noir une seule fois
screen.fill((0, 0, 0))
pygame.display.update()

# Boucle minimale : uniquement pour fermer avec Échap
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False

pygame.quit()
