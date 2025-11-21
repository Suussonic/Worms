import pygame

pygame.init()

# Plein écran noir
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("Worms")
clock = pygame.time.Clock()

# Remplit l’écran en noir une seule fois
screen.fill((0, 0, 0))
pygame.display.update()

# Boucle minimale : uniquement pour fermer avec Échap
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False
    clock.tick(60)  # limits FPS to 60
            

pygame.quit()
