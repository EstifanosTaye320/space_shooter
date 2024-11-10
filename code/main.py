import pygame
from os.path import join
from random import randint

pygame.init()
WINDOW_WIDTH, WINDOW_HEIGHT = 1289, 720
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Space Shooter")
running = True

surf = pygame.Surface((100, 200))
surf.fill("orange") # not in the loop
x = 100

player_surface = pygame.image.load(join("images", "player.png")).convert_alpha()

star_surface = pygame.image.load(join("images", "star.png")).convert_alpha()

star_locs = [(randint(0, WINDOW_WIDTH), randint(0, WINDOW_HEIGHT)) for i in range(20)]

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    display_surface.fill("darkgrey") # reset screen
    for loc in star_locs:
        display_surface.blit(star_surface, loc)
    display_surface.blit(player_surface, (x, 150))
    x += 0.1
    pygame.display.update() # show changes

pygame.quit()